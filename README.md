# ShalaConnect

School Management Platform for Cluster Heads — manage schools, attendance, meetings, events, GR documents, and forms from a single dashboard.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Java 21, Spring Boot 3.2, Spring Security, JPA/Hibernate |
| Frontend | React 18, Vite, Tailwind CSS, Axios, Recharts |
| Database | PostgreSQL 16 |
| Auth | JWT (jjwt 0.12.3), BCrypt |
| File Uploads | Multipart (20MB limit), stored in `/app/uploads` |
| Containerization | Docker, Docker Compose |
| CI/CD | AWS CodePipeline + CodeBuild |
| Infrastructure | AWS CloudFormation (IaC) |
| Hosting | AWS ECS Fargate, RDS PostgreSQL, ECR |

---

## Project Structure

```
ShalaConnect/
├── backend/                  # Spring Boot API
│   ├── src/main/java/com/shalaconnect/
│   │   ├── controller/       # REST controllers
│   │   ├── service/          # Business logic
│   │   ├── model/            # JPA entities
│   │   ├── dto/              # Request/Response DTOs
│   │   ├── repository/       # Spring Data JPA repos
│   │   ├── security/         # JWT filter + util
│   │   ├── config/           # Security, CORS, DataSeeder
│   │   └── exception/        # Global exception handler
│   ├── Dockerfile
│   └── pom.xml
├── frontend/                 # React SPA
│   ├── src/
│   │   ├── pages/
│   │   │   ├── admin/        # Admin-only pages
│   │   │   ├── headmaster/   # Headmaster pages
│   │   │   ├── auth/         # Login page
│   │   │   └── public/       # Public pages
│   │   ├── components/       # Reusable UI components
│   │   ├── services/api.js   # Axios API client
│   │   ├── context/          # Auth context
│   │   └── hooks/            # Custom hooks
│   ├── nginx.conf
│   └── Dockerfile
├── aws/
│   ├── cloudformation.yml    # Full IaC — VPC, RDS, ECR, ECS, CodePipeline
│   └── ecs-task-definition.json
├── database/init.sql         # DB init (tables created by Hibernate)
├── buildspec.yml             # CodeBuild — builds images + deploys to ECS
├── docker-compose.yml        # Local dev
└── deploy.py                 # boto3 deploy helper
```

---

## Roles

| Role | Access |
|---|---|
| `ADMIN` | Full access — manage schools, users, all data |
| `HEADMASTER` | Own school — attendance, meetings, events, GR docs, forms |

---

## API Reference

Base URL: `/api`  
Auth: `Authorization: Bearer <token>` (all endpoints except `/auth/login` and `/health`)

### Auth — `/api/auth`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| POST | `/auth/login` | Public | Login, returns JWT token |
| GET | `/auth/me` | Any | Get current user info |
| POST | `/auth/register-headmaster` | ADMIN | Create headmaster account |
| POST | `/auth/change-password` | Any | Change own password |

### Schools — `/api/schools`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/schools` | Any | List all schools |
| GET | `/schools/{id}` | Any | Get school by ID |
| POST | `/schools` | ADMIN | Create school |
| PUT | `/schools/{id}` | ADMIN | Update school |
| POST | `/schools/{id}/photo` | ADMIN | Upload school photo (multipart) |
| DELETE | `/schools/{id}` | ADMIN | Delete school |

### Attendance — `/api/attendance`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| POST | `/attendance` | HEADMASTER | Submit attendance record |
| PUT | `/attendance/{id}` | HEADMASTER | Update attendance record |
| GET | `/attendance/school/{schoolId}` | Any | Get all records for a school |
| GET | `/attendance/school/{schoolId}/range?start=&end=` | Any | Get records by date range |
| GET | `/attendance/date/{date}` | ADMIN | Get all schools' attendance for a date |
| GET | `/attendance/summary` | ADMIN | Attendance summary across all schools |

### GR Documents — `/api/gr`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/gr` | Any | List all GR documents |
| GET | `/gr/{id}` | Any | Get GR document by ID |
| POST | `/gr` | ADMIN | Upload GR document (multipart) |
| POST | `/gr/{id}/seen` | HEADMASTER | Mark document as seen |
| DELETE | `/gr/{id}` | ADMIN | Delete GR document |

### Meetings — `/api/meetings`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/meetings` | Any | List all meetings |
| GET | `/meetings/upcoming` | Any | List upcoming meetings |
| GET | `/meetings/{id}` | Any | Get meeting by ID |
| POST | `/meetings` | ADMIN | Create meeting |
| PUT | `/meetings/{id}` | ADMIN | Update meeting |
| POST | `/meetings/{id}/acknowledge` | HEADMASTER | Acknowledge meeting attendance |
| DELETE | `/meetings/{id}` | ADMIN | Delete meeting |

### Events — `/api/events`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/events` | Any | List all events |
| GET | `/events/{id}` | Any | Get event by ID |
| POST | `/events` | HEADMASTER | Create event |
| PUT | `/events/{id}` | HEADMASTER | Update event |
| POST | `/events/{id}/media` | HEADMASTER | Upload event media (multipart) |
| POST | `/events/{id}/report` | HEADMASTER | Upload event report (multipart) |
| DELETE | `/events/{id}` | ADMIN | Delete event |

### Forms — `/api/forms`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/forms` | Any | List all forms |
| GET | `/forms/{id}` | Any | Get form by ID |
| POST | `/forms` | ADMIN | Create dynamic form |
| POST | `/forms/{id}/respond` | HEADMASTER | Submit form response |
| GET | `/forms/{id}/export` | ADMIN | Export responses as Excel (.xlsx) |
| DELETE | `/forms/{id}` | ADMIN | Delete form |

### Notifications — `/api/notifications`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/notifications` | Any | List all notifications |
| GET | `/notifications/unread-count` | Any | Get unread count |
| PATCH | `/notifications/{id}/read` | Any | Mark notification as read |
| PATCH | `/notifications/read-all` | Any | Mark all as read |

### Users — `/api/users`

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/users` | ADMIN | List all users |
| GET | `/users/headmasters` | ADMIN | List headmaster accounts |
| PATCH | `/users/{id}/toggle-active` | ADMIN | Enable/disable user |
| DELETE | `/users/{id}` | ADMIN | Delete user |

### Health

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check (used by Docker/ECS) |

---

## Data Models

| Entity | Key Fields |
|---|---|
| `User` | id, name, email, password (BCrypt), role (ADMIN/HEADMASTER), school, active |
| `School` | id, name, udiseCode, address, photoUrl, headmaster |
| `AttendanceRecord` | id, school, date, boysPresent, girlsPresent, teachersPresent, totalEnrolled |
| `Meeting` | id, title, description, scheduledAt, location, createdBy, acknowledgements |
| `Event` | id, title, description, eventDate, school, mediaUrl, reportUrl |
| `GrDocument` | id, title, fileUrl, uploadedBy, seenBy |
| `DynamicForm` | id, title, fields (JSON), createdBy, responses |
| `FormResponse` | id, form, respondedBy, answers (JSON) |
| `Notification` | id, user, message, type, read, createdAt |

---

## Local Development

```bash
cp .env.example .env
docker-compose up -d --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost |
| Backend API | http://localhost:8080/api |
| PostgreSQL | localhost:5432 |

Default login: `admin@shalaconnect.in` / `Admin@123`

### Environment Variables (`.env`)

| Variable | Default | Description |
|---|---|---|
| `DB_USERNAME` | `postgres` | DB user |
| `DB_PASSWORD` | `shala123` | DB password |
| `JWT_SECRET` | *(see .env.example)* | Min 32 chars |
| `ADMIN_EMAIL` | `admin@shalaconnect.in` | Seeded admin email |
| `ADMIN_PASSWORD` | `Admin@123` | Seeded admin password |
| `ALLOWED_ORIGINS` | `http://localhost` | CORS origins |

---

## AWS Deployment — 100% IaC

**No GitHub Actions. No manual AWS steps after setup.**  
One CloudFormation stack provisions everything. Every `git push` to `main` auto-deploys via CodePipeline.

### Architecture

```
git push main
    │
    ▼
CodePipeline
    ├── Stage 1: Source  — GitHub via CodeStar Connection
    ├── Stage 2: Build   — CodeBuild (buildspec.yml)
    │             builds backend  Docker image → ECR
    │             builds frontend Docker image → ECR
    │             registers ECS task definition
    │             creates/updates ECS service
    └── (no Deploy stage — buildspec handles ECS directly)

ECS Fargate Task
    ├── frontend (Nginx :80) → proxies /api/* → localhost:8080
    └── backend  (Spring :8080) → SSM secrets → RDS PostgreSQL
```

### AWS Resources Provisioned

| Resource | Details |
|---|---|
| VPC | 2 public subnets, Internet Gateway |
| RDS | PostgreSQL 16, db.t3.micro, private subnets |
| ECR | 2 repos (backend, frontend), 10-image lifecycle |
| ECS | Fargate cluster, task + service created by buildspec |
| CodeBuild | BUILD_GENERAL1_SMALL, PrivilegedMode (Docker) |
| CodePipeline | Source (GitHub) + Build stages |
| SSM | DB URL, DB creds, JWT secret, admin credentials |
| S3 | Pipeline artifact bucket |
| IAM | Scoped roles for CodeBuild, CodePipeline, ECS execution |
| CloudWatch | Log groups for ECS backend |

### One-time Setup

#### Step 1 — Create GitHub Connection

1. Go to: `https://ap-south-1.console.aws.amazon.com/codesuite/settings/connections`
2. **Create connection** → GitHub → name it `shalaconnect-github` → authorize
3. Copy the Connection ARN: `arn:aws:codestar-connections:ap-south-1:<account-id>:connection/xxxxxxxx`

#### Step 2 — Deploy CloudFormation Stack

**Option A — AWS Console:**

1. Go to: `https://ap-south-1.console.aws.amazon.com/cloudformation`
2. Upload `aws/cloudformation.yml` → Stack name: `shalaconnect`
3. Fill parameters:

| Parameter | Value |
|---|---|
| `GitHubOwner` | `YashSabale01` |
| `GitHubRepo` | `ShalaConnect` |
| `GitHubBranch` | `main` |
| `GitHubConnectionArn` | *(ARN from Step 1)* |
| `DBPassword` | `MyRdsPass123!` |
| `JwtSecret` | `shalaconnect_prod_jwt_secret_32_chars_minimum!!` |
| `AdminEmail` | `admin@shalaconnect.in` |
| `AdminPassword` | `Admin@123` |

4. Check ✅ IAM acknowledgement → **Submit**

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

Takes ~15 minutes (RDS provisioning). CodePipeline runs automatically after stack creation.

### Every Future Deploy

```bash
git push origin main
```

### Monitor

| What | Where |
|---|---|
| Pipeline | CodePipeline → `shalaconnect-pipeline` |
| Build logs | CodeBuild → `shalaconnect-build` |
| App logs | CloudWatch → `/ecs/shalaconnect-backend` |
| App URL | ECS → Clusters → `shalaconnect-cluster` → Tasks → task public IP |

### Notes

- RDS is in private subnets — not publicly accessible
- All secrets in SSM Parameter Store — never in code
- ECR auto-expires images older than 10 most recent
- ECS task public IP changes on each deploy — add an ALB for a stable URL
- File uploads at `/app/uploads` inside container — mount EFS for persistence
- `BUILD_GENERAL1_SMALL` is free tier (100 min/month)
- RDS `db.t3.micro` is free tier for 12 months on new accounts
