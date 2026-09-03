# ==============================================================================
# AWS CloudFront CDN (Global Edge Delivery, OAC for S3, Proxy to ALB)
# ==============================================================================

# Origin Access Control (OAC) for Frontend S3 Bucket
resource "aws_cloudfront_origin_access_control" "frontend_oac" {
  name                              = "${var.project_name}-${var.environment}-oac"
  description                       = "OAC for ShalaConnect React Frontend S3"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "cdn" {
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  comment             = "ShalaConnect CDN (${var.environment})"
  price_class         = "PriceClass_100" # Lowest cost (US, Europe, India)

  # ── Origin 1: React Static Files in S3 ───────────────────────────────────────
  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id                = "S3-Frontend"
    origin_access_control_id = aws_cloudfront_origin_access_control.frontend_oac.id
  }

  # ── Origin 2: ALB for API & Dynamic Requests ─────────────────────────────────
  origin {
    domain_name = aws_lb.main.dns_name
    origin_id   = "ALB-Backend"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only" # ALB handles HTTP internally from CF
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  # ── Default Behavior: React SPA (Static S3) ──────────────────────────────────
  default_cache_behavior {
    target_origin_id       = "S3-Frontend"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 0
    default_ttl = 86400    # 24 hours
    max_ttl     = 31536000 # 1 year
    compress    = true
  }

  # ── Path Behavior: /api/* -> Proxy to ALB Backend ────────────────────────────
  ordered_cache_behavior {
    path_pattern           = "/api/*"
    target_origin_id       = "ALB-Backend"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]

    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Host", "Accept", "Content-Type"]
      cookies {
        forward = "all"
      }
    }

    min_ttl     = 0
    default_ttl = 0 # Do not cache dynamic API responses
    max_ttl     = 0
    compress    = true
  }

  # ── Path Behavior: /uploads/* -> Proxy to Backend / Static Uploads ───────────
  ordered_cache_behavior {
    path_pattern           = "/uploads/*"
    target_origin_id       = "ALB-Backend"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    min_ttl     = 3600
    default_ttl = 86400
    max_ttl     = 604800
    compress    = true
  }

  # ── SPA Fallback: Return index.html for 403 & 404 (React Router support) ────
  custom_error_response {
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }

  custom_error_response {
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name = "${var.project_name}-cdn"
  }
}

# ── S3 Bucket Policy allowing CloudFront OAC to Read ───────────────────────────
resource "aws_s3_bucket_policy" "frontend_policy" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowCloudFrontServicePrincipalReadOnly"
        Effect    = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.frontend.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.cdn.arn
          }
        }
      }
    ]
  })
}
