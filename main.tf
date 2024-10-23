# modules/ec2/main.tf

provider "aws" {
  region = var.region
}

resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type

  tags = {
    Name = var.name
  }
}

# Input variables
variable "region" {
  description = "AWS region to deploy"
  default     = "us-east-1"
}

variable "ami" {
  description = "AMI ID for the instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type"
  default     = "t2.micro"
}

variable "name" {
  description = "Name of the instance"
}
