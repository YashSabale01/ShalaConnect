output "cloudfront_url" {
  description = "Public URL for ShalaConnect (CloudFront CDN)"
  value       = "https://${aws_cloudfront_distribution.cdn.domain_name}"
}

output "cloudfront_distribution_id" {
  description = "CloudFront Distribution ID (for cache invalidation during deployments)"
  value       = aws_cloudfront_distribution.cdn.id
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = aws_lb.main.dns_name
}

output "rds_endpoint" {
  description = "PostgreSQL RDS connection endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "frontend_s3_bucket" {
  description = "S3 bucket for React build artifacts (run: aws s3 sync dist/ s3://<bucket>)"
  value       = aws_s3_bucket.frontend.id
}

output "uploads_s3_bucket" {
  description = "S3 bucket for persistent user uploads (photos, documents)"
  value       = aws_s3_bucket.uploads.id
}

output "ecs_cluster_name" {
  description = "ECS Cluster Name"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECS Service Name"
  value       = aws_ecs_service.backend.name
}
