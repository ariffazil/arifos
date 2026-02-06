#!/bin/bash

# Script to update the arifOS APPS site with enhanced product-focused content

echo "Updating arifOS APPS site with product-focused enhancements..."

# Clone the repository if not already present
if [ ! -d "/tmp/arif-fazil-sites" ]; then
    echo "Cloning arif-fazil-sites repository..."
    git clone https://github.com/ariffazil/arif-fazil-sites.git /tmp/arif-fazil-sites
fi

# Backup original files
echo "Creating backups..."
cp /tmp/arif-fazil-sites/APPS/index.html /tmp/arif-fazil-sites/APPS/index.html.backup
cp /tmp/arif-fazil-sites/APPS/src/App.tsx /tmp/arif-fazil-sites/APPS/src/App.tsx.backup

# Update the index.html file
echo "Updating index.html with product-focused content..."
cp /root/.openclaw/workspace/enhanced_index.html /tmp/arif-fazil-sites/APPS/index.html

# Update the App.tsx file
echo "Updating App.tsx with product-focused content..."
cp /root/.openclaw/workspace/enhanced_App.tsx /tmp/arif-fazil-sites/APPS/src/App.tsx

# Update the README to reflect the product focus
echo "Updating APPS README..."
cat > /tmp/arif-fazil-sites/APPS/README.md << 'EOF'
# arifOS APPS — Product & Implementation Hub

**The APPS Layer** — Production-ready constitutional AI governance products and implementation guides.

Live at [arifos.arif-fazil.com](https://arifos.arif-fazil.com)

## Product Overview

arifOS delivers production-grade constitutional AI governance through a 7-layer product stack:

- **L1 PROMPT**: Instant governance with system prompts (30% coverage)
- **L2 SKILLS**: Templated governance solutions (50% coverage) 
- **L3 WORKFLOW**: Automated governance workflows (70% coverage)
- **L4 TOOLS**: Production MCP tools (80% coverage)
- **L5 AGENTS**: Autonomous governance agents (90% coverage)
- **L6 INSTITUTION**: Full institutional systems (100% coverage)
- **L7 AGI**: Advanced constitutional AI (Research)

## Key Products

### MCP Tool Suite
9 canonical tools enforcing 9 constitutional floors:
- **init_gate**: Session initiation and authorization
- **agi_sense**: Input parsing and intent detection
- **agi_think**: Hypothesis generation
- **agi_reason**: Logical reasoning
- **asi_empathize**: Stakeholder impact assessment
- **asi_align**: Constitutional alignment checking
- **apex_verdict**: Final constitutional judgment
- **reality_search**: External verification
- **vault_seal**: Immutable sealing

### Governance Metrics
- **Ω₀ Tracking**: Real-time uncertainty monitoring (target: 0.03-0.05)
- **Verdict System**: SEAL/SABAR/VOID/888_HOLD classification
- **Audit Trail**: Immutable VAULT-999 ledger
- **Compliance**: 100% constitutional floor enforcement

## Implementation Guide

### Quick Start
```bash
# Install production package
pip install arifos

# Verify installation
python -c "import arifos; print(f'arifOS v{arifos.__version__} installed')"
```

### MCP Integration
Add to your `.mcp.json`:
```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"]
    }
  }
}
```

## Technology Stack

- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS
- Lucide React (icons)
- shadcn/ui components (Card, Badge, Button, Separator)
- FastMCP (MCP protocol implementation)

## Production Endpoints

- Health Check: `https://aaamcp.arif-fazil.com/health`
- MCP Endpoint: `https://aaamcp.arif-fazil.com/mcp`
- SSE Stream: `https://aaamcp.arif-fazil.com/sse`
- Dashboard: `https://aaamcp.arif-fazil.com/dashboard`
- API Docs: `https://aaamcp.arif-fazil.com/docs`

## Business Value

arifOS products deliver measurable governance outcomes:

- **Risk Reduction**: Proactive identification and mitigation of AI risks
- **Compliance Assurance**: 100% adherence to constitutional floors
- **Audit Readiness**: Immutable logs and verifiable processes
- **Scalability**: Enterprise-grade performance and reliability
- **Cost Efficiency**: Reduced manual oversight through automation

## Architecture Principles

1. **Constitutional Enforcement**: All decisions pass through 9 constitutional floors
2. **Uncertainty Tracking**: Ω₀ monitoring within 0.03-0.05 range
3. **Immutable Audit**: All decisions sealed in VAULT-999
4. **Human Sovereignty**: 888 Judge maintains final authority
5. **Reversibility**: F1 Amanah ensures all actions can be undone

## Deployment Options

- **SaaS**: Managed service at aaamcp.arif-fazil.com
- **On-Premise**: Self-hosted MCP server
- **Hybrid**: Federated deployment model
- **Edge**: Containerized deployment options

---

*arifOS — Production-Ready Constitutional AI Governance*
*Ditempa Bukan Diberi — Forged, Not Given*
EOF

echo "Enhanced APPS site files updated successfully!"
echo ""
echo "Files updated:"
echo "- /tmp/arif-fazil-sites/APPS/index.html"
echo "- /tmp/arif-fazil-sites/APPS/src/App.tsx"
echo "- /tmp/arif-fazil-sites/APPS/README.md"
echo ""
echo "Next steps:"
echo "1. Review the changes in the /tmp/arif-fazil-sites/APS directory"
echo "2. Test the changes locally if needed"
echo "3. Commit and push to the repository"
echo "4. Deploy to production"