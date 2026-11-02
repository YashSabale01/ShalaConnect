output "vpc_id" {
  description = "The ID of the provisioned VPC"
  value       = module.vpc.vpc_id
}

output "public_subnets" {
  description = "List of public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnets" {
  description = "List of private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

output "alb_dns_name" {
  description = "Public Load Balancer entry endpoint"
  value       = module.compute.alb_dns_name
}

output "rds_endpoint" {
  description = "PostgreSQL Database connection endpoint"
  value       = module.database.endpoint
}

output "ecs_cluster_name" {
  description = "ECS Cluster Name"
  value       = module.compute.ecs_cluster_name
}
