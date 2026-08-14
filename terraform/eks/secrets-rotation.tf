data "aws_caller_identity" "current" {}

data "aws_secretsmanager_secret" "pawfolio_app" {
  name = "pawfolio/app"
}

data "archive_file" "secrets_rotation" {
  type        = "zip"
  source_file = "${path.module}/secrets-rotation/lambda_function.py"
  output_path = "${path.module}/secrets-rotation/lambda_function.zip"
}

data "aws_iam_policy_document" "secrets_rotation_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole",
    ]
  }
}

resource "aws_iam_role" "secrets_rotation" {
  name = "${var.cluster_name}-secrets-rotation"

  assume_role_policy = data.aws_iam_policy_document.secrets_rotation_assume_role.json

  tags = {
    Name        = "${var.cluster_name}-secrets-rotation"
    Project     = "Pawfolio"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

data "aws_iam_policy_document" "secrets_rotation" {
  statement {
    effect = "Allow"

    actions = [
      "secretsmanager:DescribeSecret",
      "secretsmanager:GetSecretValue",
      "secretsmanager:PutSecretValue",
      "secretsmanager:UpdateSecretVersionStage",
    ]

    resources = [
      data.aws_secretsmanager_secret.pawfolio_app.arn,
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:*",
    ]
  }
}

resource "aws_iam_role_policy" "secrets_rotation" {
  name = "${var.cluster_name}-secrets-rotation"
  role = aws_iam_role.secrets_rotation.id

  policy = data.aws_iam_policy_document.secrets_rotation.json
}

resource "aws_lambda_function" "secrets_rotation" {
  # checkov:skip=CKV_AWS_116:DLQ is not applicable to this Secrets Manager rotation Lambda.
  # checkov:skip=CKV_AWS_117:Lambda only accesses AWS Secrets Manager APIs and does not require VPC resources.
  # checkov:skip=CKV_AWS_272:Lambda code signing is outside the scope of this project.
  # checkov:skip=CKV_AWS_50:X-Ray tracing is not required for this lightweight rotation function.

  function_name = "${var.cluster_name}-secrets-rotation"
  role          = aws_iam_role.secrets_rotation.arn

  runtime = "python3.12"
  handler = "lambda_function.lambda_handler"

  filename         = data.archive_file.secrets_rotation.output_path
  source_code_hash = data.archive_file.secrets_rotation.output_base64sha256

  timeout     = 30
  memory_size = 128

  reserved_concurrent_executions = 5

  description = "Rotates the Pawfolio application SECRET_KEY in AWS Secrets Manager"

  tags = {
    Name        = "${var.cluster_name}-secrets-rotation"
    Project     = "Pawfolio"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "secrets_manager_rotation" {
  statement_id   = "AllowSecretsManagerRotation"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.secrets_rotation.function_name
  principal      = "secretsmanager.amazonaws.com"
  source_arn     = data.aws_secretsmanager_secret.pawfolio_app.arn
  source_account = data.aws_caller_identity.current.account_id
}

resource "aws_secretsmanager_secret_rotation" "pawfolio_app" {
  secret_id           = data.aws_secretsmanager_secret.pawfolio_app.id
  rotation_lambda_arn = aws_lambda_function.secrets_rotation.arn

  rotation_rules {
    automatically_after_days = 30
  }

  depends_on = [
    aws_lambda_permission.secrets_manager_rotation,
  ]
}
