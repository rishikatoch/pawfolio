#!/bin/bash
set -euo pipefail

APP_DIR="/opt/pawfolio"

cd "$APP_DIR"

echo "=========================================="
echo "Running Health Checks"
echo "=========================================="

echo
echo "Docker Service"
systemctl is-active docker

echo
echo "Containers"
docker compose -f docker-compose.prod.yml ps

echo
echo "Docker Processes"
docker ps

echo
echo "Application"

curl --fail http://localhost:5000

echo
echo "=========================================="
echo "Application Healthy"
echo "=========================================="