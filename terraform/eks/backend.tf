terraform {
  backend "s3" {
    bucket       = "pawfolio-terraform-state-rishi-977574653467"
    key          = "eks/terraform.tfstate"
    region       = "us-west-2"
    encrypt      = true
    use_lockfile = true
  }
}
