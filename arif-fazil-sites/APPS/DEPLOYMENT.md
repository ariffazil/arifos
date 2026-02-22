# Deployment Guide for arifOS APPS Site

This guide covers deploying the updated arifOS APPS site (`arifos.arif-fazil.com`) on a VPS with real‑time monitoring dashboard.

## Prerequisites

- VPS with Ubuntu 22.04/24.04
- DNS configured for `arifos.arif-fazil.com` (A/AAAA records pointing to VPS IP)
- SSL/TLS certificates (Let's Encrypt) already obtained
- Node.js 18+ and Python 3.12+ installed
- Nginx installed

## Step 1: Build the React App

```bash
# Clone the repository (if not already)
git clone https://github.com/ariffazil/arifOS.git
cd arifOS/arif-fazil-sites/APPS

# Install dependencies
npm install

# Build for production
npm run build
```

The built static files will be in `dist/`.

## Step 2: Deploy Static Files

Copy the built files to the web root:

```bash
sudo mkdir -p /var/www/arifos-apps
sudo cp -r dist/* /var/www/arifos-apps/
sudo chown -R www-data:www-data /var/www/arifos-apps
```

## Step 3: Configure Nginx

Copy the provided nginx configuration example and adjust paths as needed:

```bash
sudo cp nginx.conf.example /etc/nginx/sites-available/arifos-apps
sudo ln -sf /etc/nginx/sites-available/arifos-apps /etc/nginx/sites-enabled/
```

**Important:** Update the SSL certificate paths in the config if they differ from the example. The example assumes Let's Encrypt certificates at `/etc/letsencrypt/live/arifos.arif-fazil.com/`.

Test and reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Step 4: Set Up Dashboard Aggregator Service

The dashboard aggregator provides real‑time metrics and WebSocket updates. It must run as a background service.

1. Ensure Python dependencies are installed (should already be present in the arifOS virtual environment).

2. Copy the systemd service file:

```bash
sudo cp dashboard-aggregator.service.example /etc/systemd/system/dashboard-aggregator.service
```

3. Edit the service file to match your environment (adjust `WorkingDirectory`, `User`, `Group`, and `ExecStart` if needed).

4. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable dashboard-aggregator
sudo systemctl start dashboard-aggregator
sudo systemctl status dashboard-aggregator
```

## Step 5: Verify Deployment

- Visit `https://arifos.arif-fazil.com` – the site should load with updated content.
- Check the dashboard at `https://arifos.arif-fazil.com/#metrics` – the monitoring dashboard should show live metrics and connect via WebSocket (indicator should be green).
- Test API proxy: `curl https://arifos.arif-fazil.com/api/health` should return JSON health status.
- Verify WebSocket connectivity: you can inspect browser developer tools → Network → WS for a connection to `/api/ws`.

## Troubleshooting

### Dashboard Shows “Disconnected”
- Ensure the dashboard aggregator is running (`sudo systemctl status dashboard-aggregator`).
- Check that Nginx proxy passes WebSocket headers (the provided config includes `proxy_set_header Upgrade` and `Connection`).
- Verify firewall allows traffic on ports 443 (HTTPS) and 3002 (aggregator). The aggregator should only be accessible via Nginx (bound to `127.0.0.1:3002`).

### SSL Certificate Errors
- Confirm certificate paths in nginx config are correct.
- Ensure Let's Encrypt certificates are renewed (`sudo certbot renew`).

### Static Files Not Updating
- Clear browser cache.
- Verify the `dist/` folder was copied to the correct web root.

## Rollback

If issues arise, revert to the previous deployment:

1. Restore the previous static files (if backed up).
2. Restart Nginx: `sudo systemctl reload nginx`.
3. Stop the dashboard aggregator if needed: `sudo systemctl stop dashboard-aggregator`.

## Monitoring

- **Nginx logs:** `/var/log/nginx/access.log` and `error.log`
- **Dashboard aggregator logs:** `sudo journalctl -u dashboard-aggregator -f`
- **System metrics:** The dashboard itself provides real‑time monitoring.

---

**Deployment completed.** The arifOS APPS site now reflects the current state of the repository (v64.2.0 / v64.1.1‑GAGI) with real‑time dashboard functionality.