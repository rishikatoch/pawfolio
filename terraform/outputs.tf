output "ecr_repository_url" {
  description = "Pawfolio ECR Repository URL"
  value       = aws_ecr_repository.pawfolio.repository_url
}
