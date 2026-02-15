"""
Incremental Merkle Tree — O(log N) Append

Replaces the O(N) full-tree recomputation in persistent_ledger.py.
Maintains a frontier of Merkle tree levels, updating only the path
from new leaf to root.

From: https://github.com/ethereum/research/blob/master/beacon_chain_impl/progressive_merkle_tree.py
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# SHA256 hash of empty data (for padding)
EMPTY_HASH = hashlib.sha256(b"").hexdigest()


def sha256_hash(left: str, right: str) -> str:
    """Compute SHA256 hash of two concatenated hashes."""
    return hashlib.sha256((left + right).encode()).hexdigest()


@dataclass
class IncrementalMerkleTree:
    """
    Incremental Merkle tree with O(log N) append.
    
    Maintains a frontier (list) where frontier[i] is the hash at level i
    that is "complete" (has both children). New leaves fill in the right.
    
    Example after 5 leaves (0-4):
    
                    root (hash of L and R)
                   /    \
                  L      R
                /  \    /  \
               A    B  C    D
              / \  / \/ \  / \
             0  1 2  3 4  .  .  .
    
    Frontier = [E, hash(A,B), hash(hash(A,B), hash(C,D))]
    (where E = hash(4, empty) is incomplete)
    
    When we add leaf 5:
    - E becomes complete: hash(4, 5)
    - Propagate up, updating frontier
    """
    
    frontier: List[str] = field(default_factory=list)
    leaf_count: int = 0
    
    def append(self, leaf_hash: str) -> str:
        """
        Append a new leaf and return the new Merkle root.
        
        Complexity: O(log N) where N = number of leaves
        """
        current_hash = leaf_hash
        
        for level in range(len(self.frontier) + 1):
            if level == len(self.frontier):
                # New level - frontier extends
                self.frontier.append(current_hash)
                break
            
            if self.leaf_count & (1 << level) == 0:
                # Bit is 0: left child complete, store as frontier
                self.frontier[level] = current_hash
                break
            else:
                # Bit is 1: combine with stored left sibling
                current_hash = sha256_hash(self.frontier[level], current_hash)
        
        self.leaf_count += 1
        return self.root()
    
    def root(self) -> str:
        """Compute current Merkle root from frontier."""
        if not self.frontier:
            return EMPTY_HASH
        
        # Combine frontier from right to left
        result = self.frontier[-1]
        for i in range(len(self.frontier) - 2, -1, -1):
            # Check if this level is "filled" in current leaf_count
            if self.leaf_count & (1 << i):
                result = sha256_hash(self.frontier[i], result)
            else:
                # Pad with empty
                result = sha256_hash(self.frontier[i], EMPTY_HASH)
        
        return result
    
    def get_proof(self, leaf_index: int, leaf_hash: str) -> List[Tuple[str, bool]]:
        """
        ⚠️  DEV/UNSAFE: This proof method is NOT cryptographically secure.
        
        The implementation uses frontier approximation and does NOT produce
        valid Merkle inclusion proofs. Do not use for cryptographic verification.
        
        TODO: Implement proper Merkle tree storage for real proofs.
        
        Returns list of (sibling_hash, is_right) tuples.
        is_right = True if sibling is on the right (we're left).
        """
        if leaf_index >= self.leaf_count:
            raise ValueError(f"Leaf index {leaf_index} >= count {self.leaf_count}")
        
        proof = []
        current_idx = leaf_index
        current_hash = leaf_hash
        
        for level in range(len(self.frontier)):
            sibling_idx = current_idx ^ 1  # Flip last bit
            
            if sibling_idx < self.leaf_count:
                # Sibling exists in tree
                # We need to reconstruct sibling hash from frontier
                sibling_hash = self._get_hash_at_index(sibling_idx, level)
            else:
                # Sibling is empty
                sibling_hash = EMPTY_HASH
            
            is_right = (current_idx % 2 == 0)  # We're left if index is even
            proof.append((sibling_hash, is_right))
            
            # Move up
            current_idx //= 2
        
        return proof
    
    def _get_hash_at_index(self, index: int, level: int) -> str:
        """Reconstruct hash at given index and level (for proofs)."""
        # This is expensive - in production, store full tree or use different proof approach
        # For now, return frontier[level] as approximation
        if level < len(self.frontier):
            return self.frontier[level]
        return EMPTY_HASH
    
    def to_dict(self) -> dict:
        """Serialize to dict for database storage."""
        return {
            "frontier": self.frontier,
            "leaf_count": self.leaf_count,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "IncrementalMerkleTree":
        """Deserialize from dict."""
        return cls(
            frontier=data.get("frontier", []),
            leaf_count=data.get("leaf_count", 0),
        )


@dataclass
class PersistentMerkleState:
    """
    Persistent Merkle state for PostgreSQL storage.
    Replaces the O(N) SELECT + full recompute.
    """
    
    merkle_tree: IncrementalMerkleTree = field(default_factory=IncrementalMerkleTree)
    last_sequence: int = 0
    
    def append_leaf(self, leaf_hash: str, sequence: int) -> str:
        """Append leaf and return new root."""
        root = self.merkle_tree.append(leaf_hash)
        self.last_sequence = sequence
        return root
    
    def get_root(self) -> str:
        """Get current Merkle root."""
        return self.merkle_tree.root()
    
    def to_json(self) -> dict:
        """Serialize for JSONB column."""
        return {
            "merkle_tree": self.merkle_tree.to_dict(),
            "last_sequence": self.last_sequence,
        }
    
    @classmethod
    def from_json(cls, data: dict) -> "PersistentMerkleState":
        """Deserialize from JSONB."""
        tree_data = data.get("merkle_tree", {})
        return cls(
            merkle_tree=IncrementalMerkleTree.from_dict(tree_data),
            last_sequence=data.get("last_sequence", 0),
        )


# Global singleton for process-level caching (optional optimization)
_merkle_cache: dict = {}


def get_merkle_state(ledger_id: str = "default") -> PersistentMerkleState:
    """Get cached Merkle state (if using in-memory caching)."""
    if ledger_id not in _merkle_cache:
        _merkle_cache[ledger_id] = PersistentMerkleState()
    return _merkle_cache[ledger_id]


def clear_merkle_cache(ledger_id: Optional[str] = None):
    """Clear Merkle cache (for testing or reset)."""
    global _merkle_cache
    if ledger_id:
        _merkle_cache.pop(ledger_id, None)
    else:
        _merkle_cache = {}
