data "aws_caller_identity" "current" {}

data "aws_secretsmanager_secret" "pawfolio_app" {
  name = "pawfolio/app"
}

data "aws_iam_policy_document" "secrets_rotation_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole"
    ]
  }
}

resource "aws_iam_role" "secrets_rotation" {
  name               = "${var.cluster_name}-secrets-rotation"
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
      "secretsmanager:UpdateSecretVersionStage"
    ]

    resources = [
      data.aws_secretsmanager_secret.pawfolio_app.arn
    ]
  }
}

resource "aws_iam_role_policy" "secrets_rotation" {
  name = "${var.cluster_name}-secrets-rotation"
  role = aws_iam_role.secrets_rotation.id

  policy = data.aws_iam_policy_document.secrets_rotation.json
}

resource "aws_iam_role_policy_attachment" "secrets_rotation_logs" {
  role       = aws_iam_role.secrets_rotation.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "archive_file" "secrets_rotation" {
  type        = "zip"
  source_file = "${path.module}/secrets-rotation/lambda_function.py"
  output_path = "${path.module}/secrets-rotation/lambda_function.zip"
}

resource "aws_lambda_function" "secrets_rotation" {
  function_name = "${var.cluster_name}-secrets-rotation"
  role          = aws_iam_role.secrets_rotation.arn

  runtime = "python3.12"
  handler = "lambda_function.lambda_handler"

  filename         = data.archive_file.secrets_rotation.output_path
  source_code_hash = data.archive_file.secrets_rotation.output_base64sha256

  timeout     = 30
  memory_size = 128

  description = "Rotates the Pawfolio application SECRET_KEY in AWS Secrets Manager"

  tags = {
    Name        = "${var.cluster_name}-secrets-rotation"
    Project     = "Pawfolio"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "secrets_manager_rotation" {
  statement_id  = "AllowSecretsManagerRotation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.secrets_rotation.function_name
  principal     = "secretsmanager.amazonaws.com"

  source_account = data.aws_caller_identity.current.account_id
  source_arn     = data.aws_secretsmanager_secret.pawfolio_app.arn
}

resource "aws_secretsmanager_secret_rotation" "pawfolio_app" {
  secret_id           = data.aws_secretsmanager_secret.pawfolio_app.id
  rotation_lambda_arn = aws_lambda_function.secrets_rotation.arn

  rotation_rules {
    automatically_after_days = 30
  }

  depends_on = [
    aws_lambda_permission.secrets_manager_rotation
  ]
}
