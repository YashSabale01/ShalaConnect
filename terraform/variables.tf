variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "ap-south-1" # Asia Pacific (Mumbai) - Ideal for Maharashtra
}

variable "environment" {
  description = "Deployment environment (e.g. prod, staging, dev)"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project identifier"
  type        = string
  default     = "shalaconnect"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones to use"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "db_name" {
  description = "PostgreSQL Database Name"
  type        = string
  default     = "school_management"
}

variable "db_username" {
  description = "PostgreSQL Master Username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "PostgreSQL Master Password (store securely in SSM/Secrets Manager)"
  type        = string
  sensitive   = true
}

variable "jwt_secret" {
  description = "Application JWT Secret Key (min 32 chars)"
  type        = string
  sensitive   = true
}

variable "admin_email" {
  description = "Default cluster admin email"
  type        = string
  default     = "admin@shalaconnect.in"
}

variable "admin_password" {
  description = "Default cluster admin password"
  type        = string
  sensitive   = true
}

variable "backend_image" {
  description = "ECR Image URI for ShalaConnect backend"
  type        = string
  default     = "shalaconnect-backend:latest"
}

variable "container_cpu" {
  description = "ECS Task CPU units (e.g. 512 for 0.5 vCPU)"
  type        = number
  default     = 512
}

variable "container_memory" {
  description = "ECS Task Memory in MB (e.g. 1024 for 1 GB)"
  type        = number
  default     = 1024
}

variable "domain_name" {
  description = "Optional custom domain name (e.g. shalaconnect.in)"
  type        = string
  default     = ""
}
