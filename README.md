# ShalaConnect

School Management Platform for Cluster Heads — Spring Boot + React + PostgreSQL.

---

## Local Development

```bash
cp .env.example .env
docker-compose up -d --build

# Frontend: http://localhost
# Backend:  http://localhost:8080
# Login:    admin@shalaconnect.in / Admin@123
```

---

## AWS Deployment — 100% IaC (CloudFormation + CodePipeline)

**No GitHub Actions. No manual AWS steps after setup.**  
One CloudFormation stack provisions everything.  
Every `git push` to `main` automatically builds and deploys via CodePipeline.

---

### Architecture

```
git push main
    │
    ▼
CodePipeline (AWS)
    ├── Stage 1: Source  — pulls code from GitHub via CodeStar Connection
    ├── Stage 2: Build   — CodeBuild runs buildspec.yml
    │             builds backend  Docker image → pushes to ECR
    │             builds frontend Docker image → pushes to ECR
    │             writes imagedefinitions.json
    └── Stage 3: Deploy  — updates ECS service with new image tags

ECS Fargate Task
    ├── frontend container (Nginx :80) → proxies /api/* to localhost:8080
    └── backend  container (Spring :8080) → reads secrets from SSM → RDS
```

---

### IaC Files

| File | Purpose |
|------|---------|
| `aws/cloudformation.yml` | Everything — VPC, RDS, ECR, ECS, CodeBuild, CodePipeline, IAM, SSM |
| `buildspec.yml` | CodeBuild instructions — builds both Docker images |

---

### One-time Setup (do this once, never again)

#### Step 1 — Create a GitHub Connection in AWS Console

This is the only thing you cannot do via CloudFormation — GitHub OAuth requires a browser click.

1. Go to AWS Console → **Developer Tools → Connections**  
   Direct link: `https://ap-south-1.console.aws.amazon.com/codesuite/settings/connections`
2. Click **Create connection** → choose **GitHub**
3. Name it `shalaconnect-github` → click **Connect to GitHub** → authorize
4. Copy the **Connection ARN** — looks like:  
   `arn:aws:codestar-connections:ap-south-1:123456789:connection/xxxxxxxx`

#### Step 2 — Deploy the CloudFormation stack

**Option A — AWS Console (recommended):**

1. Go to: `https://ap-south-1.console.aws.amazon.com/cloudformation/home?region=ap-south-1#/stacks/create`
2. Choose **Upload a template file** → upload `aws/cloudformation.yml` → **Next**
3. Stack name: `shalaconnect`
4. Fill parameters:

| Parameter | Value |
|---|---|
| AdminEmail | `admin@shalaconnect.in` |
| AdminPassword | `Admin@123` |
| DBPassword | `MyRdsPass123!` |
| GitHubBranch | `main` |
| GitHubConnectionArn | *(ARN from Step 1)* |
| GitHubOwner | `YashSabale01` |
| GitHubRepo | `ShalaConnect` |
| JwtSecret | `shalaconnect_prod_jwt_secret_32_chars_minimum!!` |

5. **Next** → **Next** → check ✅ IAM acknowledgement → **Submit**

**Option B — AWS CLI:**

```bash
aws cloudformation deploy \
  --stack-name shalaconnect \
  --template-file aws/cloudformation.yml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region ap-south-1 \
  --parameter-overrides \
    GitHubOwner=YashSabale01 \
    GitHubRepo=ShalaConnect \
    GitHubBranch=main \
    GitHubConnectionArn=arn:aws:codeconnections:ap-south-1:ACCOUNT_ID:connection/XXXXXXXX \
    DBPassword=MyRdsPass123! \
    JwtSecret=shalaconnect_prod_jwt_secret_32_chars_minimum!! \
    AdminEmail=admin@shalaconnect.in \
    AdminPassword=Admin@123
```

This takes ~15 minutes (RDS provisioning).  
When it completes, CodePipeline automatically runs the first build and deploys the app.

---

### Every future deploy

```bash
git push origin main
```

CodePipeline detects the push and runs automatically. Done.

---

### Monitor

- **Pipeline**: AWS Console → CodePipeline → `shalaconnect-pipeline`
- **Build logs**: AWS Console → CodeBuild → `shalaconnect-build`
- **App logs**: AWS Console → CloudWatch → `/ecs/shalaconnect-backend`
- **App URL**: ECS Console → Clusters → `shalaconnect-cluster` → Tasks → task public IP

---

### Notes

- RDS is in private subnets — not publicly accessible
- All secrets live in SSM Parameter Store — never in code
- ECR keeps last 10 images, older ones auto-expire
- ECS task public IP changes on each deploy — add an ALB for a stable URL
- File uploads live in `/app/uploads` inside the container — mount EFS for persistence
