# L2_SKILLS — Deployment Guide

**Parameterized Template Deployment | v55.0-SEAL**

> *"From templates to tools — deploy constitutional governance in 5 minutes."*

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Direct Python Import
```bash
# Clone arifOS repository
git clone https://github.com/ariffazil/arifOS.git
cd arifOS

# Install dependencies
pip install -e ".[dev]"

# Use skills in your code
from L2_SKILLS.mcp_tool_templates import ConstitutionalSkill

skill = ConstitutionalSkill("f2_truth_verification")
result = skill.invoke(claim="Your claim here")
```

### Option 2: YAML Template Loading
```python
import yaml

# Load skill templates
with open("333_APPS/L2_SKILLS/skill_templates.yaml", "r") as f:
    skills = yaml.safe_load(f)

# Use a skill
truth_skill = skills["constitutional_skills"]["f2_truth_verification"]
print(truth_skill["invocation"])
```

### Option 3: MCP Server Integration
```json
{
  "mcpServers": {
    "arifos-skills": {
      "command": "python",
      "args": ["-m", "L2_SKILLS.mcp_tool_templates"],
      "env": {
        "ARIFOS_MODE": "PROD"
      }
    }
  }
}
```

---

## 📋 Deployment Options

### Local Development
```bash
# 1. Navigate to skills directory
cd 333_APPS/L2_SKILLS

# 2. Install in development mode
pip install -e .

# 3. Test skill invocation
python -c "from mcp_tool_templates import list_skills; print(list_skills())"
```

### Production Deployment
```bash
# 1. Install from PyPI (when published)
pip install arifos-skills

# 2. Configure environment
export ARIFOS_HOME="~/.arifos"
export ARIFOS_MODE="PROD"

# 3. Run skill server
python -m L2_SKILLS.server
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install -e ".[dev]"

EXPOSE 8000

CMD ["python", "-m", "L2_SKILLS.server", "--port", "8000"]
```

```bash
# Build and run
docker build -t arifos-skills .
docker run -p 8000:8000 arifos-skills
```

---

## 🏗️ Architecture Deployment Patterns

### Pattern 1: Standalone Skills (L2 Only)
```
┌─────────────────────────────────────┐
│  Your Application                   │
│  ┌─────────────────────────────┐   │
│  │  L2_SKILLS Templates        │   │
│  │  - skill_templates.yaml     │   │
│  │  - mcp_tool_templates.py    │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
              ↓
        Constitutional
        Validation
```

**Use when:** You need parameterized prompts without full MCP infrastructure.

### Pattern 2: Skills + MCP Tools (L2 + L4)
```
┌─────────────────────────────────────┐
│  MCP Client (Claude/Cursor)         │
│  ┌─────────────────────────────┐   │
│  │  L2_SKILLS                  │   │
│  │  (Template preparation)     │   │
│  └─────────────────────────────┘   │
│              ↓                      │
│  ┌─────────────────────────────┐   │
│  │  L4_TOOLS (codebase/mcp/)   │   │
│  │  (Constitutional enforcement)│  │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Use when:** You need both template flexibility and programmatic enforcement.

### Pattern 3: Full Stack (L1-L4)
```
┌─────────────────────────────────────┐
│  L1_PROMPT (System Instructions)    │
│  ┌─────────────────────────────┐   │
│  │  L2_SKILLS (Templates)      │   │
│  │  ┌─────────────────────┐   │   │
│  │  │  L3_WORKFLOW        │   │   │
│  │  │  (Sequences)        │   │   │
│  │  │  ┌─────────────┐   │   │   │
│  │  │  │  L4_TOOLS   │   │   │   │
│  │  │  │  (MCP)      │   │   │   │
│  │  │  └─────────────┘   │   │   │
│  │  └─────────────────────┘   │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Use when:** You need the complete constitutional stack.

---

## ⚙️ Configuration

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `ARIFOS_HOME` | `~/.arifos` | Base directory for skills |
| `ARIFOS_MODE` | `PROD` | PROD / STUDIO / DEBUG |
| `ARIFOS_SKILLS_PATH` | `333_APPS/L2_SKILLS` | Skills location |
| `ARIFOS_LOG_LEVEL` | `INFO` | DEBUG / INFO / WARNING |

### YAML Configuration (`~/.arifos/skills.yaml`)
```yaml
skills:
  enabled:
    - constitutional_skills
    - engineering_skills
    - workflow_skills
  
  defaults:
    f2_truth_threshold: 0.99
    f6_empathy_threshold: 0.70
    f8_genius_threshold: 0.80
  
  custom_skills_path: "./my_skills"
```

---

## 🎯 Deployment by Use Case

### Use Case: Personal Development
```bash
# Minimal setup — just the skills
pip install arifos-skills

# Use in Python
from arifos.skills import load_skill

skill = load_skill("code_review")
result = skill.review(code="your_code_here")
```

### Use Case: Team SOPs
```bash
# Deploy with Docker
docker-compose up -d

# Access skills API
curl http://localhost:8000/skills/list
curl -X POST http://localhost:8000/skills/invoke \
  -H "Content-Type: application/json" \
  -d '{"skill": "f2_truth_verification", "params": {"claim": "..."}}'
```

### Use Case: Enterprise
```bash
# Kubernetes deployment
kubectl apply -f k8s/skills-deployment.yaml

# ConfigMap for skills
kubectl create configmap arifos-skills \
  --from-file=skill_templates.yaml
```

---

## 🔄 Skill Deployment Lifecycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  DEVELOP │ →  │   TEST   │ →  │  DEPLOY  │ →  │  MONITOR │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
• Edit YAML      • Unit tests    • Production    • Metrics
• Validate       • Integration   • Scaling       • Alerts
• Version        • Constitutional• Updates       • Audit
```

### Development
```bash
# Edit skill template
vim skill_templates.yaml

# Validate schema
python -m L2_SKILLS.validate skill_templates.yaml
```

### Testing
```bash
# Run skill tests
pytest L2_SKILLS/tests/

# Constitutional compliance test
pytest L2_SKILLS/tests/test_constitutional.py -v
```

### Deployment
```bash
# Deploy to staging
./deploy.sh staging

# Deploy to production
./deploy.sh production
```

### Monitoring
```bash
# Check skill usage
arifos-cli skills stats

# View audit log
arifos-cli vault logs --skill=f2_truth_verification
```

---

## 📊 Deployment Checklist

### Pre-Deployment
- [ ] Skills validated (`validate_skills.py`)
- [ ] Constitutional floors tested
- [ ] Environment variables configured
- [ ] Logging configured
- [ ] Backup strategy in place

### Deployment
- [ ] Deploy to staging first
- [ ] Run integration tests
- [ ] Deploy to production
- [ ] Verify health checks
- [ ] Update documentation

### Post-Deployment
- [ ] Monitor error rates
- [ ] Check constitutional compliance
- [ ] Review audit logs
- [ ] Gather feedback
- [ ] Plan updates

---

## 🛠️ Troubleshooting

### Issue: Skills not loading
```bash
# Check path
export ARIFOS_SKILLS_PATH="/absolute/path/to/L2_SKILLS"

# Verify YAML syntax
python -c "import yaml; yaml.safe_load(open('skill_templates.yaml'))"
```

### Issue: Constitutional validation failing
```bash
# Check floor thresholds
arifos-cli config get f2_truth_threshold

# Run diagnostics
python -m L2_SKILLS.diagnose
```

### Issue: MCP integration not working
```bash
# Check MCP server status
python -m mcp --status

# Verify client config
cat ~/.cursor/mcp.json
```

---

## 🔗 Next Steps

- **L3_WORKFLOW/** — Add documented sequences for complex deployments
- **L4_TOOLS/** — Connect to production MCP server
- **ROADMAP/** — View v55.0+ deployment plans

---

## 👑 Authority

**Sovereign:** Muhammad Arif bin Fazil  
**Version:** v54.1-SEAL  
**Creed:** DITEMPA BUKAN DIBERI
