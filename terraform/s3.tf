# ==============================================================================
# S3 Buckets (Frontend Static Hosting & Uploads Persistence)
# ==============================================================================

# Random suffix for globally unique S3 bucket names
resource "random_string" "bucket_suffix" {
  length  = 6
  special = false
  upper   = false
}

# ── Frontend S3 Bucket (React SPA Build) ───────────────────────────────────────
resource "aws_s3_bucket" "frontend" {
  bucket        = "${var.project_name}-frontend-${var.environment}-${random_string.bucket_suffix.result}"
  force_destroy = false

  tags = {
    Name = "${var.project_name}-frontend"
  }
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# ── Uploads S3 Bucket (Photos, GR PDFs, Dynamic Form Attachments) ─────────────
resource "aws_s3_bucket" "uploads" {
  bucket        = "${var.project_name}-uploads-${var.environment}-${random_string.bucket_suffix.result}"
  force_destroy = false

  tags = {
    Name = "${var.project_name}-uploads"
  }
}

resource "aws_s3_bucket_versioning" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
