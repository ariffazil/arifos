# 🚀 arifOS DEPLOYMENT PROTOCOL (v2026.03.24)

## PHASE 000 — READINESS

1. **Unity Check:** Ensure you are in the root of the unified rifOS repo.
2. **Mirror Check:** The mirror universe AAA/ must be archived. 
3. **Site Map:** L3 Face is at sites/aaa/.

---

## PHASE 111 — CLOUDFLARE PAGES (L3 Face)

To go live at **aaa.arif-fazil.com**, create a new project in the CF Dashboard:

- **Project Name:** aa
- **Root Directory:** sites/aaa
- **Build Command:** (None)
- **Output Directory:** .
- **Custom Domain:** aa.arif-fazil.com

---

## PHASE 888 — VPS DEPLOYMENT (The Wire)

For routine code updates after unification:

`ash
cd /srv/arifos
git pull origin main
make fast-deploy
`

**888_HOLD Triggers:** 
- If substrate_policy.py is modified, run 	ests/test_hardened_toolchain.py before push.
- If credentials are exposed, the deployment will automatically **VOID**.

---

*Ditempa Bukan Diberi — Forged, Not Given*
