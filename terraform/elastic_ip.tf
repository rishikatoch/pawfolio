resource "aws_eip" "pawfolio" {
  domain = "vpc"

  tags = {
    Name = "pawfolio-eip"
  }
}

resource "aws_eip_association" "pawfolio" {
  instance_id   = aws_instance.pawfolio.id
  allocation_id = aws_eip.pawfolio.id
}
