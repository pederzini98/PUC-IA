# terraform/variables.tf
variable "aws_region"        { description = "AWS region"; type = string; default = "us-east-1" }
variable "s3_bucket_name"    { description = "S3 bucket name"; type = string }
variable "vpc_id"            { description = "Existing VPC ID"; type = string }
variable "subnet_id"         { description = "Subnet ID for the EC2 instance"; type = string }
variable "ec2_ami_id"        { description = "AMI ID for the EC2 instance"; type = string }
variable "ec2_instance_type" { description = "EC2 instance type"; type = string; default = "t3.small" }
variable "ssh_key_name"      { description = "Existing EC2 KeyPair name for SSH access"; type = string }
variable "GOOGLE_API_KEY"    { description = "Google API key injected into container"; type = string; sensitive = true }
