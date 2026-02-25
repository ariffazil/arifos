#!/usr/bin/env python3
"""
888_SIGNER: Offline Sovereign Key Utility

This standalone script lives ONLY on the Sovereign's secure local machine.
It generates the ed25519 Sovereign Keypair and signs 888_HOLD ratification challenges.

DO NOT DEPLOY THIS TO THE MCP SERVER OR ANY NETWORKED ENVIRONMENT.
"""

import os
import sys
import argparse
import base64
try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
except ImportError:
    print("[!] Error: 'cryptography' package is required.")
    print("    Install it locally via: pip install cryptography")
    sys.exit(1)

KEY_FILE = "sovereign_private_key.pem"
PUB_KEY_FILE = "sovereign_public_key.pem"

def generate_keys():
    """Generates a new ed25519 keypair if one does not exist."""
    if os.path.exists(KEY_FILE):
        print(f"[-] Key file {KEY_FILE} already exists. Refusing to overwrite.")
        return

    print("[*] Forging new Sovereign Keypair (ed25519)...")
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Save Private Key (KEEP THIS SECRET AND OFFLINE)
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(KEY_FILE, "wb") as f:
        f.write(private_bytes)
    os.chmod(KEY_FILE, 0o600)  # Restrict permissions

    # Save Public Key (Deploy this to aclip_cai PUBLIC_KEY_APEX)
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(PUB_KEY_FILE, "wb") as f:
        f.write(public_bytes)

    print(f"[+] Sovereign Private Key saved to: {KEY_FILE} (SECURE THIS)")
    print(f"[+] Sovereign Public Key saved to:  {PUB_KEY_FILE} (DEPLOY TO arifOS)")

def sign_challenge(challenge: str):
    """Signs a challenge string with the Sovereign Private Key."""
    if not os.path.exists(KEY_FILE):
        print(f"[!] Error: Private key not found at {KEY_FILE}.")
        print("[!] Run `python 888_signer.py generate` first.")
        sys.exit(1)

    with open(KEY_FILE, "rb") as f:
        private_bytes = f.read()

    private_key = serialization.load_pem_private_key(
        private_bytes,
        password=None
    )

    # Sign the challenge
    challenge_bytes = challenge.encode('utf-8')
    signature = private_key.sign(challenge_bytes)
    
    # Encode the signature as base64 for easy transport (copy-pasting into chat)
    token = base64.b64encode(signature).decode("utf-8")

    print("\n" + "=" * 50)
    print("⚖️  888 SOVEREIGN RATIFICATION TOKEN")
    print("="*50)
    print(f"Challenge: {challenge}")
    print(f"Token:     {token}")
    print("="*50)
    print("Copy the Token string and provide it to the AI to release the 888_HOLD.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="888 Sovereign Offline Signer")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Generate command
    parser_gen = subparsers.add_parser("generate", help="Generate a new Sovereign Keypair")

    # Sign command
    parser_sign = subparsers.add_parser("sign", help="Sign a ratification challenge")
    parser_sign.add_argument("challenge", help="The 888_HOLD ratification_challenge string")

    args = parser.parse_args()

    if args.command == "generate":
        generate_keys()
    elif args.command == "sign":
        sign_challenge(args.challenge)
    else:
        parser.print_help()
