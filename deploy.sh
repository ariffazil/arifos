#!/bin/bash
# This script automates the deployment of the arifOS MCP application using Docker.
# It is triggered by the webhook listener.
set -e

# Navigate to the application directory
cd /root/arifOS

echo ">>> Deployment started at $(date)"

# --- Step 1: Pull the latest code ---
echo ">>> Pulling latest changes from Git repository..."
git fetch origin main
git reset --hard origin/main
echo ">>> Git pull complete."

# --- Step 2: Build and restart the Docker service ---
echo ">>> Building and restarting Docker service using docker-compose.vps.yml..."
# Build the new image from the updated code.
docker-compose -f docker-compose.vps.yml build

# Stop the old container and start the new one in detached mode.
# Docker Compose automatically handles recreating only the services whose image has changed.
docker-compose -f docker-compose.vps.yml up -d
echo ">>> Docker service restarted successfully."

# --- Step 3: Clean up old resources ---
echo ">>> Pruning old Docker images to save space..."
# The -f flag forces the removal of dangling images without prompting.
docker image prune -f
echo ">>> Pruning complete."

echo ">>> Deployment finished successfully at $(date)"
