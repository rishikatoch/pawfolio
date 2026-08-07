output "cluster_name" {
  description = "Amazon EKS Cluster Name"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "Amazon EKS Cluster Endpoint"
  value       = module.eks.cluster_endpoint
}

output "cluster_version" {
  description = "Amazon EKS Kubernetes Version"
  value       = module.eks.cluster_version
}

output "cluster_certificate_authority_data" {
  description = "Cluster Certificate Authority Data"
  value       = module.eks.cluster_certificate_authority_data
  sensitive   = true
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "private_subnets" {
  description = "Private Subnets"
  value       = module.vpc.private_subnets
}

output "public_subnets" {
  description = "Public Subnets"
  value       = module.vpc.public_subnets
}
