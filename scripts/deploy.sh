#!/bin/bash
set -euo pipefail

APP_DIR="/opt/pawfolio"

echo "=========================================="
echo "Starting Pawfolio Deployment"
echo "=========================================="

cd "$APP_DIR"

echo "Updating repository..."

git fetch origin
git reset --hard origin/main

echo "Checking environment file..."

if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    exit 1
fi

echo "Stopping existing containers..."

docker compose -f docker-compose.prod.yml down || true

echo "Building latest image..."

docker compose -f docker-compose.prod.yml build

echo "Starting containers..."

docker compose -f docker-compose.prod.yml up -d

echo "Running health checks..."

chmod +x scripts/healthcheck.sh
./scripts/healthcheck.sh

echo "=========================================="
echo "Pawfolio Deployment Successful"
echo "=========================================="