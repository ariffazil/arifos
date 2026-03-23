# ============================================================
# ARIFOS AGI STACK - SECURITY SETUP COMPLETE
# ============================================================

## 📁 Files Created

| File | Purpose | Location |
|------|---------|----------|
| `.env` | All secrets (API keys, passwords) | `/root/agi-stack/.env` |
| `docker-compose.lab.yml` | Full privileges for private/VPN use | `/root/agi-stack/docker-compose.lab.yml` |
| `docker-compose.public.yml` | Minimal privileges for internet | `/root/agi-stack/docker-compose.public.yml` |
| `rotate-keys.sh` | List of exposed keys to rotate | `/root/agi-stack/rotate-keys.sh` |

---

## 🔐 Security Comparison

### LAB MODE (docker-compose.lab.yml)
**Use when:** VPS is on private network/VPN only

| Feature | Setting | Risk |
|---------|---------|------|
| privileged | `true` | ⚠️ Container can access host hardware |
| Host mount | `/:/host:rw` | ⚠️ Full filesystem read/write |
| Docker socket | Mounted | ⚠️ Can control all containers |
| Ports | `0.0.0.0:50001` | ⚠️ Exposed to all interfaces |
| Capabilities | `ALL` | ⚠️ All Linux capabilities |

### PUBLIC MODE (docker-compose.public.yml)
**Use when:** VPS is internet-facing

| Feature | Setting | Risk |
|---------|---------|------|
| privileged | `false` | ✅ Standard container isolation |
| Host mount | `/workspace` only | ✅ Limited directory access |
| Docker socket | NOT mounted | ✅ Cannot control containers |
| Ports | `127.0.0.1:50001` | ✅ Localhost only (needs proxy) |
| Capabilities | Default only | ✅ Minimal privileges |

---

## 🚀 Usage

### Option 1: Lab Mode (Private Network)
```bash
cd /root/agi-stack
docker compose -f docker-compose.lab.yml up -d
```

### Option 2: Public Mode (Internet)
```bash
cd /root/agi-stack
# 1. Setup SSL certificates first
mkdir -p /opt/ssl-certs /opt/nginx-config
# 2. Add your SSL certs to /opt/ssl-certs/
# 3. Create nginx config at /opt/nginx-config/default.conf
# 4. Start services
docker compose -f docker-compose.public.yml up -d
```

---

## 🔑 API Key Rotation (CRITICAL!)

All API keys exposed in chat are compromised. Run:
```bash
/root/agi-stack/rotate-keys.sh
```

Then visit each provider to generate new keys and update `.env`

---

## 📊 Resource Allocation (8GB RAM, 2 vCPU)

### Lab Mode
| Service | Memory | CPU | Privileges |
|---------|--------|-----|------------|
| Agent Zero | 4GB | 1.5 cores | Full system access |
| Qdrant | 1.5GB | Shared | Standard |
| Browserless | 2GB | Shared | Standard |
| n8n | 1GB | Shared | Standard |
| Netdata | 512MB | Shared | Host PID |
| Portainer | 512MB | Shared | Docker socket |

### Public Mode
Same memory, but NO host access, NO Docker control

---

## 🛡️ Security Checklist

- [ ] Rotate all API keys (run rotate-keys.sh)
- [ ] Change ROOT_PASSWORD in .env
- [ ] Change N8N_BASIC_AUTH_PASSWORD in .env
- [ ] Change BROWSERLESS_TOKEN in .env
- [ ] Set file permissions: `chmod 600 .env`
- [ ] For public mode: Setup HTTPS reverse proxy
- [ ] For public mode: Configure firewall (ufw)
- [ ] Clear shell history: `history -c && history -w`
- [ ] Delete old keys from provider dashboards

---

## 📞 Access URLs (Lab Mode)

| Service | URL |
|---------|-----|
| Agent Zero | http://72.62.71.199:50001 |
| n8n | http://72.62.71.199:5678 |
| Portainer | http://72.62.71.199:9000 |
| Netdata | http://72.62.71.199:19999 |
| Browserless | http://72.62.71.199:3000 |

---

## 🎯 Next Steps

1. **Immediate:** Rotate API keys
2. **Today:** Choose lab or public mode
3. **This week:** Setup HTTPS for public mode
4. **Ongoing:** Monitor with Netdata

---

## 🆘 Emergency Commands

```bash
# Stop all services
docker compose -f docker-compose.lab.yml down

# View logs
docker logs -f agentzero

# Restart single service
docker compose -f docker-compose.lab.yml restart agentzero

# Check resource usage
docker stats
```

---

## 📚 References

- Agent Zero Docs: https://github.com/agent0ai/agent-zero
- Docker Security: https://docs.docker.com/engine/security/
- OpenCode CLI: https://opencode.ai/docs/cli/

---

**Status:** ✅ Security configuration complete
**Date:** 2026-02-09
**Version:** 1.0
