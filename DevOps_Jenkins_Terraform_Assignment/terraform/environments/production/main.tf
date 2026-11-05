# Production Environment Root Configuration
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
      Environment = "production"
      ManagedBy   = "Terraform"
      Owner       = "Yash Sabale (PRN: 202301040087)"
    }
  }
}

module "shalaconnect_prod" {
  source               = "../../"
  aws_region           = var.aws_region
  project_name         = "shalaconnect"
  environment          = "production"
  vpc_cidr             = "10.20.0.0/16"
  availability_zones   = ["ap-south-1a", "ap-south-1b"]
  public_subnet_cidrs  = ["10.20.1.0/24", "10.20.2.0/24"]
  private_subnet_cidrs = ["10.20.10.0/24", "10.20.11.0/24"]
  db_name              = "school_management_prod"
  db_username          = "shalaconnect_dba"
  db_password          = var.db_password
  db_instance_class    = "db.t4g.small"
}

output "production_alb_url" {
  value = module.shalaconnect_prod.alb_dns_name
}

output "production_rds_endpoint" {
  value = module.shalaconnect_prod.rds_endpoint
}
