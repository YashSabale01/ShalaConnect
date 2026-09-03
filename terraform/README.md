# ShalaConnect — AWS Infrastructure as Code (Terraform)

This directory contains the production-grade **Terraform** configuration provisioning the complete AWS architecture for **ShalaConnect (शाळाकनेक्ट)**:

```
                     [ Internet ]
                          │
                   [ Route 53 DNS ]
                          │
               [ AWS CloudFront (CDN) ]
                          │
          ┌───────────────┴───────────────┐
          │                               │
    (Static Assets)                  (/api/* & /uploads/*)
          │                               │
  [ S3 Bucket (Vite UI) ]     [ Application Load Balancer ]
                                          │
                                 [ ECS Fargate Cluster ]
                              ┌───────────┴───────────┐
                              │  ShalaConnect Backend │
                              │    (Spring Boot 21)   │
                              └───────────┬───────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  │                                               │
         [ Amazon RDS PostgreSQL ]                       [ Amazon S3 Bucket ]
          (Multi-AZ / Encrypted)                       (Photos, GRs, Documents)
```

## Provisioned AWS Resources

1. **Networking (`vpc.tf`)**:
   - Multi-AZ VPC (`10.0.0.0/16`) in `ap-south-1` (Mumbai).
   - 2 Public Subnets (ALB & NAT Gateway).
   - 2 Private Subnets (ECS Fargate & RDS PostgreSQL).
   - Internet Gateway + NAT Gateway with Elastic IP.

2. **Security & Isolation (`security_groups.tf`)**:
   - `alb-sg`: Public HTTP/HTTPS ingress.
   - `ecs-sg`: Ingress restricted to port `8080` strictly from `alb-sg`.
   - `rds-sg`: Ingress restricted to port `5432` strictly from `ecs-sg`.

3. **Storage (`s3.tf`)**:
   - S3 Frontend Bucket with **Origin Access Control (OAC)** (zero public access).
   - S3 Uploads Bucket with AES-256 encryption, versioning, and IAM access.

4. **Database (`rds.tf`)**:
   - Amazon RDS PostgreSQL 16 on Graviton (`db.t4g.micro` / `db.t4g.small`).
   - Encrypted at rest, automated 7-day backups, IST timezone configuration.

5. **Compute & Orchestration (`ecs.tf` & `alb.tf`)**:
   - ECS Fargate cluster with Container Insights.
   - Task definition with CloudWatch logs (`/ecs/shalaconnect-backend`).
   - Application Load Balancer with target group health check at `/api/health`.

6. **Edge & CDN (`cloudfront.tf`)**:
   - CloudFront distribution with HTTPS redirection and SPA fallback (`index.html`).
   - Caching for static assets and pass-through for `/api/*`.

---

## Deployment Instructions

### Prerequisites
- [AWS CLI](https://aws.amazon.com/cli/) installed and authenticated (`aws configure`).
- [Terraform](https://www.terraform.io/) >= 1.5.0.

### Step 1: Configure Variables
```bash
cp terraform.tfvars.example terraform.tfvars
# Open terraform.tfvars and provide:
# - db_password
# - jwt_secret
# - admin_password
# - backend_image (your Amazon ECR URI)
```

### Step 2: Initialize & Review Plan
```bash
cd terraform
terraform init
terraform plan
```

### Step 3: Deploy Infrastructure
```bash
terraform apply
```

### Step 4: Deploy Frontend & Invalidate CDN Cache
```bash
# 1. Build frontend
cd ../frontend
npm run build

# 2. Sync to S3
aws s3 sync dist/ s3://<frontend_s3_bucket_from_output> --delete

# 3. Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id <cloudfront_distribution_id_from_output> --paths "/*"
```
