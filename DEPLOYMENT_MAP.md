# arifOS Deployment Map (Unified)

Single source of truth for what deploys where, which workflow owns it, and how to debug when public sites drift.

---

## Canonical Surfaces

| Surface | Public URL | Platform | Source Path | Workflow Owner |
|:--|:--|:--|:--|:--|
| Docs site (APPS) | `https://arifos.arif-fazil.com` | GitHub Pages | `sites/docs/**` | `.github/workflows/deploy-sites.yml` |
| MCP runtime | `https://arifosmcp.arif-fazil.com` | VPS (Coolify) | `aaa_mcp/**`, `arifos_aaa_mcp/**`, `core/**`, `aclip_cai/**` | `.github/workflows/deploy.yml` |
| VPS legacy deploy path | VPS host direct | VPS SSH deploy | broad repo changes (non-doc) | `.github/workflows/deploy-vps.yml` |
| Constitutional dashboard | `https://arifosmcp-truth-claim.pages.dev` | Cloudflare Pages | `run_evals.py`, `tests/mcp_live/golden/**`, `aclip_cai/core/eval/**` | `.github/workflows/deploy-cloudflare.yml` |

---

## Ownership Rules (No Chaos)

- Docs production domain `arifos.arif-fazil.com` is owned by `deploy-sites.yml` only.
- MCP production domain `arifosmcp.arif-fazil.com` is owned by `deploy.yml` (Coolify webhook) primarily.
- Dashboard domain `arifosmcp-truth-claim.pages.dev` is owned by `deploy-cloudflare.yml` only.
- `sites/docs/docs/**` is canonical docs source. Root `docs/**` is reference content and not the Docusaurus publish source.

---

## Trigger Matrix

### 1) Docs (GitHub Pages)

- Workflow: `.github/workflows/deploy-sites.yml`
- Trigger: push to `main`/`master` (all changes) + manual dispatch
- Build root: `sites/docs`
- Build command: `npm ci && npm run build`
- Publish target: GitHub Pages artifact + CNAME `arifos.arif-fazil.com`
- Post-check: public smoke test on `/intro` and `/architecture`

### 2) MCP Server (VPS)

- Workflow: `.github/workflows/deploy.yml`
- Trigger: push to `main` with backend/runtime path filters
- Deploy mode: Coolify webhook (if secret configured)
- Health verify: `https://arifosmcp.arif-fazil.com/health`

### 3) VPS Legacy SSH Pipeline

- Workflow: `.github/workflows/deploy-vps.yml`
- Trigger: push to `main` with `paths-ignore` for docs/github metadata
- Deploy mode: SSH + `/opt/arifOS/deploy.sh`
- Note: Keep only if intentionally used. If Coolify is canonical, treat this as fallback and document accordingly.

### 4) Dashboard (Cloudflare)

- Workflow: `.github/workflows/deploy-cloudflare.yml`
- Trigger: push path filters + manual + schedule
- Deploy mode: Cloudflare Pages action

---

## Required Repo Settings

### GitHub Pages

- Settings -> Pages -> Source: `GitHub Actions`
- Environment `github-pages` must be available and not blocked unexpectedly
- Custom domain mapped: `arifos.arif-fazil.com`

### Secrets

- Coolify: `COOLIFY_WEBHOOK_URL`
- VPS SSH path (if used): `VPS_SSH_KEY`, `VPS_HOST`, `VPS_USER`
- Cloudflare: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`

---

## Why Docs Sometimes Did Not Update

Common causes:

1. Workflow path filters skipped run (fixed for docs by triggering on every push to `main/master`).
2. Pushed to non-default branch and expected production domain to update.
3. GitHub Pages source not set to `GitHub Actions`.
4. Workflow green but CDN/DNS propagation delay on custom domain.
5. Edited root `docs/**` while website actually builds from `sites/docs/docs/**`.

---

## Fast Recovery Runbook (Docs)

1. Check latest Actions run for `Deploy APPS site to GitHub Pages`.
2. If no run: ensure commit landed on `main` and workflow is enabled.
3. If failed build: run locally:

```bash
cd /c/Users/User/arifOS/sites/docs
npm ci
npm run build
```

4. If deploy succeeded but site stale: hard refresh, then wait 1-5 minutes for custom domain propagation.
5. If still stale: manually run workflow_dispatch for `deploy-sites.yml`.

---

## Local Validation Before Push

```bash
cd /c/Users/User/arifOS/sites/docs
npm ci
npm run build
```

If this passes, `deploy-sites.yml` should produce the same static artifact in CI.

---

## Recommended Next Tightening

- Choose one canonical VPS deploy path (`deploy.yml` Coolify **or** `deploy-vps.yml` SSH) and mark the other as fallback explicitly.
- Add a short badge block in `README.md` linking directly to the 3 deployment workflows.
- Keep this file updated whenever workflow triggers or domain ownership changes.
