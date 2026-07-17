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

echo "Checking Docker Compose file..."

if [ ! -f "docker-compose.prod.yml" ]; then
    echo "ERROR: docker-compose.prod.yml not found!"
    exit 1
fi

echo "Waiting for Docker service..."

until docker info >/dev/null 2>&1; do
    echo "Docker is starting..."
    sleep 2
done

echo "Docker is ready."

echo "Stopping existing containers..."

docker compose -f docker-compose.prod.yml down || true

echo "Building Docker images..."

docker compose -f docker-compose.prod.yml build --no-cache

echo "Starting containers..."

docker compose -f docker-compose.prod.yml up -d

echo "Waiting for application to start..."

sleep 10

echo "Running health checks..."

chmod +x scripts/healthcheck.sh
./scripts/healthcheck.sh

echo "=========================================="
echo "Pawfolio Deployment Successful"
echo "=========================================="