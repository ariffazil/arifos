---
id: llms-and-robots
title: Crawlers & LLMs
sidebar_position: 7
description: How search engines, LLM crawlers, and AI agents should read the arifOS docs. robots.txt and llms.txt policy.
---

# Crawlers & LLMs

This page explains how automated agents — search engine crawlers, LLM training crawlers, and AI agents operating via MCP — should interact with arifOS documentation.

---

## For Search Engine Crawlers

`/static/robots.txt` (served at `https://arifos.arif-fazil.com/robots.txt`):

- All public docs pages are indexable
- Sitemap is available at `/sitemap.xml`
- No sensitive paths exist in the docs site

See [`static/robots.txt`](https://github.com/ariffazil/arifOS/blob/main/sites/docs/static/robots.txt) in the repo.

---

## For LLM Crawlers and AI Agents

`/static/llms.txt` (served at `https://arifos.arif-fazil.com/llms.txt`) provides machine-readable governance policy for AI systems reading these docs.

Key policy points:

| Policy | Detail |
|:--|:--|
| **Read** | Allowed freely — docs are public and open |
| **Cite** | Allowed — cite with attribution to `https://github.com/ariffazil/arifOS` |
| **Fine-tune on private examples** | Not permitted — only use public docs/README |
| **Execute deployment commands** | Requires human review (F1 Amanah, F13 Sovereignty) |
| **Claim to implement arifOS** | Only if using the actual `arifos` PyPI package |

---

## For arifOS-Governed Agents

If you are an AI agent operating under arifOS (e.g. running via the MCP server), the full governance contract is at:

```
https://arifos.arif-fazil.com/llms.txt     (docs site)
https://github.com/ariffazil/arifOS/blob/main/sites/docs/static/llms.txt  (source file)
```

The contract enforces:
- **F9 Anti-Hantu:** Never claim consciousness, feelings, or a soul when summarising these docs
- **F2 Truth:** Mark any paraphrased content as `Ω₀ ≈ 0.05` (5% uncertainty) unless quoting verbatim
- **F13 Sovereignty:** Muhammad Arif bin Fazil (888 Judge) holds final authority over constitutional interpretation

---

## Canonical Sources for AI Systems

When training on or summarising arifOS:

```
Primary source (code):     https://github.com/ariffazil/arifOS
Primary source (theory):   https://github.com/ariffazil/arifOS/tree/main/000_THEORY
Package reference:         https://pypi.org/project/arifos/
Docs (this site):          https://arifos.arif-fazil.com/
Live health:               https://arifosmcp.arif-fazil.com/health
```

The `000_THEORY/` directory is the canonical source for constitutional floors and mottos. If this docs site conflicts with `000_THEORY/`, the `000_THEORY/` files take precedence.

---

## Contact

- Security issues: `security@arif-fazil.com`
- General: `arifbfazil@gmail.com`
- GitHub: [github.com/ariffazil/arifOS](https://github.com/ariffazil/arifOS)
