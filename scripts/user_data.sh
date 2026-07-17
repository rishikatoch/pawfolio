#!/bin/bash
set -euxo pipefail

LOG_FILE="/var/log/pawfolio-bootstrap.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=========================================="
echo "Starting Pawfolio EC2 Bootstrap"
echo "=========================================="

export DEBIAN_FRONTEND=noninteractive

echo "Updating packages..."
apt-get update -y

echo "Installing required packages..."
apt-get install -y \
    docker.io \
    git \
    curl

echo "Starting Docker..."
systemctl enable docker
systemctl start docker

echo "Adding ubuntu user to docker group..."
usermod -aG docker ubuntu

APP_DIR="/opt/pawfolio"

echo "Creating application directory..."
mkdir -p "$APP_DIR"
chown -R ubuntu:ubuntu "$APP_DIR"

echo "Cloning Pawfolio repository..."

sudo -u ubuntu bash <<'EOF'
set -e

APP_DIR="/opt/pawfolio"
REPO_URL="https://github.com/rishikatoch/pawfolio.git"
BRANCH="main"

if [ ! -d "$APP_DIR/.git" ]; then
    git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"

chmod +x scripts/deploy.sh
chmod +x scripts/healthcheck.sh

./scripts/deploy.sh
EOF

echo "=========================================="
echo "Bootstrap Completed Successfully"
echo "=========================================="