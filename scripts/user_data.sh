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
    docker-compose-v2 \
    git \
    curl \
    unzip

echo "Installing AWS CLI v2..."

cd /tmp

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip

unzip -q awscliv2.zip

./aws/install

aws --version

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

chmod +x scripts/generate_env.sh
chmod +x scripts/deploy.sh
chmod +x scripts/healthcheck.sh
EOF

echo "Generating environment file..."
"$APP_DIR/scripts/generate_env.sh"

echo "Deploying Pawfolio..."

sudo -u ubuntu bash <<EOF
cd "$APP_DIR"
./scripts/deploy.sh
EOF

echo "=========================================="
echo "Bootstrap Completed Successfully"
echo "=========================================="