terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "customer_360" {
  bucket = "${var.project_name}-${var.environment}-data"
}

resource "aws_s3_bucket_versioning" "customer_360" {
  bucket = aws_s3_bucket.customer_360.id
  versioning_configuration { status = "Enabled" }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "project_name" {
  type    = string
  default = "customer-360"
}
