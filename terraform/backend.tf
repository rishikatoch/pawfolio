terraform {
  backend "s3" {
    bucket         = "pawfolio-terraform-state-rishi-977574653467"
    key            = "production/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "pawfolio-terraform-state-lock"
    encrypt        = true
  }
}
