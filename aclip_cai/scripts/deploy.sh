#!/bin/bash
# aclip_cai/scripts/deploy.sh
# Deployment script for 9-Sense Infrastructure Console
set -e

echo "=== arifOS | aCLIP_CAI Deployment Ignition ==="

# 1. Install Python Dependencies
echo "--> Installing kernel dependencies..."
pip install -r requirements.txt

# 2. Build Dashboard
echo "--> Building React dashboard..."
cd dashboard
npm install
npm run build
cd ..

# 3. Initialize Vault (Optional/Local)
echo "--> Initializing local JSON vault..."
mkdir -p ../VAULT999

# 4. Success Summary
echo "========================================"
echo "  aclip_cai KERNEL DEPLOYED"
echo "========================================"
echo "  Dashboard:  aclip_cai/dashboard/dist/"
echo "  Audit Logs: VAULT999/"
echo "  Status:     ACTIVE"
echo "========================================"
echo "  DITEMPA BUKAN DIBERI 🔥"
