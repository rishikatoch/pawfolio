#!/bin/bash

set -e

echo "======================================"
echo "🚀 Starting Pawfolio Deployment..."
echo "======================================"

APP_DIR="/opt/pawfolio"

cd "$APP_DIR"

echo "📥 Pulling latest code..."
git pull origin main

echo "🔐 Fetching secrets from AWS SSM..."

SECRET_KEY=$(aws ssm get-parameter \
    --name "/pawfolio/SECRET_KEY" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text)

DATABASE_URL=$(aws ssm get-parameter \
    --name "/pawfolio/DATABASE_URL" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text)

POSTGRES_USER=$(aws ssm get-parameter \
    --name "/pawfolio/POSTGRES_USER" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text)

POSTGRES_PASSWORD=$(aws ssm get-parameter \
    --name "/pawfolio/POSTGRES_PASSWORD" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text)

POSTGRES_DB=$(aws ssm get-parameter \
    --name "/pawfolio/POSTGRES_DB" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text)

echo "📝 Updating .env file..."

# Preserve existing Google OAuth credentials (if present)
EXISTING_GOOGLE_CLIENT_ID=$(grep "^GOOGLE_CLIENT_ID=" .env 2>/dev/null | cut -d '=' -f2-)
EXISTING_GOOGLE_CLIENT_SECRET=$(grep "^GOOGLE_CLIENT_SECRET=" .env 2>/dev/null | cut -d '=' -f2-)

cat > .env <<EOF
SECRET_KEY=$SECRET_KEY
DATABASE_URL=$DATABASE_URL

POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=$POSTGRES_DB

GOOGLE_CLIENT_ID=$EXISTING_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=$EXISTING_GOOGLE_CLIENT_SECRET
EOF

echo "🛑 Stopping existing containers..."
docker compose -f docker-compose.prod.yml down

echo "📥 Pulling latest Docker image from Amazon ECR..."
docker compose -f docker-compose.prod.yml pull

echo "🚀 Starting containers..."
docker compose -f docker-compose.prod.yml up -d

echo "⏳ Waiting for PostgreSQL to become ready..."

until docker exec pawfolio-db pg_isready -U "$POSTGRES_USER" >/dev/null 2>&1; do
    echo "Database is starting... waiting 5 seconds..."
    sleep 5
done

echo "✅ Database is ready."

echo "🗄️ Running database migrations..."

until docker exec pawfolio-app flask db upgrade; do
    echo "Migration failed. Retrying in 5 seconds..."
    sleep 5
done

echo "🧹 Cleaning unused Docker images..."
docker image prune -f

echo "======================================"
echo "✅ Pawfolio deployed successfully!"
echo "======================================"