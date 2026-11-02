variable "aws_region" {
  type        = string
  default     = "ap-south-1"
  description = "AWS deployment region (Asia Pacific - Mumbai)"
}

variable "project_name" {
  type        = string
  default     = "shalaconnect"
  description = "Application project identifier"
}

variable "environment" {
  type        = string
  default     = "staging"
  description = "Deployment target environment (staging/prod)"
}

variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "CIDR block for VPC"
}

variable "availability_zones" {
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]
  description = "Availability zones list"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
  description = "CIDR blocks for public subnets"
}

variable "private_subnet_cidrs" {
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
  description = "CIDR blocks for private subnets"
}

variable "db_name" {
  type        = string
  default     = "school_management"
  description = "PostgreSQL DB name"
}

variable "db_username" {
  type        = string
  default     = "shalaconnect_admin"
  description = "PostgreSQL master username"
}

variable "db_password" {
  type        = string
  sensitive   = true
  default     = "ShalaConnectPass2026!"
  description = "PostgreSQL master password"
}

variable "db_instance_class" {
  type        = string
  default     = "db.t4g.micro"
  description = "RDS DB instance class"
}
