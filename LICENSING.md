# arifOS Licensing Model

**This document resolves the CC0 ↔ AGPL-3.0 question definitively.**

arifOS operates as two legally distinct repositories with complementary licenses:

---

## Two-Repo, Two-License Architecture

### The Mind — `ariffazil/arifOS` — CC0 1.0 Universal

**What it contains:**
- Constitutional specification (`STANDARD.v1.md`)
- Machine-readable governance policy (`arifos.standard.v1.json`)
- Theory and doctrine (`000_CONSTITUTION.md`, `000_THEORY.md`, `WHITEPAPER.md`)
- Landing content and community documentation

**What this means:**
- The standard is in the public domain. No attribution required.
- Anyone may implement, fork, translate, or embed the standard without restriction.
- Downstream implementations may be any license — proprietary, open, or mixed.
- This is intentional: a governance standard that restricts reuse would be self-defeating.

**Repository:** https://github.com/ariffazil/arifOS
**License file:** CC0 1.0 Universal

---

### The Body — `ariffazil/arifosmcp` — AGPL-3.0-only

**What it contains:**
- Reference implementation of the arifOS Standard (Python runtime)
- FastMCP server with 11 mega-tools, 13 constitutional floors
- Production infrastructure (Docker, Prometheus, Grafana)
- All executable code under `arifosmcp/` directory

**What this means:**
- The reference implementation is open-source under AGPL-3.0.
- If you run a modified version of this server as a network service, you must release your modifications.
- Embedding this code in a proprietary system that runs as a service requires AGPL compliance.
- This is intentional: the reference implementation should stay open to benefit the community.

**Repository:** https://github.com/ariffazil/arifosmcp
**License file:** GNU Affero General Public License v3

---

## Layered Summary

| Artifact | Repository | License | Can I use freely? |
|----------|------------|---------|-------------------|
| `STANDARD.v1.md` | arifOS (Mind) | CC0 | Yes — public domain |
| `arifos.standard.v1.json` | arifOS (Mind) | CC0 | Yes — public domain |
| `WHITEPAPER.md` | arifOS (Mind) | CC0 | Yes — public domain |
| `000_CONSTITUTION.md` | arifOS (Mind) | CC0 | Yes — public domain |
| MCP server runtime | arifosmcp (Body) | AGPL-3.0 | Yes, with copyleft obligation |
| Docker images | arifosmcp (Body) | AGPL-3.0 | Yes, with copyleft obligation |
| Grafana dashboards | arifosmcp (Body) | AGPL-3.0 | Yes, with copyleft obligation |

---

## For Implementers

**You want to build your own AI governance layer based on arifOS:**
→ Use `STANDARD.v1.md` and `arifos.standard.v1.json` freely (CC0). Build in any language, any license.

**You want to run the reference server:**
→ Use `arifosmcp` under AGPL-3.0. Modifications to the server must remain open-source if offered as a network service.

**You want to embed arifOS constitutional logic in a closed product:**
→ Implement the CC0 standard yourself, or contact the author for a commercial license to the runtime.

---

## Contact

**Arif Fazil** — author and sovereign architect
GitHub: [@ariffazil](https://github.com/ariffazil)
Site: https://arifos.arif-fazil.com

*Last updated: 2026-03-22*
