# arif-fazil-sites — APPS Only (arifOS)

**Location:** `arifOS/arif-fazil-sites/`  
**Domain:** `arifos.arif-fazil.com`  
**Hosting:** GitHub Pages  
**DNS:** Cloudflare  
**Motto:** *DITEMPA BUKAN DIBERI* — Forged, Not Given

---

## 🏛️ Trinity Architecture (Split Repos)

| Site | Domain | Repository | Hosting |
|------|--------|------------|---------|
| **HUMAN** | `arif-fazil.com` | `ariffazil` | Separate |
| **THEORY** | `apex.arif-fazil.com` | `APEX-THEORY` | Separate |
| **APPS** | `arifos.arif-fazil.com` | `arifOS` (this) | ✅ **GitHub Pages** |

---

## 🚀 Deployment Architecture

```
User → arifos.arif-fazil.com → Cloudflare DNS → GitHub Pages → Site loads
```

| Component | Provider | Purpose |
|-----------|----------|---------|
| **Build & Host** | GitHub Pages | Compiles React, serves static files |
| **DNS** | Cloudflare | Routes domain to GitHub Pages |
| **CDN** | GitHub Pages | Global edge caching |

---

## 📁 Directory Structure

```
arif-fazil-sites/
├── APPS/               # arifOS Application (React + Vite)
│   ├── src/            # React components
│   ├── public/         # Static assets
│   │   ├── CNAME       # ← Custom domain config for GitHub Pages
│   │   ├── robots.txt
│   │   ├── llms.txt
│   │   └── llms.json
│   └── dist/           # Build output (generated)
└── shared/             # Shared assets (reference only)
```

---

## 🛠️ Setup Steps

### 1. Enable GitHub Pages (One-time setup)

Go to: `https://github.com/ariffazil/arifOS/settings/pages`

| Setting | Value |
|---------|-------|
| **Source** | GitHub Actions |
| **Branch** | (not applicable with Actions) |

Click **Save**.

---

### 2. Configure Cloudflare DNS

Cloudflare Dashboard → `arif-fazil.com` → DNS → Records

Add this CNAME record:

| Type | Name | Target | TTL |
|------|------|--------|-----|
| CNAME | `arifos` | `ariffazil.github.io` | Auto |

> **Note:** If you're using Cloudflare's proxy (orange cloud icon), keep it **DNS-only** (gray cloud) for GitHub Pages, or configure properly for SSL.

---

### 3. Push to Deploy

```bash
cd C:\Users\User\arifOS
git add .
git commit -m "Configure GitHub Pages deployment for arifos.arif-fazil.com"
git push origin main
```

The workflow will:
1. Build the React app
2. Copy `CNAME` file (sets custom domain)
3. Create `404.html` for SPA routing
4. Deploy to GitHub Pages

---

## 🔄 Automatic Deployments

Any push to `main` that changes:
- `arif-fazil-sites/APPS/**`
- `.github/workflows/deploy-sites.yml`

Triggers automatic deployment (~2 minutes).

---

## 🛠️ Local Development

```bash
cd arif-fazil-sites/APPS
npm install
npm run dev
```

Build locally:
```bash
npm run build
# Output: dist/
```

---

## 🌐 SPA Routing on GitHub Pages

GitHub Pages doesn't natively support SPA (Single Page Application) routing. The workflow handles this by:

1. **Build** → Creates `dist/index.html`
2. **Copy** → `cp dist/index.html dist/404.html`
3. **Result** → Any unknown route serves `404.html` which loads the React app
4. **React Router** → Handles the route client-side

This allows URLs like `arifos.arif-fazil.com/tools/forge` to work on refresh.

---

## ✅ Setup Checklist

- [x] Remove nested `.git` folder
- [x] Create GitHub Pages deployment workflow
- [x] Create `CNAME` file for custom domain
- [ ] Enable GitHub Pages in repo settings (Source: GitHub Actions)
- [ ] Add Cloudflare DNS CNAME record
- [ ] Push to main to trigger first deployment
- [ ] Verify site loads at `arifos.arif-fazil.com`

---

## 🔗 Related Repos

| Repo | Path | Site | Hosting |
|------|------|------|---------|
| `ariffazil` | `C:\Users\User\ariffazil` | arif-fazil.com | (your choice) |
| `APEX-THEORY` | `C:\Users\User\APEX-THEORY` | apex.arif-fazil.com | (your choice) |
| `arifOS` | `C:\Users\User\arifOS` | arifos.arif-fazil.com | ✅ GitHub Pages |

---

*Part of arifOS — Constitutional AI Governance System*
