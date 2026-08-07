module "aws_ebs_csi_pod_identity" {
  source  = "terraform-aws-modules/eks-pod-identity/aws"
  version = "~> 2.8"

  name = "aws-ebs-csi"

  attach_aws_ebs_csi_policy = true

  associations = {
    ebs = {
      cluster_name    = module.eks.cluster_name
      namespace       = "kube-system"
      service_account = "ebs-csi-controller-sa"
    }
  }

  tags = {
    Project     = "Pawfolio"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
