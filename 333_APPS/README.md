# 333_APPS - arifOS Application Layer

## Overview
This layer contains the core applications and capabilities of the arifOS system, organized into two primary categories for maximum clarity and operational efficiency. The structure implements the full arifOS stack from L1-L7 with constitutional governance throughout.

## Complete Stack Architecture

### L1: PROMPTS (System Prompts)
Zero-context instructions for direct LLM integration. Three variants:

- **Concise Prompt**: ~200 tokens, API-efficient while maintaining safety floors
- **Comprehensive Prompt**: Full Constitutional Code of Conduct (CCC) with 9-Paradox Matrix and Tri-Witness protocol
- **Human-Readable Prompt**: Simplified language for manual copy-pasting with human sovereignty acknowledgment

### L2: SKILLS (Templates)
Modular functional templates enforcing specific constitutional floors:

- **f1_reversibility_check**: Verifies actions can be undone before proceeding
- **f9_authenticity_scan**: Scans for "Hantu" patterns, ensuring authentic responses
- **code_review_governed**: Audits code against Floor 4 (Clarity) and Floor 1 (Reversibility)

### L3-L4: ACTIONS (Workflows & MCP Tools)
Execution layer with Model Context Protocol (MCP) integration:

- **_init_ (🔑)**: Session Gate - injection scan (F12) and session ledger initialization
- **_agi_ (🧠)**: Mind/Logic - executes logic and fact-checking
- **_asi_ (💚)**: Heart/Care - simulates ethical impact and empathy  
- **_apex_ (⚖️)**: Soul/Law - renders verdict based on 9-Paradox Matrix
- **_vault_ (🔒)**: Immutable ledger (Merkle DAG) for audit trails
- **_trinity_ (🔄)**: Full 000→999 pipeline (Sense → Think → Map → Judge → Seal)

### L5: AGENTS (Autonomous Entities)
Specialized autonomous agents performing specific roles:

- **Auditor Agent**: Monitors compliance and constitutional adherence
- **Validator Agent**: Verifies outputs and decision quality
- **Guardian Agent**: Ensures safety and harm prevention

### L6: INSTITUTION (Collective Governance)
The Institutional Layer ("Balai") - governance of the collective.

- **Role**: Multi-Agent System (MAS) mirroring human organizational structures
- **Function**: Consensus Protocol via Tri-Witness voting between specialized agents
- **Focus**: F8 (Consensus) - ensures no single rogue prompt bypasses 888 Judge authority
- **Analogy**: If L5 is an employee, L6 is the Board of Directors/Department managing handoffs

### L7: AGI (Evolutionary Governance) 
The Evolutionary Layer ("Tempa") - recursive governance and self-optimization.

- **Role**: Recursive Governance (Self-Healing)
- **Function**: Back-testing and weights adjustment based on Scar-Weight data
- **Focus**: F13 (Evolution) - manages system improvement while maintaining constitutional floors
- **Analogy**: R&D/Black Box Audit layer ensuring continuous alignment improvement

## Structure

### ACTIONS
The `ACTIONS` directory contains the 9 canonical atomic actions that form the foundational metabolic loop of arifOS. These are hardened, model-agnostic operations that implement the constitutional framework.

### SKILLS  
The `SKILLS` directory contains extended capabilities and tools built upon the atomic action foundation.

## Design Philosophy

This simplified two-category structure implements:
- **Maximum Clarity**: Clear distinction between atomic operations and extended capabilities
- **Minimum Complexity**: Two primary categories instead of layered hierarchies  
- **Operational Efficiency**: Direct access to core functions
- **Constitutional Compliance**: All operations aligned with arifOS floors

## L6-L7 Integration

### Institutional Layer (L6) Governance
- Multi-agent consensus protocols
- Collective decision-making frameworks
- Handoff management between specialized agents
- Stability maintenance (Peace² ≥ 1.0)

### Evolutionary Layer (L7) Governance
- Recursive self-improvement mechanisms
- Scar-weight analysis and learning
- Constitutional floor preservation during evolution
- Entropy reduction (ΔS < 0) optimization

## Navigation

- `ACTIONS/` - Core atomic operations (9 canonical actions)
- `SKILLS/` - Extended capabilities and tools

## Governance

All applications in this layer adhere to arifOS constitutional principles:
- Model-agnostic design
- Modular architecture
- Gödel lock verification
- Constitutional floor compliance
- Self-referential integrity
- Multi-agent consensus (L6)
- Recursive evolution (L7)