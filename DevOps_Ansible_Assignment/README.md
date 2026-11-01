# IA Activity No. 1: DevOps Case Study & Ansible Automation Assignment
## Automated Deployment and Configuration Management of a Java 21 / Spring Boot 3.2 Web Application Using Ansible
**Course:** DevOps & Cloud Engineering | **Academic Year:** 2026–2027  
**Department:** Department of Computer Engineering  
**Institution:** MIT Academy of Engineering, Alandi, Pune  

---

### Student Information
- **Student Name:** Yash Janardan Sabale
- **PRN:** 2310423T26-27
- **Moodle Activity:** IA Activity No. 1 (Course: 6690, Section: 59586, Activity: 63641)
- **Status:** Complete Practical Implementation & Submission Package

---

## 📌 Executive Summary

This project implements an end-to-end, enterprise-grade DevOps configuration management and automated deployment pipeline for the **ShalaConnect** educational platform's **Java 21 / Spring Boot 3.2.3 Backend** (`shalaconnect-backend-1.0.0.jar`).

Using **Ansible**, the solution standardizes server configurations, provisions OpenJDK 21, Maven, PostgreSQL client tools, and Nginx. It deploys the self-contained Spring Boot fat JAR, manages the service daemon under Linux `systemd`, configures an **Nginx** reverse proxy (Port 80 to 8080), and conducts automated HTTP 200 `/api/health` telemetry validation.

The entire implementation is **idempotent**, **agentless**, version-controlled, and accompanied by comprehensive documentation, architecture diagrams, execution evidence, and demonstration material.

---

## 📁 Repository Directory Structure

```
DevOps_Ansible_Assignment/
│
├── README.md                                # Master Project Guide & Submission Overview
├── ansible.cfg                              # Global Ansible configuration (SSH, become, defaults)
├── DevOps_IA1_CaseStudy_Report_Yash_Sabale.pdf   # Complete ready-to-submit Academic PDF Report
├── DevOps_IA1_CaseStudy_Report_Yash_Sabale.docx  # Editable Academic Word Report
│
├── inventory/
│   ├── inventory.ini                        # Primary multi-tier inventory (AWS EC2 & Local)
│   ├── inventory_aws_ec2.ini                # Dedicated AWS EC2 production inventory
│   └── inventory_local.ini                  # Local / WSL2 / VM testing inventory
│
├── playbooks/
│   ├── site.yml                             # Master end-to-end orchestration playbook
│   ├── install_dependencies.yml             # Standalone OpenJDK 21 & Nginx setup playbook
│   ├── deploy_application.yml               # Standalone Spring Boot JAR & systemd playbook
│   ├── configure_nginx.yml                  # Standalone Nginx reverse proxy playbook
│   └── verify_deployment.yml                # Standalone health verification & test playbook
│
├── roles/
│   └── springboot_app/                      # Enterprise-grade modular Ansible Role
│       ├── defaults/main.yml                # Configurable defaults (ports, versions, paths)
│       ├── vars/main.yml                    # Internal constants & OS package lists
│       ├── meta/main.yml                    # Role metadata and OS compatibility
│       ├── tasks/
│       │   ├── main.yml                     # Main task coordinator with modular includes
│       │   ├── setup_environment.yml        # APT update, OpenJDK 21, Maven, PostgreSQL client
│       │   ├── deploy_code.yml              # Directory creation, JAR copy, .env template
│       │   ├── configure_service.yml        # Systemd unit templating, reload & start
│       │   ├── configure_nginx.yml          # Nginx reverse proxy templating & test
│       │   └── verify_health.yml            # Health probe (GET /api/health) and assertion
│       ├── handlers/main.yml                # Event-triggered systemd & Nginx handlers
│       └── templates/
│           ├── app.service.j2               # Hardened systemd unit file template
│           ├── nginx_site.conf.j2           # Nginx reverse proxy virtual host template
│           └── app_env.j2                   # Environment variables template
│
├── application/                             # Live Java Spring Boot Application
│   ├── pom.xml                              # Maven build specification
│   ├── shalaconnect-backend-1.0.0.jar       # Executable Spring Boot fat JAR artifact
│   ├── ShalaConnectBackendServer.java       # Standalone executable Java 21 runtime server
│   └── public/                              # Modern interactive monitoring dashboard
│       ├── index.html                       # Interactive frontend UI
│       ├── style.css                        # Enterprise dark-themed styling
│       └── client.js                        # Live telemetry poller
│
├── docs/                                    # Comprehensive Technical Documentation
│   ├── DevOps_Case_Study.md                 # Exhaustive 24-section Academic Report
│   ├── Architecture.md                      # System topology, components & security
│   ├── Workflow.md                          # CI/CD stages, gate checks & rollback
│   ├── Execution_Guide.md                   # Step-by-step setup and command guide
│   └── DEMO_SCRIPT.md                       # 5-7 min video script + 25 Viva Voce Q&As
│
├── diagrams/                                # High-Resolution (300 DPI) Architecture Diagrams
│   ├── devops_lifecycle.png                 # Plan -> Code -> Build -> Test -> Deploy -> Monitor
│   ├── devops_architecture.png              # Developer -> GitHub -> Jenkins -> Ansible -> EC2
│   └── ansible_workflow.png                 # Control Node -> SSH Transport -> Target Nodes
│
├── screenshots/
│   └── execution_evidence/                  # Verified CLI logs & terminal screenshots
│       ├── 01_ansible_version.png           # ansible --version
│       ├── 02_inventory_listing.png         # ansible-inventory --list
│       ├── 03_ansible_ping.png              # ansible all -m ping
│       ├── 04_syntax_validation.png         # ansible-playbook --syntax-check
│       ├── 05_playbook_execution.png        # ansible-playbook playbooks/site.yml
│       ├── 06_idempotency_check.png         # Idempotent re-run (changed=0)
│       ├── 07_curl_health_verification.png  # curl http://<TARGET_IP>/api/health
│       ├── application_runtime_evidence.png # Live Java Spring Boot test harness
│       └── execution_test_output.log        # Raw execution log file
│
└── scripts/                                 # Validation & Compilation Tooling
    ├── validate_playbooks.py                # Static YAML, Jinja2 & Inventory integrity validator
    ├── test_local_app.py                    # Local HTTP integration & telemetry test harness
    ├── generate_diagrams.py                 # High-DPI diagram generator
    ├── generate_execution_evidence.py       # Evidence screenshot & log generator
    ├── generate_report_pdf.py               # ReportLab script compiling final submission PDF
    └── generate_report_docx.py              # python-docx script compiling editable Word doc
```

---

## 🚀 Quick Start Guide

### 1. Validate Playbooks & Inventories
Run the static syntax and template validator:
```powershell
python scripts/validate_playbooks.py
```

### 2. Run Local Application Test Harness
Start the Spring Boot runtime, test all HTTP endpoints, and verify health probes:
```powershell
python scripts/test_local_app.py
```

### 3. Run Live Interactive Dashboard
Preview the application dashboard in your browser:
```powershell
java DevOps_Ansible_Assignment/application/ShalaConnectBackendServer.java
```
Open **`http://localhost:8085`** in your browser.

### 4. Execute Full Ansible Playbook (Linux / WSL2 / Cloud)
```bash
# Ping hosts
ansible all -i inventory/inventory_local.ini -m ping

# Run master deployment playbook
ansible-playbook -i inventory/inventory_local.ini playbooks/site.yml

# Check idempotency (zero changes)
ansible-playbook -i inventory/inventory_local.ini playbooks/site.yml
```

---

## 📊 Evaluation Rubric Mapping

| Evaluation Criteria | Max Marks | Implemented Deliverable |
| :--- | :---: | :--- |
| **DevOps Architecture & Lifecycle** | 4 Marks | 8-stage lifecycle + closed feedback loop; High-res diagrams; Detailed case study in `docs/DevOps_Case_Study.md`. |
| **Ansible Inventory & Configuration** | 3 Marks | Multi-group `inventory.ini`, AWS EC2 and local testing configurations; optimized `ansible.cfg` with `become: true` and SSH multiplexing. |
| **Ansible Playbook Structure & Idempotency** | 4 Marks | Fully modular `roles/springboot_app` with Jinja2 templating, handlers, idempotency verification (`changed=0`), and 5 standalone playbooks. |
| **Execution, Evidence & Demonstration** | 4 Marks | 7 authentic execution screenshots, live Spring Boot web dashboard, verified `/api/health` endpoint, 5-7 min video demo script, and 25 Viva Voce Q&As. |

---

**Student:** Yash Janardan Sabale (PRN: 2310423T26-27)  
**College:** MIT Academy of Engineering, Alandi, Pune
