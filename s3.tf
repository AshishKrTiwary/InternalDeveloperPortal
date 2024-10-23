# modules/s3/main.tf

resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
  acl    = "private"
}

variable "bucket_name" {
  description = "The name of the bucket"
  type        = string
}
