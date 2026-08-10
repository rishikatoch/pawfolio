#!/usr/bin/env bash

set -u

REGION="us-west-2"
CLUSTER_NAME="pawfolio-eks"
TF_DIR="terraform/eks"
ARGO_APP="pawfolio"
ARGO_NAMESPACE="argocd"

echo "=============================================="
echo " Pawfolio EKS Teardown"
echo "=============================================="

# --------------------------------------------------
# Helpers
# --------------------------------------------------

fail() {
    echo
    echo "❌ ERROR: $1"
    exit 1
}

info() {
    echo
    echo "▶ $1"
}

# --------------------------------------------------
# Check Terraform state
# --------------------------------------------------

info "Checking Terraform state..."

STATE_LIST=$(terraform -chdir="$TF_DIR" state list 2>/dev/null || true)

if [ -z "$STATE_LIST" ]; then
    echo "Terraform EKS state is already empty."
    echo "Nothing to destroy."
    exit 0
fi

echo "$STATE_LIST"

# --------------------------------------------------
# Get VPC ID
# --------------------------------------------------

VPC_ID=$(terraform -chdir="$TF_DIR" output -raw vpc_id 2>/dev/null || true)

if [ -z "$VPC_ID" ]; then
    fail "Could not determine VPC ID from Terraform."
fi

echo "VPC: $VPC_ID"

# --------------------------------------------------
# Check whether EKS exists
# --------------------------------------------------

info "Checking EKS cluster..."

if aws eks describe-cluster \
    --region "$REGION" \
    --name "$CLUSTER_NAME" >/dev/null 2>&1; then

    echo "EKS cluster exists."

    # --------------------------------------------------
    # Configure kubectl
    # --------------------------------------------------

    info "Updating kubeconfig..."

    aws eks update-kubeconfig \
        --region "$REGION" \
        --name "$CLUSTER_NAME" >/dev/null

    # --------------------------------------------------
    # Delete Argo CD Application
    # --------------------------------------------------

    info "Checking Argo CD Application..."

    if kubectl get application "$ARGO_APP" \
        -n "$ARGO_NAMESPACE" >/dev/null 2>&1; then

        echo "Deleting Argo CD Application..."

        kubectl delete application "$ARGO_APP" \
            -n "$ARGO_NAMESPACE" \
            --wait=true

        echo "Argo CD Application deleted."
    else
        echo "Argo CD Application not found."
    fi

else
    echo "EKS cluster does not exist."
fi

# --------------------------------------------------
# Wait for AWS Load Balancers
# --------------------------------------------------

info "Waiting for AWS Load Balancers to disappear..."

MAX_ATTEMPTS=30
ATTEMPT=1

while [ "$ATTEMPT" -le "$MAX_ATTEMPTS" ]; do

    CLASSIC_COUNT=$(
        aws elb describe-load-balancers \
            --region "$REGION" \
            --query "LoadBalancerDescriptions[?VPCId=='$VPC_ID'] | length(@)" \
            --output text 2>/dev/null || echo "0"
    )

    ELBV2_COUNT=$(
        aws elbv2 describe-load-balancers \
            --region "$REGION" \
            --query "LoadBalancers[?VpcId=='$VPC_ID'] | length(@)" \
            --output text 2>/dev/null || echo "0"
    )

    echo "Attempt $ATTEMPT/$MAX_ATTEMPTS — Classic ELB: $CLASSIC_COUNT, ELBv2: $ELBV2_COUNT"

    if [ "$CLASSIC_COUNT" = "0" ] && [ "$ELBV2_COUNT" = "0" ]; then
        echo "No AWS Load Balancers remain."
        break
    fi

    if [ "$ATTEMPT" -eq "$MAX_ATTEMPTS" ]; then
        fail "Load Balancers still exist in VPC $VPC_ID."
    fi

    sleep 10
    ATTEMPT=$((ATTEMPT + 1))
done


# --------------------------------------------------
# Terraform destroy
# --------------------------------------------------

info "Running Terraform destroy..."

if ! terraform -chdir="$TF_DIR" destroy -auto-approve; then
    fail "Terraform destroy failed."
fi

# --------------------------------------------------
# Verify Terraform state
# --------------------------------------------------

info "Verifying Terraform state..."

REMAINING_STATE=$(terraform -chdir="$TF_DIR" state list 2>/dev/null || true)

if [ -n "$REMAINING_STATE" ]; then
    echo "$REMAINING_STATE"
    fail "Terraform state still contains resources."
fi

echo "Terraform state is empty."

# --------------------------------------------------
# Verify EKS
# --------------------------------------------------

info "Verifying EKS cluster is gone..."

if aws eks describe-cluster \
    --region "$REGION" \
    --name "$CLUSTER_NAME" >/dev/null 2>&1; then

    fail "EKS cluster still exists."

fi

echo "EKS cluster is gone."

# --------------------------------------------------
# Verify VPC
# --------------------------------------------------

info "Verifying VPC is gone..."

if aws ec2 describe-vpcs \
    --region "$REGION" \
    --vpc-ids "$VPC_ID" >/dev/null 2>&1; then

    fail "VPC $VPC_ID still exists."

fi

echo "VPC is gone."

echo
echo "=============================================="
echo " ✅ Pawfolio EKS teardown completed"
echo "=============================================="
