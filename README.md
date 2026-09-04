# ShalaConnect (शाळाकनेक्ट)

> **School Education Cluster Administration & Governance Platform**  
> Designed for **Cluster Resource Centers (CRC / केंद्र प्रमुख / Kendra Pramukh)** and **School Headmasters (मुख्याध्यापक)** across Maharashtra to streamline daily attendance, Government Resolutions (GR), cluster review meetings, celebration events, and dynamic survey forms.

---

## Table of Contents
1. [Unified Architecture & Deployment Logic](#unified-architecture--deployment-logic)
2. [Automated CI/CD Pipeline (GitHub Actions)](#automated-cicd-pipeline-github-actions)
3. [Key Features & Capabilities](#key-features--capabilities)
4. [Tech Stack](#tech-stack)
5. [Project Directory Structure](#project-directory-structure)
6. [Roles & Permissions](#roles--permissions)
7. [Complete REST API Reference](#complete-rest-api-reference)
8. [Database Schema & Entities](#database-schema--entities)
9. [Local Development (Docker Compose)](#local-development-docker-compose)
10. [AWS Production Deployment with Terraform](#aws-production-deployment-with-terraform)

---

## Unified Architecture & Deployment Logic

ShalaConnect uses **one single, standardized deployment strategy**:
- **Infrastructure as Code (IaC)**: 100% provisioned and managed with **Terraform** ([`terraform/`](./terraform/)).
- **Automated CI/CD**: 100% automated with **GitHub Actions** ([`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml)).
- **Zero Legacy Stacks**: All legacy CloudFormation templates, CodePipeline configs, and helper scripts have been removed in favor of this clean, decoupled architecture.

### Target Architecture

```
                                [ Internet Users / Headmasters / Admins ]
                                                   │
                                                   ▼
                                        [ Route 53 DNS (Custom Domain) ]
                                                   │
                                                   ▼
                                        [ AWS CloudFront (Global CDN) ]
                                        (SSL Termination & HTTPS Enforced)
                                                   │
                         ┌─────────────────────────┴─────────────────────────┐
                         │                                                   │
         (Path: /* - Static SPA Assets)                    (Path: /api/* & /uploads/*)
                         │                                                   │
                         ▼                                                   ▼
           [ Amazon S3 (Frontend Bucket) ]                     [ Application Load Balancer (ALB) ]
             (Origin Access Control - OAC)                                   │
                                                                             ▼
                                                                  [ ECS Fargate Cluster ]
                                                               ┌─────────────┴─────────────┐
                                                               │    ShalaConnect Backend   │
                                                               │      (Spring Boot 21)     │
                                                               └─────────────┬─────────────┘
                                                                             │
                                              ┌──────────────────────────────┴──────────────────────────────┐
                                              ▼                                                             ▼
                                [ Amazon RDS PostgreSQL 16 ]                               [ Amazon S3 (Uploads Bucket) ]
                                 (Multi-AZ, Private Subnets)                                (GR PDFs, Event Photos, Forms)
```

---

## Automated CI/CD Pipeline (GitHub Actions)

Deployments are automated through [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml). Every `git push origin main` triggers two parallel jobs:

```
                            git push origin main
                                     │
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
    [ Job 1: Deploy Backend ]               [ Job 2: Deploy Frontend ]
                 │                                       │
    • Checkout & Set up JDK 21              • Checkout & Set up Node.js 20
    • Authenticate with Amazon ECR          • Install dependencies (npm ci)
    • Build Spring Boot Docker image        • Build optimized SPA (vite build)
    • Tag with SHA & latest                 • Sync build to S3 Frontend bucket
    • Push image to Amazon ECR              • Invalidate CloudFront CDN cache
    • Trigger ECS Fargate rolling rollout   
```

---

## Key Features & Capabilities

### 1. Bilingual Marathi & English UI (मराठी भाषांतर)
- Built-in live language switcher in the navigation bar (`EN | मराठी`).
- Localized terminology reflecting Maharashtra State Board and Zilla Parishad governance (*दैनिक उपस्थिती, शाळा माहिती, शासन निर्णय (GR), केंद्र बैठका, शालेय उपक्रम, प्रपत्रे, अहवाल*).

### 2. Daily Student & Teacher Attendance (दैनिक उपस्थिती)
- **Tenancy Validation**: Headmasters can strictly submit/update attendance for their assigned school only.
- **Defaulter Tracking**: Real-time cluster dashboard showing submitted vs. pending schools.
- **Offline Caching & Auto-Sync**: In rural areas with spotty 2G/3G connectivity, attendance is cached locally (`localStorage`) and automatically flushes to the server when network connectivity is restored.
- **30-Day Trend Analytics**: Visual attendance graphs powered by Recharts.

### 3. BEO Monthly Cluster Report Card Export (मासिक केंद्र अहवाल)
- One-click Excel export (`.xlsx`) formatted for the Block Education Officer (BEO / गट शिक्षणाधिकारी).
- Computes school-wise compliance status (*Regular, Partial, Non-Compliant*), student presence percentages, and operational days.

### 4. Government Resolutions & Circulars (शासन निर्णय - GR)
- Admin uploads circulars, PDF documents, and policy updates (up to 20MB).
- Read receipts: Tracks which school headmasters have seen and acknowledged each circular with audit timestamps (`/api/gr/{id}/seen`).

### 5. Cluster Review Meetings (केंद्र बैठका)
- Scheduling meetings with agenda, venue, offline/online type, and video conference links.
- One-click headmaster acknowledgment of meeting attendance.

### 6. School Events & Photo Proof Implementations (शालेय उपक्रम)
- Admin publishes cluster-wide events and celebrations (e.g. Independence Day, Sports Meet, Science Exhibition).
- Headmasters submit implementation reports with photographic proof.
- Full multi-photo support with deduplicated storage and direct high-resolution previews.
- **Public Photo Galleries**: Citizens and parents can explore event celebration photos and implementation notes directly on the Public Portal and individual school profile pages.

### 7. Dynamic Data Collection Forms (माहिती प्रपत्रे)
- Admin form builder supporting dynamic fields: `TEXT`, `NUMBER`, `SELECT`, `TEXTAREA`, `DATE`, `CHECKBOX`.
- Schools submit customized survey data.
- One-click Excel aggregation and export of all school responses using Apache POI.

### 8. Bidirectional Notification System (सूचना प्रणाली)
- In-app notification bell with unread counters.
- Headmasters are notified when:
  - New events are scheduled.
  - New GR documents are published.
  - New meetings are arranged.
  - New survey forms are assigned.
- Cluster Admins are notified when:
  - Schools submit daily attendance.
  - Schools submit event implementation reports and photos.
  - Schools submit dynamic form responses.

### 9. Public Transparency Portal (नागरिक पोर्टल)
- Search schools across the cluster by Name, Village, or 11-digit UDISE Code.
- Detailed public profiles showing student enrollment, teacher staff count, infrastructure facilities, top student achievements, and attendance statistics.

### 10. Headmaster Profile & Self-Service
- Dedicated profile portal (`/headmaster/profile`) to inspect assigned school records and update account security passwords.

---

## Tech Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Java 21, Spring Boot 3.2.3 | REST API, Spring Security, Spring Data JPA, Apache POI |
| **Frontend** | React 18, Vite 5, Tailwind CSS | SPA, Lucide Icons, Recharts, React Hook Form, Context API |
| **Database** | PostgreSQL 16 | Relational store, foreign key integrity, Hibernate `ddl-auto` |
| **Auth & Security** | JWT (JJWT 0.12.3) + BCrypt | Stateless bearer authentication with role validation |
| **CDN & Edge** | AWS CloudFront | Global edge caching, HTTPS redirection, SPA fallback |
| **Static Hosting** | Amazon S3 | Frontend hosting with Origin Access Control (OAC) |
| **Persistent Storage**| Amazon S3 | Private bucket for GR documents and event photos |
| **API Ingress** | AWS Application Load Balancer | Health checks, path-based routing (`/api/*`, `/uploads/*`) |
| **Compute** | AWS ECS Fargate | Serverless Docker container runtime |
| **Container Registry**| Amazon ECR | Docker image repository with lifecycle cleanup |
| **CI/CD Pipeline** | GitHub Actions | Automated build, test, push, and deployment on push to `main` |
| **IaC** | Terraform >= 1.5.0 | Modular infrastructure provisioning suite |

---

## Project Directory Structure

```
ShalaConnect/
├── .github/
│   └── workflows/
│       └── deploy.yml                      # GitHub Actions automated CI/CD pipeline
├── backend/                                # Spring Boot 21 REST API
│   ├── src/main/java/com/shalaconnect/
│   │   ├── config/                         # SecurityConfig, WebConfig, AppConfig, DataSeeder
│   │   ├── controller/                     # REST endpoints (Attendance, Events, GR, Forms, etc.)
│   │   ├── dto/request/                    # Incoming JSON payloads & validations
│   │   ├── dto/response/                   # Standardized JSON response wrappers
│   │   ├── exception/                      # GlobalExceptionHandler, ResourceNotFound, BadRequest
│   │   ├── model/                          # JPA Entities (School, User, Attendance, Event, etc.)
│   │   ├── repository/                     # Spring Data JPA interfaces & custom JPQL queries
│   │   ├── security/                       # JwtAuthFilter, JwtUtil
│   │   ├── service/impl/                   # Business logic implementations
│   │   └── util/                           # FileStorageService (local & S3 storage adapter)
│   ├── src/main/resources/
│   │   └── application.properties          # Spring configuration & environment mappings
│   ├── Dockerfile                          # Multi-stage Maven build → Temurin JRE 21 Alpine
│   └── pom.xml                             # Maven project dependencies
├── frontend/                               # React 18 + Vite SPA
│   ├── src/
│   │   ├── components/layout/              # DashboardLayout, ProtectedRoute
│   │   ├── components/ui/                  # ErrorBoundary, Modal, ConfirmDialog, StatCard, etc.
│   │   ├── context/                        # AuthContext, LanguageContext (Marathi / English)
│   │   ├── hooks/                          # Custom useApi hook
│   │   ├── pages/admin/                    # Admin Dashboard, Schools, Attendance, Meetings, etc.
│   │   ├── pages/headmaster/               # HM Dashboard, Submit Attendance, Profile, Events, etc.
│   │   ├── pages/auth/                     # LoginPage
│   │   ├── pages/public/                   # PublicPortal, PublicSchoolDetail
│   │   ├── services/api.js                 # Axios instance with auth interceptors
│   │   ├── App.jsx                         # React router, ErrorBoundary, LanguageProvider
│   │   ├── index.css                       # Tailwind layers & typography (Plus Jakarta + Devanagari)
│   │   └── main.jsx                        # React root mount
│   ├── nginx.conf                          # Nginx reverse proxy (for Docker container deployment)
│   ├── Dockerfile                          # Node build → Nginx Alpine runtime
│   └── package.json                        # Frontend dependencies
├── terraform/                              # Modular AWS Terraform Suite
│   ├── main.tf, variables.tf, outputs.tf   # Provider configuration, parameters & outputs
│   ├── vpc.tf, security_groups.tf          # Multi-AZ VPC & least-privilege security groups
│   ├── alb.tf, ecs.tf, ecr.tf              # ALB, ECS Fargate & ECR repository
│   ├── rds.tf, s3.tf, cloudfront.tf        # PostgreSQL RDS, S3 buckets & CloudFront CDN
│   ├── terraform.tfvars.example            # Example configuration variables
│   └── README.md                           # Terraform deployment walkthrough
├── database/
│   └── init.sql                            # Initial database setup script
├── docker-compose.yml                      # Local full-stack development orchestration
└── README.md                               # Project documentation
```

---

## Roles & Permissions

| Role | Target User | Permitted Actions |
| :--- | :--- | :--- |
| **`ADMIN`** | Cluster Head (केंद्र प्रमुख) | Full cluster access: manage schools, assign headmasters, create meetings/events/GRs, create dynamic forms, view all attendance, export BEO reports, and manage user accounts. |
| **`HEADMASTER`** | School Headmaster (मुख्याध्यापक) | School-scoped access: submit daily attendance for assigned school, acknowledge cluster meetings, mark GRs as read, submit event implementations and photos, respond to dynamic forms, and view school profile. |
| **`PUBLIC`** | General Public / Parents | Unauthenticated access: search schools by name/village/UDISE, view school facilities, enrollment, topper achievements, and public attendance stats. |

---

## Complete REST API Reference

**Base URL**: `/api`  
**Authentication Header**: `Authorization: Bearer <jwt_token>` (required for all protected routes)

### 1. Authentication — `/api/auth`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/login` | Public | Authenticates credentials, returns JWT token & user profile |
| `GET` | `/auth/me` | Authenticated | Fetches currently authenticated user and school context |
| `POST` | `/auth/register-headmaster` | `ADMIN` | Creates a new headmaster user account |
| `POST` | `/auth/change-password` | Authenticated | Changes current user password |

### 2. Schools — `/api/schools`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/schools` | Public | Lists all active schools with staff and student counts |
| `GET` | `/schools/{id}` | Public | Retrieves comprehensive school details by ID |
| `POST` | `/schools` | `ADMIN` | Registers a new school (validates unique UDISE code) |
| `PUT` | `/schools/{id}` | `ADMIN` | Updates school metadata, address, contact, or topper info |
| `POST` | `/schools/{id}/photo` | `ADMIN` | Uploads school facade photograph (multipart) |
| `DELETE` | `/schools/{id}` | `ADMIN` | Soft-deletes a school (`active = false`) |
| `DELETE` | `/schools/{id}/headmaster` | `ADMIN` | Unlinks assigned headmaster from a school |

### 3. Attendance — `/api/attendance`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/attendance` | `HEADMASTER` | Submits daily attendance (validates assigned school ownership) |
| `PUT` | `/attendance/{id}` | `ADMIN`, `HEADMASTER` | Updates attendance record (enforces school tenancy) |
| `GET` | `/attendance/school/{schoolId}` | Public | Fetches attendance history for a specific school |
| `GET` | `/attendance/school/{schoolId}/range?start=&end=` | Public | Fetches date-range attendance for a specific school |
| `GET` | `/attendance/date/{date}` | Authenticated | Lists attendance status across all cluster schools for a date |
| `GET` | `/attendance/summary` | Authenticated | Aggregates daily and 30-day cluster attendance percentages |
| `GET` | `/attendance/export-monthly?year=&month=` | `ADMIN` | Generates and downloads official BEO Monthly Cluster Attendance Excel sheet (`.xlsx`) |

### 4. Government Resolutions (GR) — `/api/gr`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/gr` | Authenticated | Lists all published GR documents |
| `GET` | `/gr/{id}` | Authenticated | Retrieves specific GR document details |
| `POST` | `/gr` | `ADMIN` | Uploads a new GR document or circular PDF (multipart) |
| `POST` | `/gr/{id}/seen` | `HEADMASTER` | Marks GR circular as read/acknowledged by headmaster |
| `DELETE` | `/gr/{id}` | `ADMIN` | Soft-deletes a GR document |

### 5. Cluster Meetings — `/api/meetings`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/meetings` | Authenticated | Lists all active meetings sorted by scheduled date |
| `GET` | `/meetings/upcoming` | Authenticated | Filters upcoming meetings |
| `GET` | `/meetings/{id}` | Authenticated | Gets meeting agenda, venue, and acknowledgment list |
| `POST` | `/meetings` | `ADMIN` | Schedules a new cluster review meeting |
| `PUT` | `/meetings/{id}` | `ADMIN` | Updates meeting details |
| `POST` | `/meetings/{id}/acknowledge` | `HEADMASTER` | Acknowledges meeting attendance |
| `DELETE` | `/meetings/{id}` | `ADMIN` | Soft-deletes/cancels a meeting |

### 6. Events & Celebrations — `/api/events`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/events` | Public | Lists all active events announced in the cluster |
| `GET` | `/events/{id}` | Public | Gets event details and participating schools |
| `POST` | `/events` | `ADMIN` | Announces a new celebration, sports, or cultural event |
| `PUT` | `/events/{id}` | `ADMIN` | Modifies event information |
| `DELETE` | `/events/{id}` | `ADMIN` | Soft-deletes an event |
| `GET` | `/events/{id}/implementations` | Public | Views all school implementation reports and photo proof |
| `GET` | `/events/school/{schoolId}/implementations` | Public | Views all event implementation reports and photos for a specific school |
| `GET` | `/events/{id}/my-implementation` | `HEADMASTER` | Views own school's implementation status |
| `POST` | `/events/{id}/implement` | `HEADMASTER` | Submits school event report and activity notes |
| `POST` | `/events/{id}/implement/photo` | `HEADMASTER` | Uploads photographic proof for event implementation |

### 7. Dynamic Data Forms — `/api/forms`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/forms` | Authenticated | Lists all active dynamic survey forms |
| `GET` | `/forms/{id}` | Authenticated | Gets form schema, questions, and submission status |
| `POST` | `/forms` | `ADMIN` | Creates dynamic form with JSON field configuration |
| `POST` | `/forms/{id}/respond` | `HEADMASTER` | Submits answers to dynamic form questions |
| `GET` | `/forms/{id}/export` | `ADMIN` | Exports all submitted school responses to Excel (`.xlsx`) |
| `DELETE` | `/forms/{id}` | `ADMIN` | Deactivates a dynamic form |

### 8. User Management — `/api/users`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/users` | `ADMIN` | Lists all users with school association |
| `GET` | `/users/headmasters` | `ADMIN` | Lists all registered headmaster accounts |
| `PATCH` | `/users/{id}/assign-school` | `ADMIN` | Assigns or unassigns a school to a headmaster account |
| `PATCH` | `/users/{id}/toggle-active` | `ADMIN` | Activates or deactivates user login |
| `DELETE` | `/users/{id}` | `ADMIN` | Deletes user (or safe soft-delete if audit records exist) |

### 9. Notifications — `/api/notifications`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/notifications` | Authenticated | Fetches user notifications sorted by recent |
| `GET` | `/notifications/unread-count` | Authenticated | Gets count of unread notifications |
| `PATCH` | `/notifications/{id}/read` | Authenticated | Marks a single notification as read |
| `PATCH` | `/notifications/read-all` | Authenticated | Marks all user notifications as read |

### 10. Health Check — `/api/health`
| Method | Endpoint | Role | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Public | Returns service status `UP` (for ECS and Docker health checks) |

---

## Database Schema & Entities

- **`users`**: `id`, `name`, `email` (unique), `password` (BCrypt), `role` (`ADMIN`, `HEADMASTER`), `school_id`, `active`.
- **`schools`**: `id`, `name`, `udise_code` (unique), `address`, `village`, `taluka`, `district`, `pincode`, `phone`, `email`, `total_students`, `total_teachers`, `school_photo`, `active`.
- **`attendance_records`**: `id`, `school_id`, `submitted_by`, `attendance_date`, `total_students`, `present_students`, `absent_students`, `total_teachers`, `present_teachers`, `attendance_percentage`, `remarks`.
- **`gr_documents`**: `id`, `title`, `description`, `gr_number`, `file_name`, `file_path`, `file_size`, `uploaded_by`, `active`, `created_at`.
- **`gr_document_seen`**: `gr_document_id`, `user_id` (tracking read receipts).
- **`meetings`**: `id`, `title`, `agenda`, `scheduled_at`, `meeting_type` (`OFFLINE`, `ONLINE`), `venue`, `meeting_link`, `created_by`, `active`.
- **`meeting_acknowledgments`**: `meeting_id`, `user_id` (headmaster attendance confirmations).
- **`events`**: `id`, `title`, `description`, `event_date`, `venue`, `event_type`, `created_by`, `active`.
- **`event_implementations`**: `id`, `event_id`, `school_id`, `submitted_by`, `description`, `implemented_at`.
- **`event_impl_photos`**: `implementation_id`, `photo_path` (collection of photos proving implementation).
- **`dynamic_forms`**: `id`, `title`, `description`, `fields_json` (TEXT), `deadline`, `created_by`, `active`.
- **`form_responses`**: `id`, `form_id`, `submitted_by`, `school_id`, `answers_json` (TEXT), `submitted_at`.
- **`notifications`**: `id`, `user_id`, `title`, `message`, `type`, `reference_id`, `reference_type`, `read`, `created_at`.

---

## Local Development (Docker Compose)

### 1. Clone & Setup Environment
```bash
git clone https://github.com/YashSabale01/ShalaConnect.git
cd ShalaConnect

cp .env.example .env
```

### 2. Start Services
```bash
docker compose up -d --build
```

### 3. Service Access
| Service | Local Address |
| :--- | :--- |
| **Frontend Portal** | `http://localhost` |
| **Backend REST API** | `http://localhost:8080/api` |
| **PostgreSQL Database** | `localhost:5432` |

**Default Admin Credentials**:
- Email: `admin@shalaconnect.in`
- Password: `Admin@123`

---

## AWS Production Deployment with Terraform

The infrastructure is 100% codified in [`terraform/`](./terraform/).

### Step 1: Provision Infrastructure with Terraform
```bash
cd terraform

# Copy example variables
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your secrets:
# - db_password
# - jwt_secret
# - admin_password

terraform init
terraform plan
terraform apply
```

Upon completion, Terraform outputs:
- `cloudfront_url`: Your public application URL.
- `cloudfront_distribution_id`: CloudFront ID for cache invalidation.
- `frontend_s3_bucket`: S3 bucket name for React SPA build.
- `ecr_repository_url`: ECR repository for Spring Boot Docker images.
- `ecs_cluster_name`: ECS cluster name (`shalaconnect-prod-cluster`).
- `ecs_service_name`: ECS service name (`shalaconnect-prod-service`).

### Step 2: Configure GitHub Repository Secrets
To enable automated CI/CD on every `git push`, add these 5 secrets in **GitHub Repo Settings $\to$ Secrets and variables $\to$ Actions**:

| Secret Name | Source / Value |
| :--- | :--- |
| `AWS_ACCESS_KEY_ID` | Your AWS IAM deployment user Access Key |
| `AWS_SECRET_ACCESS_KEY`| Your AWS IAM deployment user Secret Key |
| `FRONTEND_S3_BUCKET` | Terraform output: `frontend_s3_bucket` |
| `CLOUDFRONT_DISTRIBUTION_ID` | Terraform output: `cloudfront_distribution_id` |
| `ECR_REPOSITORY` | `shalaconnect-backend` |

### Step 3: Automated Deployments
From now on, every time you push code to `main`:
```bash
git push origin main
```
GitHub Actions will automatically build the backend Docker image, push it to ECR, deploy to ECS Fargate, build the frontend SPA, sync it to S3, and invalidate CloudFront edge caches. Zero manual steps!
