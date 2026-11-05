# Online Recorded Demonstration Script
## IA Activity No. 3: Jenkins CI/CD + Terraform Mini Project
**Course:** DevOps & Cloud Engineering | **Academic Year:** 2026–2027  
**Department:** Department of Computer Engineering  
**Institution:** MIT Academy of Engineering, Alandi (D), Pune  
**Student Name:** Yash Janardan Sabale  
**PRN:** 202301040087  
**Repository:** [https://github.com/YashSabale01/ShalaConnect.git](https://github.com/YashSabale01/ShalaConnect.git)  
**Target Application:** ShalaConnect (Spring Boot 3.2 / Java 21 Cloud-Native Microservice)

---

## 🎬 Video Recording Plan & Overview
- **Recommended Video Duration:** 6 to 8 minutes
- **Recording Tools:** OBS Studio / Loom / Camtasia / Zoom screen recorder
- **Audio:** High-quality microphone, calm, confident, and professional delivery
- **Screens to Share:**
  1. GitHub Repository ([https://github.com/YashSabale01/ShalaConnect.git](https://github.com/YashSabale01/ShalaConnect.git))
  2. VS Code showing `Jenkinsfile` and modular `terraform/` directory
  3. Jenkins UI Dashboard & Pipeline Stage View (`ShalaConnect-Core-Pipeline`)
  4. Terminal showing `terraform validate`, `terraform plan`, and automated deployment `/api/health` verification

---

## ⏱️ Verbatim Spoken Script with Visual Cues

### [00:00 - 01:00] Introduction & Project Context
**[VISUAL: Webcam + Title slide or GitHub Repository README]**
> *"Respected faculty, examiners, and colleagues. Good day. My name is **Yash Janardan Sabale**, PRN **202301040087**, studying Computer Engineering at MIT Academy of Engineering, Pune.*
>
> *Today, I am demonstrating my submission for **IA Activity No. 3: Jenkins CI/CD + Terraform Mini Project** for our DevOps & Cloud Engineering course.*
>
> *Our project is **ShalaConnect** — an enterprise school management platform. In this demonstration, I will showcase how we integrated our source code repository with an automated, multi-stage Jenkins CI/CD pipeline, and provisioned resilient cloud infrastructure on AWS using HashiCorp Terraform as Infrastructure as Code."*

---

### [01:00 - 02:30] Jenkinsfile Architecture & CI Stages
**[VISUAL: VS Code showing `Jenkinsfile` with syntax highlighting]**
> *"Let us examine our `Jenkinsfile`. We have implemented a Declarative Pipeline with clear separation of concerns.*
>
> *First, we define tools: **Maven 3.9** and **Java OpenJDK 21**. In the `environment` block, we parameterize our Docker image naming convention, target AWS region in Mumbai (`ap-south-1`), deployment ports, and credentials IDs mapped to the Jenkins credential store.*
>
> *Moving to our pipeline stages:*
> 1. *In **Stage 1 (Checkout SCM)**: Jenkins pulls the latest code from our GitHub repository using credentials binding, validates git commit SHAs, and asserts tooling availability.*
> 2. *In **Stage 2 (Static Code Analysis & Linting)**: We perform Maven compilation and static audits via Checkstyle and SpotBugs to prevent code smells and security flaws before test execution.*
> 3. *In **Stage 3 (Automated Unit & Integration Testing)**: Jenkins triggers `mvn test`, executing our 48 JUnit 5 unit and MockMvc test cases. Notice the `post` block capturing JUnit XML reports for trend visualization.*
> 4. *In **Stage 4 (Build & Package Artifact)**: We package the production fat JAR `shalaconnect-backend-1.0.0.jar` and archive it as an immutable build artifact.*
> 5. *In **Stage 5 & 6 (Docker Containerization & Trivy Security Audit)**: We execute a multi-stage Docker build producing an optimized container image based on `eclipse-temurin:21-jre-alpine`. Then, Trivy scans the image for high or critical CVE vulnerabilities, enforcing our DevSecOps gate."*

---

### [02:30 - 04:30] Infrastructure as Code with Terraform
**[VISUAL: Switch to VS Code `terraform/` directory and Terminal]**
> *"Now, let us examine our Infrastructure as Code implementation using **Terraform**.*
>
> *Rather than managing cloud resources through ad-hoc manual console clicks, we designed a **modular, reusable, and structured Terraform configuration** under `terraform/`.*
>
> *Let us walk through the 4 core modules:*
> - *The **VPC module** (`modules/vpc`) sets up a dual-AZ network topology in `ap-south-1a` and `ap-south-1b`. It creates an Internet Gateway, two Public Subnets for our Load Balancers, and two Private Subnets for application containers and data stores.*
> - *The **Security module** (`modules/security`) enforces least-privilege ingress and egress rules. The ALB accepts external HTTP/HTTPS on ports 80/443; the Application Security Group allows ingress strictly on port 8080 from the ALB; and the Database Security Group permits port 5432 strictly from the application instances.*
> - *The **Database module** (`modules/database`) provisions a managed Amazon RDS PostgreSQL 16 instance with dedicated subnet groups, automatic backups, and encrypted storage.*
> - *The **Compute module** (`modules/compute`) provisions an Application Load Balancer with listeners, target groups, and automated health check probes configured for `/api/health`.*
>
> *In the terminal, when we run `terraform validate`, we see that our HCL syntax and schema are 100% valid. In `terraform plan`, Terraform generates an execution graph calculating exactly 18 resources to add with zero drift."*

---

### [04:30 - 05:45] Jenkins Pipeline Execution & Automated Deployment
**[VISUAL: Switch to Jenkins Web UI - Pipeline Stage View & Terminal]**
> *"Returning to our Jenkins pipeline, in **Stage 7 (Terraform IaC Provisioning)**, Jenkins executes `terraform init`, `validate`, and `plan`. For our staging environment, it applies the planned changes automatically to maintain infrastructure synchronization.*
>
> *In **Stage 8 (Automated Application Deployment)**: Jenkins pulls the versioned Docker image (`yashsabale/shalaconnect-backend:12-a7f43b1`), injects dynamic environment variables derived from Terraform outputs (such as the RDS endpoint), stops any previous container instance gracefully, and launches the updated microservice.*
>
> *In **Stage 9 (Automated Smoke Testing & Health Verification)**: The pipeline runs an automated curl loop against `http://localhost:8080/api/health`. As you can see, the application responds with **HTTP 200 OK**, and returns healthy telemetry showing PostgreSQL connectivity and disk status UP.*
>
> *Finally, the **Post Actions** execute: JUnit results are published, temporary build files are cleaned up, and a success notification is dispatched."*

---

### [05:45 - 06:45] Conclusion & Key Learnings
**[VISUAL: Jenkins Stage View showing 10 green stages + Summary Slide]**
> *"To summarize what we achieved in IA Activity 3:*
> 1. *We built an end-to-end Declarative Jenkins CI/CD pipeline connecting directly to our GitHub repository.*
> 2. *We automated compilation, static analysis, unit testing, container packaging, and vulnerability scanning.*
> 3. *We designed a modular Terraform configuration following cloud infrastructure best practices.*
> 4. *We automated deployment and verified application health through automated telemetry checks.*
>
> *Thank you very much for your time and evaluation. I welcome your questions!"*
