#!/bin/bash
set -euo pipefail

echo "=========================================="
echo "Generating .env from AWS Parameter Store"
echo "=========================================="

APP_DIR="/opt/pawfolio"

# Ensure AWS CLI is installed
if ! command -v aws >/dev/null 2>&1; then
    echo "ERROR: AWS CLI is not installed."
    exit 1
fi

echo "Retrieving AWS Region..."

TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
    -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
    -s)

AWS_REGION=$(curl \
    -H "X-aws-ec2-metadata-token: $TOKEN" \
    -s http://169.254.169.254/latest/dynamic/instance-identity/document \
    | grep region \
    | awk -F\" '{print $4}')

echo "AWS Region: $AWS_REGION"

echo "Reading secrets from AWS Systems Manager..."

SECRET_KEY=$(aws ssm get-parameter \
    --name "/pawfolio/SECRET_KEY" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text \
    --region "$AWS_REGION")

DATABASE_URL=$(aws ssm get-parameter \
    --name "/pawfolio/DATABASE_URL" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text \
    --region "$AWS_REGION")

POSTGRES_USER=$(aws ssm get-parameter \
    --name "/pawfolio/POSTGRES_USER" \
    --query "Parameter.Value" \
    --output text \
    --region "$AWS_REGION")

POSTGRES_PASSWORD=$(aws ssm get-parameter \
    --name "/pawfolio/POSTGRES_PASSWORD" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text \
    --region "$AWS_REGION")

POSTGRES_DB=$(aws ssm get-parameter \
    --name "/pawfolio/POSTGRES_DB" \
    --query "Parameter.Value" \
    --output text \
    --region "$AWS_REGION")

echo "Creating .env file..."

cat > "$APP_DIR/.env" <<EOF
SECRET_KEY=$SECRET_KEY
DATABASE_URL=$DATABASE_URL

POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=$POSTGRES_DB
EOF

chmod 600 "$APP_DIR/.env"
chown ubuntu:ubuntu "$APP_DIR/.env"

echo ".env created successfully."