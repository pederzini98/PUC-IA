# terraform/main.tf
resource "aws_s3_bucket" "bugsage_bucket" {
  bucket = var.s3_bucket_name
}
resource "aws_s3_bucket_versioning" "bugsage_bucket_ver" {
  bucket = aws_s3_bucket.bugsage_bucket.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_security_group" "bugsage_sg" {
  name        = "bugsage-sg"
  description = "Allow 22 and 8501"
  vpc_id      = var.vpc_id

  ingress { from_port = 22  to_port = 22  protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 8501 to_port = 8501 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0   to_port = 0   protocol = "-1"  cidr_blocks = ["0.0.0.0/0"] }
}

resource "aws_instance" "bugsage_ec2" {
  ami                    = var.ec2_ami_id
  instance_type          = var.ec2_instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.bugsage_sg.id]
  key_name               = var.ssh_key_name

  user_data = <<-EOF
              #!/bin/bash
              set -eux
              apt-get update
              apt-get install -y docker.io
              systemctl enable docker
              systemctl start docker
              docker run -d --restart=always -p 8501:8501 \
                -e GOOGLE_API_KEY=${GOOGLE_API_KEY} \
                --name bugsage ghcr.io/SEU_USUARIO/bugsage:latest
              EOF

  tags = { Name = "bugsage-ec2" }
}
