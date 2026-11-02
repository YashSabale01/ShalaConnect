variable "project_name" {
  type        = string
  description = "Project name"
}

variable "environment" {
  type        = string
  description = "Environment name"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs for DB Subnet Group"
}

variable "security_group_id" {
  type        = string
  description = "Database Security Group ID"
}

variable "db_name" {
  type        = string
  default     = "school_management"
  description = "Database name"
}

variable "db_username" {
  type        = string
  default     = "shalaconnect_admin"
  description = "Database Master Username"
}

variable "db_password" {
  type        = string
  sensitive   = true
  default     = "ShalaConnectSecure2026!"
  description = "Database Master Password"
}

variable "instance_class" {
  type        = string
  default     = "db.t4g.micro"
  description = "RDS DB Instance class"
}
