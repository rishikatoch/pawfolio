output "instance_public_ip" {
  value = aws_instance.pawfolio.public_ip
}

output "instance_id" {
  value = aws_instance.pawfolio.id
}

output "public_dns" {
  value = aws_instance.pawfolio.public_dns
}