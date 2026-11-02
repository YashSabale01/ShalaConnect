output "endpoint" {
  description = "Connection endpoint for the RDS PostgreSQL instance"
  value       = aws_db_instance.postgres.endpoint
}

output "db_name" {
  description = "Database name"
  value       = aws_db_instance.postgres.db_name
}

output "db_instance_id" {
  description = "RDS Instance Identifier"
  value       = aws_db_instance.postgres.id
}
