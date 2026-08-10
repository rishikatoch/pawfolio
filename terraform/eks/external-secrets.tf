data "aws_iam_policy_document" "external_secrets" {
  statement {
    effect = "Allow"

    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret"
    ]

    resources = [
      "arn:aws:secretsmanager:us-west-2:977574653467:secret:pawfolio/app-*"
    ]
  }
}

resource "aws_iam_policy" "external_secrets" {
  name        = "${var.cluster_name}-external-secrets"
  description = "Allow External Secrets Operator to read Pawfolio secrets"

  policy = data.aws_iam_policy_document.external_secrets.json

  tags = {
    Name        = "${var.cluster_name}-external-secrets"
    Project     = "Pawfolio"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

module "external_secrets_pod_identity" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "~> 2.8"

  name = "external-secrets"

  additional_policy_arns = {
    secrets_manager = aws_iam_policy.external_secrets.arn
  }

  associations = {
    external_secrets = {
      cluster_name    = module.eks.cluster_name
      namespace       = "external-secrets"
      service_account = "external-secrets"
    }
  }

  tags = {
    Project     = "Pawfolio"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
