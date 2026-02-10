# MCP Registry Submission Guide

Official guide for submitting AAA MCP to the Model Context Protocol Registry.

## Prerequisites (✅ Completed)

- [x] Package published to PyPI (`pip install arifos`)
- [x] `mcpName` added to `pyproject.toml`
- [x] `server.json` created with official schema
- [x] GitHub repository public

## Submission Steps

### Step 1: Install MCP Publisher CLI

**Option A: Homebrew (Mac/Linux)**
```bash
brew install modelcontextprotocol/tap/mcp-publisher
```

**Option B: Download Binary**
```bash
# Download latest release from:
# https://github.com/modelcontextprotocol/registry/releases

# Or use curl (example for Linux x64):
curl -L -o mcp-publisher https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher-linux-amd64
chmod +x mcp-publisher
```

**Option C: Build from Source**
```bash
git clone https://github.com/modelcontextprotocol/registry.git
cd registry
make publisher
# Binary will be at ./bin/mcp-publisher
```

### Step 2: Authenticate

```bash
# Login with GitHub (for io.github.ariffazil/* namespace)
mcp-publisher login github

# Or use DNS verification (for custom domain)
# mcp-publisher login dns
```

This will open a browser for GitHub OAuth authorization.

### Step 3: Submit to Registry

```bash
# From the repo root
mcp-publisher publish --file server.json
```

**Expected output:**
```
✓ Validated server.json
✓ Authenticated as ariffazil
✓ Namespace verified: io.github.ariffazil
✓ Package found on PyPI: arifos v60.0.0
✓ Published to registry: io.github.ariffazil/aaa-mcp
✓ Live at: https://registry.modelcontextprotocol.io/servers/io.github.ariffazil/aaa-mcp
```

### Step 4: Verify Submission

Visit: **https://registry.modelcontextprotocol.io/servers/io.github.ariffazil/aaa-mcp**

Or search for "AAA MCP" on the registry homepage.

---

## Alternative: GitHub Actions (Automated)

The workflow `.github/workflows/publish-mcp-registry.yml` is configured to validate `server.json` on every release.

To trigger:
1. Create a new release on GitHub
2. The workflow will validate and prepare the submission
3. Manual approval required for actual registry push (pending MCP Registry API availability)

---

## Troubleshooting

### "mcpName not found in package"
- Ensure `mcpName = "io.github.ariffazil/aaa-mcp"` is in `pyproject.toml` under `[project]`
- Republish to PyPI: `pip install build twine && python -m build && twine upload dist/*`

### "Namespace not verified"
- Must authenticate with GitHub account that owns `ariffazil` username
- Run `mcp-publisher login github` again

### "Version mismatch"
- Ensure `server.json` version matches PyPI version
- Update both files to same version number

### "Schema validation failed"
- Check `$schema` URL is correct: `https://registry.modelcontextprotocol.io/schema/2025-12-11/server.schema.json`
- Validate JSON syntax: `python -c "import json; json.load(open('server.json'))"`

---

## Post-Submission Checklist

- [ ] Server appears in registry search
- [ ] `pip install arifos` works for users
- [ ] `python -m aaa_mcp` launches successfully
- [ ] Health endpoint responds: https://aaamcp.arif-fazil.com/health
- [ ] Documentation site loads: https://arifos.arif-fazil.com

---

## Registry Links

- **Registry Home:** https://registry.modelcontextprotocol.io
- **Your Server (after publish):** https://registry.modelcontextprotocol.io/servers/io.github.ariffazil/aaa-mcp
- **Publisher Docs:** https://modelcontextprotocol.io/registry/quickstart
- **Schema Reference:** https://github.com/modelcontextprotocol/registry/tree/main/schema

---

*DITEMPA BUKAN DIBERI* — Forged for the Registry. 🔥
