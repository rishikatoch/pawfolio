resource "aws_security_group" "pawfolio" {
  name        = "pawfolio-sg"
  description = "Security group for Pawfolio"
  vpc_id      = aws_vpc.pawfolio.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"

    # Temporary for learning.
    # Later we'll restrict this or use Session Manager.
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"

    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "pawfolio-security-group"
  }
}
