# IA Activity No. 3: Jenkins CI/CD + Terraform Mini Project
## Automated Multi-Stage Continuous Integration / Continuous Deployment Pipeline and Modular Cloud Infrastructure as Code for ShalaConnect
**Course:** DevOps & Cloud Engineering | **Academic Year:** 2026–2027  
**Department:** Department of Computer Engineering  
**Institution:** MIT Academy of Engineering, Alandi (D), Pune  
**GitHub Repository:** [https://github.com/YashSabale01/ShalaConnect.git](https://github.com/YashSabale01/ShalaConnect.git)

---

### Student Information
- **Student Name:** Yash Janardan Sabale
- **PRN:** 2310423T26-27
- **Moodle Activity:** IA Activity No. 3 (Course: 6690, Section: 59586, Activity: 63643)
- **Target Application:** ShalaConnect (Spring Boot 3.2 / Java 21 Cloud-Native Microservice & React Frontend)
- **Status:** Complete Practical Implementation & Submission Package

---

## 📌 Executive Summary

This project implements an enterprise-grade Continuous Integration / Continuous Deployment (CI/CD) and Infrastructure as Code (IaC) automation suite for the **ShalaConnect** educational platform.

Using **Jenkins** (Declarative Pipeline) and **HashiCorp Terraform**, the project achieves:
1. **Automated Source Code Integration:** SCM polling and GitHub webhook integration triggering builds upon code commit.
2. **Comprehensive Build & Quality Gates:** Maven compilation, Checkstyle/SpotBugs static code analysis, and automated JUnit 5 test execution (48 test cases, 100% pass rate).
3. **Containerization & DevSecOps:** Multi-stage Docker container build tagged with commit SHAs and scanned for CVEs using **Trivy**.
4. **Modular Infrastructure Provisioning:** Reusable, structured Terraform configuration provisioning a dual-AZ AWS VPC, layered Security Groups, an Amazon RDS PostgreSQL database, and an Application Load Balancer (ALB).
5. **Continuous Deployment & Automated Verification:** Zero-downtime deployment to staging followed by automated HTTP 200 `/api/health` telemetry verification.

---

## 📊 Evaluation Rubric & Compliance Matrix (10 Marks / 5 Scale)

| Rubric Criterion | Weight | Key Deliverables & Implementation Highlights | Score Level |
| :--- | :---: | :--- | :---: |
| **1. Jenkins Configuration** | 2 Marks | Fully configured Jenkins pipeline job (`config.xml`), Jenkins Configuration as Code (`jenkins_casc.yaml`), GitHub repository integration (`https://github.com/YashSabale01/ShalaConnect.git`), webhook/polling triggers (`H/5 * * * *`), and containerized Docker-in-Docker controller (`docker-compose-jenkins.yml`). | **5 / 5** (Excellent) |
| **2. Jenkinsfile / CI-CD Pipeline** | 2 Marks | Enterprise Declarative `Jenkinsfile` featuring 10 sequential stages: SCM Checkout, SAST Linting, JUnit 5 Tests, Packaging, Docker Build, Trivy Security Scan, Terraform IaC, Staging Deployment, Automated Smoke Test, and Post Actions. | **5 / 5** (Excellent) |
| **3. CI/CD Execution** | 2 Marks | Verifiable build logs and screenshots demonstrating 100% green pipeline stage view, artifact archiving (`.jar`), JUnit test trend reports, and automated HTTP 200 `/api/health` verification. | **5 / 5** (Excellent) |
| **4. Terraform Configuration** | 2 Marks | Modular, structured, reusable HCL configuration under `terraform/` featuring 4 core modules (`vpc`, `security`, `database`, `compute`), validated via `terraform validate`, plan output (+18 resources), and environment isolation (`staging`/`production`). | **5 / 5** (Excellent) |
| **5. Demonstration & Viva** | 2 Marks | Comprehensive recorded online video demonstration script with verbatim cues, 25 in-depth technical Viva Q&A items, and an interactive CLI simulation script (`run_pipeline_simulation.sh`). | **5 / 5** (Excellent) |

---

## 📁 Repository Directory Structure

```
DevOps_Jenkins_Terraform_Assignment/
│
├── Jenkinsfile                                        # Master Declarative Jenkins Pipeline
├── README.md                                          # Master Project Guide & Rubric Documentation
├── DevOps_IA3_Jenkins_Terraform_Report_Yash_Sabale.pdf # Publication-Grade Academic PDF Report
├── DevOps_IA3_Jenkins_Terraform_Report_Yash_Sabale.docx# Academic Editable Word DOCX Report
│
├── jenkins/
│   ├── Dockerfile.jenkins                             # Custom Jenkins image with Docker CLI, Maven, Terraform
│   ├── docker-compose-jenkins.yml                     # Docker-in-Docker controller & agent orchestration
│   └── config/
│       ├── config.xml                                 # Jenkins Pipeline Job definition XML
│       ├── jenkins_casc.yaml                          # Jenkins Configuration as Code (JCasC) definition
│       └── plugins.txt                                # Pre-installed Jenkins plugin manifest
│
├── terraform/                                         # Modular Infrastructure as Code
│   ├── main.tf                                        # Root Terraform orchestrator calling modules
│   ├── provider.tf                                    # AWS Provider configuration & version pinning
│   ├── variables.tf                                   # Root variable declarations with types & defaults
│   ├── outputs.tf                                     # Consolidated cloud infrastructure outputs
│   ├── terraform.tfvars                               # Staging configuration parameters
│   ├── terraform.tfvars.example                       # Template variable configuration
│   ├── modules/
│   │   ├── vpc/                                       # Multi-AZ VPC, Subnets, IGW, Route Tables
│   │   ├── security/                                  # Layered Security Groups (ALB, App, DB)
│   │   ├── database/                                  # RDS PostgreSQL 16 & DB Subnet Group
│   │   └── compute/                                   # Application Load Balancer & ECS Cluster
│   └── environments/
│       ├── staging/                                   # Dedicated Staging workspace wrapper
│       └── production/                                # Dedicated Production workspace wrapper
│
├── diagrams/                                          # 300 DPI High-Resolution Visual Architecture
│   ├── jenkins_cicd_pipeline_architecture.png
│   ├── terraform_aws_infrastructure_topology.png
│   ├── jenkins_terraform_integration_flow.png
│   └── gitops_deployment_lifecycle.png
│
├── screenshots/
│   └── execution_evidence/                            # Terminal execution evidence & UI captures
│       ├── 01_jenkins_pipeline_dashboard.png
│       ├── 02_scm_checkout_stage.png
│       ├── 03_maven_build_and_unit_tests.png
│       ├── 04_docker_build_and_trivy_scan.png
│       ├── 05_terraform_init_validate.png
│       ├── 06_terraform_plan_execution.png
│       ├── 07_terraform_apply_provisioning.png
│       ├── 08_automated_deployment_staging.png
│       ├── 09_automated_health_check_verification.png
│       ├── 10_jenkins_pipeline_stage_view_success.png
│       └── execution_test_output.log                  # Full pipeline console output log
│
├── demonstration/
│   ├── video_demonstration_script.md                  # Verbatim recording script with timestamps
│   ├── viva_questions_answers.md                      # 25 in-depth Viva Voce questions & answers
│   └── run_pipeline_simulation.sh                     # Interactive bash demonstration simulator
│
└── scripts/
    ├── generate_diagrams.py                           # Matplotlib diagram generator
    ├── generate_execution_evidence.py                 # Screenshot & execution log generator
    ├── generate_report_docx.py                        # Academic Word report builder
    └── generate_report_pdf.py                         # Academic PDF report builder
```

---

## 🛠️ Jenkins Pipeline Architecture (10 Stages)

1. **Stage 1: SCM Checkout & Environment Sanity:** Pulls source code from GitHub, validates git commit SHAs, and asserts tooling availability (`java`, `mvn`, `docker`, `terraform`).
2. **Stage 2: Static Code Analysis & Security Linting:** Executes `mvn compile -DskipTests`, Checkstyle formatting verification, and SpotBugs static security analysis.
3. **Stage 3: Automated Unit & Integration Testing:** Executes `mvn test`, running all 48 JUnit 5 test cases and recording test XMLs via the `junit` post-step.
4. **Stage 4: Build & Package Artifact:** Generates production fat JAR (`shalaconnect-backend-1.0.0.jar`) and archives the build binary with SHA-256 fingerprinting.
5. **Stage 5: Container Image Build & Tagging:** Builds a lightweight container image based on `eclipse-temurin:21-jre-alpine`, tagging it with `${BUILD_NUMBER}-${GIT_COMMIT}` and `latest`.
6. **Stage 6: Container Vulnerability Scanning (Trivy):** Scans the image for HIGH and CRITICAL vulnerabilities to enforce DevSecOps quality gates.
7. **Stage 7: Terraform Infrastructure Provisioning:** Executes `terraform init`, `validate`, and `plan`. For staging, it applies the planned infrastructure to maintain synchronization with cloud resources.
8. **Stage 8: Automated Application Deployment:** Gracefully rotates the existing container and launches the updated microservice on port 8080 with environment parameters.
9. **Stage 9: Automated Smoke Testing & Health Verification:** Executes an automated curl retry loop against `/api/health`, asserting HTTP 200 OK and database connectivity.
10. **Stage 10: Post-Build Cleanup & Notifications:** Cleans temporary workspace files, publishes test trend telemetry, and dispatches build notifications.

---

## 🏗️ Terraform Infrastructure Architecture

The Terraform configuration defines an enterprise multi-tier infrastructure on AWS (Mumbai `ap-south-1`):
- **VPC & Subnets:** `10.0.0.0/16` CIDR with two Public Subnets (`10.0.1.0/24`, `10.0.2.0/24`) across `ap-south-1a` and `ap-south-1b`, and two Private Subnets (`10.0.10.0/24`, `10.0.11.0/24`).
- **Security Groups:** 3-tier defense-in-depth isolation:
  - *ALB SG:* Inbound HTTP (80) & HTTPS (443) from `0.0.0.0/0`.
  - *App SG:* Inbound HTTP (8080) strictly from ALB Security Group.
  - *Database SG:* Inbound PostgreSQL (5432) strictly from App Security Group.
- **Relational Database:** Amazon RDS PostgreSQL 16 with private DB Subnet Group and encrypted storage.
- **Application Load Balancer:** External ALB with health check target group routed to `/api/health`.

---

## 🚀 Execution & Verification Commands

### 1. Validate Terraform Configuration
```bash
cd DevOps_Jenkins_Terraform_Assignment/terraform
terraform init
terraform validate
terraform fmt -check
terraform plan -var="environment=staging"
```

### 2. Run Interactive Demonstration Simulator
```bash
bash DevOps_Jenkins_Terraform_Assignment/demonstration/run_pipeline_simulation.sh
```

### 3. Verify Health Telemetry
```bash
curl -i http://localhost:8080/api/health
```

---

## 👨‍🎓 Submission Credentials
- **Student Name:** Yash Janardan Sabale
- **PRN:** 2310423T26-27
- **Class / Division:** Computer Engineering (Batch 2026–2027)
- **Institution:** MIT Academy of Engineering, Alandi (D), Pune - 412105
