module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  cluster_name    = "dev-cluster"
  cluster_version = "1.21"
  vpc_id          = var.vpc_id
  subnet_ids      = var.subnet_ids

  worker_groups = [
    {
      instance_type = "t3.medium"
      asg_max_size  = 5
    }
  ]
}

output "kubeconfig" {
  value = module.eks.kubeconfig
}
