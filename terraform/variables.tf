variable "aws_region" {
  description = "AWS Region"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}
variable "key_pair_name" {
  description = "EC2 Key Pair Name"
  type        = string
}
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}
