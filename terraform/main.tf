terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Recommended for team production: configure S3 backend for tfstate
  # backend "s3" {
  #   bucket         = "shalaconnect-terraform-state"
  #   key            = "prod/terraform.tfstate"
  #   region         = "ap-south-1"
  #   dynamodb_table = "shalaconnect-tf-locks"
  #   encrypt        = true
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# CloudFront requires ACM certificates in us-east-1 for custom domains
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}
