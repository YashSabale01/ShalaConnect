# Staging Environment Root Configuration
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "shalaconnect"
      Environment = "staging"
      ManagedBy   = "Terraform"
      Owner       = "Yash Sabale (PRN: 202301040087)"
    }
  }
}

module "shalaconnect_staging" {
  source               = "../../"
  aws_region           = var.aws_region
  project_name         = "shalaconnect"
  environment          = "staging"
  vpc_cidr             = "10.10.0.0/16"
  availability_zones   = ["ap-south-1a", "ap-south-1b"]
  public_subnet_cidrs  = ["10.10.1.0/24", "10.10.2.0/24"]
  private_subnet_cidrs = ["10.10.10.0/24", "10.10.11.0/24"]
  db_name              = "school_management_staging"
  db_username          = "shalaconnect_admin"
  db_password          = var.db_password
  db_instance_class    = "db.t4g.micro"
}

output "staging_alb_url" {
  value = module.shalaconnect_staging.alb_dns_name
}

output "staging_rds_endpoint" {
  value = module.shalaconnect_staging.rds_endpoint
}
