output "alb_security_group_id" {
  description = "ID of ALB Security Group"
  value       = aws_security_group.alb.id
}

output "app_security_group_id" {
  description = "ID of Application Security Group"
  value       = aws_security_group.app.id
}

output "db_security_group_id" {
  description = "ID of Database Security Group"
  value       = aws_security_group.db.id
}
