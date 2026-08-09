module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  name               = var.cluster_name
  kubernetes_version = "1.33"

  endpoint_public_access = true

  enable_cluster_creator_admin_permissions = true

  authentication_mode = "API_AND_CONFIG_MAP"

  addons = {
    eks-pod-identity-agent = {
      before_compute = true
    }

    vpc-cni = {
      before_compute = true
    }

    coredns = {}

    kube-proxy = {}

    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    pawfolio = {

      instance_types = ["c7i-flex.large"]

      ami_type = "AL2023_x86_64_STANDARD"

      capacity_type = "ON_DEMAND"

      min_size     = 1
      desired_size = 1
      max_size     = 2

      disk_size = 30

      labels = {
        role = "general"
      }

      update_config = {
        max_unavailable_percentage = 33
      }

      tags = {
        Name = "pawfolio-node-group"
      }
    }
  }

  tags = {
    Project     = "Pawfolio"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
