# IA Activity No. 3: Jenkins CI/CD + Terraform Mini Project
## Automated Multi-Stage Continuous Integration / Continuous Deployment Pipeline and Modular Cloud Infrastructure as Code for ShalaConnect
**Course:** DevOps & Cloud Engineering | **Academic Year:** 2026–2027  
**Department:** Department of Computer Engineering  
**Institution:** MIT Academy of Engineering, Alandi (D), Pune  
**GitHub Repository:** [https://github.com/YashSabale01/ShalaConnect.git](https://github.com/YashSabale01/ShalaConnect.git)

---

### Student Information
- **Student Name:** Yash Janardan Sabale
- **PRN:** 202301040087
- **Course Name:** DevOps & Cloud Engineering (Course ID: 6690)
- **Target Application:** ShalaConnect (Spring Boot 3.2 / Java 21 Cloud-Native Microservice & React Frontend)

---

## 📌 Executive Summary

This project implements an enterprise-grade Continuous Integration / Continuous Deployment (CI/CD) and Infrastructure as Code (IaC) automation architecture for the **ShalaConnect** educational platform.

By integrating **Jenkins** (Declarative Pipeline as Code) with **HashiCorp Terraform** (declarative cloud resource provisioning on AWS), the release process is fully automated from the developer Git commit through build, automated testing, container security scanning, cloud infrastructure planning, and deployment health verification.

---

## 🚀 What We Covered in This Project

### 1. Continuous Integration (CI) Workflow
- **Source Code Management (SCM) Integration:** Integrated with GitHub (`https://github.com/YashSabale01/ShalaConnect.git`) using credential binding and automated triggers (SCM polling `H/5 * * * *` and webhook hooks).
- **Tooling & Environment Sanity:** Configured declarative agents with JDK 21, Maven 3.9, Docker CLI, and Terraform 1.14.
- **Static Code Analysis & Linting:** Automated class compilation and static code audits using Checkstyle and SpotBugs to eliminate code smells and security flaws before test execution.
- **Automated Unit & Integration Testing:** Automated execution of 48 JUnit 5 test cases covering controllers, services, JPA entities, and Spring Security JWT filters. Automated recording and archiving of Surefire test XML reports (`junit '**/target/surefire-reports/*.xml'`).
- **Artifact Packaging & Fingerprinting:** Packaging of the production-ready fat JAR (`shalaconnect-backend-1.0.0.jar`) and archiving as an immutable build artifact.

### 2. Containerization & DevSecOps
- **Multi-Stage Docker Containerization:** Automated building of minimal OCI container images based on `eclipse-temurin:21-jre-alpine`, minimizing attack surface and runtime image footprint.
- **Semantic Image Tagging:** Versioning each container image with both the Jenkins build number and the Git commit SHA (`${BUILD_NUMBER}-${GIT_COMMIT}`), plus a mutable `latest` tag.
- **Container Vulnerability Scanning (Trivy):** Integrated automated CVE vulnerability auditing to inspect container base OS packages and application dependencies for HIGH and CRITICAL vulnerabilities prior to deployment.

### 3. Infrastructure as Code (IaC) with HashiCorp Terraform
- **Modular Architecture:** Structured the cloud infrastructure into 4 isolated, reusable modules under `terraform/modules/`:
  - **`vpc` Module:** Provisions a dual-AZ Virtual Private Cloud (`10.0.0.0/16`) in AWS Mumbai (`ap-south-1`) with 2 Public Subnets, 2 Private Subnets, Internet Gateway, and Route Tables.
  - **`security` Module:** Enforces a 3-tier defense-in-depth security model:
    - *ALB Security Group:* Permits public ingress on HTTP 80 and HTTPS 443.
    - *Application Security Group:* Strictly restricts ingress on port 8080 to traffic originating from the ALB Security Group.
    - *Database Security Group:* Strictly restricts PostgreSQL port 5432 ingress to traffic originating from the Application Security Group.
  - **`database` Module:** Manages a private Amazon RDS PostgreSQL 16 database instance with dedicated DB Subnet Groups, automatic backups, parameter groups, and encrypted storage.
  - **`compute` Module:** Provisions an external Application Load Balancer (ALB), listener rules, target groups with active health checks on `/api/health`, and ECS cluster definitions.
- **Multi-Environment Isolation:** Implemented dedicated environment configurations (`environments/staging` and `environments/production`) with separated variables and state.
- **HCL Syntax & Plan Validation:** Validated via `terraform validate` and `terraform plan`, generating an execution plan adding 18 cloud resources with zero configuration drift.

### 4. Continuous Deployment (CD) & Health Telemetry Verification
- **Automated Staging Deployment:** Automated container lifecycle management—gracefully stopping prior container workloads, pulling updated images, and launching the new release with dynamic environment variables.
- **Automated Smoke Testing:** Automated post-deployment HTTP retry loop validating `/api/health` endpoint returning `HTTP 200 OK` with JSON telemetry confirming application status (`UP`) and database connectivity (`CONNECTED`).
- **Post-Build Pipeline Actions:** Workspace cleanup of temporary build files, test trend aggregation, and deployment notification handling.

---

## 📁 Repository Directory Structure

```
DevOps_Jenkins_Terraform_Assignment/
│
├── Jenkinsfile                                        # Master Declarative Multi-Stage Jenkins Pipeline
├── README.md                                          # Master Project & Implementation Documentation
├── DevOps_IA3_Jenkins_Terraform_Report_Yash_Sabale.pdf # Publication-Grade Academic PDF Report
├── DevOps_IA3_Jenkins_Terraform_Report_Yash_Sabale.docx# Academic Editable Word DOCX Report
│
├── jenkins/                                           # Jenkins Controller & Pipeline Job Configuration
│   ├── Dockerfile.jenkins                             # Custom Jenkins image with Docker, Maven, Terraform
│   ├── docker-compose-jenkins.yml                     # Containerized Jenkins Controller & Docker-in-Docker setup
│   └── config/
│       ├── config.xml                                 # Jenkins Pipeline Job definition XML
│       ├── jenkins_casc.yaml                          # Jenkins Configuration as Code (JCasC) definition
│       └── plugins.txt                                # Pre-installed Jenkins plugin manifest
│
├── terraform/                                         # Modular Infrastructure as Code
│   ├── main.tf                                        # Root Terraform orchestrator calling modules
│   ├── provider.tf                                    # AWS Provider configuration & version pinning (ap-south-1)
│   ├── variables.tf                                   # Root variable declarations with types and defaults
│   ├── outputs.tf                                     # Consolidated cloud infrastructure outputs
│   ├── terraform.tfvars                               # Staging configuration parameters
│   ├── terraform.tfvars.example                       # Sample template variable configuration
│   ├── modules/
│   │   ├── vpc/                                       # Multi-AZ VPC, Subnets, IGW, Route Tables
│   │   ├── security/                                  # Layered Security Groups (ALB, App, DB)
│   │   ├── database/                                  # RDS PostgreSQL 16 & DB Subnet Group
│   │   └── compute/                                   # Application Load Balancer & ECS Cluster
│   └── environments/
│       ├── staging/                                   # Dedicated Staging workspace wrapper
│       └── production/                                # Dedicated Production workspace wrapper
│
├── diagrams/                                          # High-Resolution Visual Architecture Diagrams
│   ├── jenkins_cicd_pipeline_architecture.png         # 10-stage automated pipeline architecture
│   ├── terraform_aws_infrastructure_topology.png      # Multi-AZ AWS cloud infrastructure topology
│   ├── jenkins_terraform_integration_flow.png         # Jenkins + Terraform orchestration handshake
│   └── gitops_deployment_lifecycle.png                # GitOps continuous delivery lifecycle
│
├── screenshots/
│   └── execution_evidence/                            # Student execution evidence screenshots
│       └── .gitkeep
│
└── demonstration/
    ├── video_demonstration_script.md                  # Verbatim recording walkthrough script with timestamps
    └── viva_questions_answers.md                      # 25 in-depth technical Viva Voce Q&As
```

---

## 🛠️ Jenkins Pipeline Stages Overview

| Stage | Name | Key Operations Performed |
| :---: | :--- | :--- |
| **1** | **SCM Checkout & Environment Sanity** | Clones repository, validates Git commit SHA, asserts JDK 21, Maven 3.9, Docker, and Terraform. |
| **2** | **Static Code Analysis & Linting** | Runs `mvn compile -DskipTests`, Checkstyle rules, and SpotBugs security audit. |
| **3** | **Automated Unit & Integration Testing** | Runs `mvn test`, executes 48 JUnit 5 test cases, and archives Surefire test XMLs. |
| **4** | **Build & Package Artifact** | Compiles production fat JAR `shalaconnect-backend-1.0.0.jar` with SHA-256 fingerprint. |
| **5** | **Container Image Build & Tagging** | Builds Docker container image tagged with `${BUILD_NUMBER}-${GIT_COMMIT}` and `latest`. |
| **6** | **Container Vulnerability Scanning** | Trivy scans container OS layers and JAR dependencies for HIGH and CRITICAL CVEs. |
| **7** | **Terraform Infrastructure Provisioning** | Executes `terraform init`, `validate`, and `plan` (+18 resources planned for AWS). |
| **8** | **Automated Application Deployment** | Deploys containerized application to the staging environment host. |
| **9** | **Automated Smoke Testing** | Queries `/api/health` via curl retry loop, asserting `HTTP 200 OK` and `"status": "UP"`. |
| **10** | **Post-Build Actions** | Publishes JUnit test results, performs workspace cleanup, and dispatches status notifications. |

---

## ⚡ Execution & Verification Commands

### 1. Validate & Plan Terraform Cloud Infrastructure
```powershell
cd "D:\java\New folder\ShalaConnect\DevOps_Jenkins_Terraform_Assignment\terraform"
terraform init
terraform validate
terraform plan -var="environment=staging"
```

### 2. Launch Website Frontend Portal
```powershell
cd "D:\java\New folder\ShalaConnect\frontend"
npm run dev
# Access via browser at: http://localhost:5173
```

### 3. Verify Backend Health Telemetry Endpoint
```powershell
curl.exe -i http://localhost:8085/api/health
```

---

## 👨‍🎓 Project Metadata & Authentication
- **Student Name:** Yash Janardan Sabale
- **PRN:** 202301040087
- **Institution:** MIT Academy of Engineering, Alandi (D), Pune - 412105
- **Department:** Department of Computer Engineering
- **Academic Year:** 2026–2027
