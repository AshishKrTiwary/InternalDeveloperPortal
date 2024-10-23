module "ec2" {
  source          = "./modules/ec2"
  region          = var.region
  ami             = "ami-123456"
  instance_type   = "t2.micro"
  name            = "dev-instance"
}

output "instance_id" {
  value = module.ec2.web_instance_id
}

output "instance_public_ip" {
  value = module.ec2.web_instance_public_ip
}
