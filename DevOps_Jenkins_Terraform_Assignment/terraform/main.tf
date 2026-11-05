# Master Terraform Orchestrator for ShalaConnect Cloud Infrastructure
# Author: Yash Janardan Sabale (PRN: 202301040087)
# Academic Activity: IA Activity No. 3 (Jenkins CI/CD + Terraform)

# Module 1: Virtual Private Cloud (Networking Tier)
module "vpc" {
  source               = "./modules/vpc"
  project_name         = var.project_name
  environment          = var.environment
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
}

# Module 2: Layered Security Groups (Security Tier)
module "security" {
  source       = "./modules/security"
  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
}

# Module 3: RDS PostgreSQL Database (Data Tier)
module "database" {
  source            = "./modules/database"
  project_name      = var.project_name
  environment       = var.environment
  subnet_ids        = module.vpc.private_subnet_ids
  security_group_id = module.security.db_security_group_id
  db_name           = var.db_name
  db_username       = var.db_username
  db_password       = var.db_password
  instance_class    = var.db_instance_class
}

# Module 4: Application Load Balancer & Container Workloads (Compute Tier)
module "compute" {
  source                = "./modules/compute"
  project_name          = var.project_name
  environment           = var.environment
  vpc_id                = module.vpc.vpc_id
  public_subnet_ids     = module.vpc.public_subnet_ids
  alb_security_group_id = module.security.alb_security_group_id
}
