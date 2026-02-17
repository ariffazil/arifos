# arifOS MCP Server

This repository contains the source code for the arifOS MCP (Master Control Program) server.

It is configured with a fully automated, Docker-based deployment pipeline.

---

## Automated Deployment Architecture

This project uses a secure, automated CI/CD pipeline to deploy changes. The architecture is as follows:

1.  **Git Push**: A developer pushes a commit to the `main` branch of this GitHub repository.
2.  **Webhook Trigger**: GitHub sends a secure POST request (a webhook) to the configured endpoint on the VPS.
3.  **Webhook Listener Service**: A `systemd` service on the VPS (`arifos-webhook.service`) runs the `webhook_listener.py` script, which securely listens for this webhook.
4.  **Deployment Script**: Upon receiving a valid webhook for the `main` branch, the listener executes the `deploy.sh` script.
5.  **Docker-Based Deployment**: The `deploy.sh` script uses `docker-compose` to:
    *   Pull the latest code from the `main` branch.
    *   Build a new, updated Docker image containing the application.
    *   Gracefully restart the `arifosmcp` service with the new image.
    *   Prune old, unused Docker images to save disk space.

This ensures that any push to the `main` branch is automatically and safely deployed to production.

---

## How It Runs

The application itself is defined in the `docker-compose.vps.yml` file and runs as a Docker container.

*   **Entrypoint**: The container runs the `start-trinity.sh` script.
*   **Services**: This script starts the `aaa_mcp` application, which includes both an HTTP server and a Server-Sent Events (SSE) server for real-time communication.
*   **Networking**: The application ports (`8080` and `8089` inside the container) are exposed only to the host machine (`127.0.0.1`) on ports `8888` and `8889` for security. An external web server like Nginx can be used to expose these to the public if needed.

## Configuration

*   **Webhook Secret**: The `GITHUB_WEBHOOK_SECRET` is managed securely. It is loaded via the `/root/arifOS/.env` file by the `arifos-webhook.service`. This file is intentionally not committed to the repository.

---
### Manual Service Setup (for reference)

The webhook listener service is managed by `systemd`. The configuration is located at `/root/arifos-webhook.service` and contains the following:

```ini
[Unit]
Description=GitHub Webhook Listener for arifOS MCP
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/arifOS
# This line securely loads environment variables from the specified file.
EnvironmentFile=/root/arifOS/.env
ExecStart=/usr/bin/python3 /root/arifOS/webhook_listener.py
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
