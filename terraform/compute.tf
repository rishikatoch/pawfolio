resource "aws_instance" "pawfolio" {
  ami                    = data.aws_ssm_parameter.ubuntu_ami.value
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.pawfolio.id]
  key_name               = var.key_pair_name

  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.pawfolio.name

  user_data = file("${path.module}/../scripts/user_data.sh")

  monitoring = true

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    encrypted = true
  }

  tags = {
    Name = "pawfolio-server"
  }
}
