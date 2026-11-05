# ShalaConnect: Ansible Automation & Configuration Management
## Enterprise Automated Deployment Pipeline for Java 21 / Spring Boot 3.2 on AWS EC2 & Linux

---

### Student & Academic Details
- **Student Name:** Yash Janardan Sabale
- **Permanent Registration Number (PRN):** 2310423T26-27
- **Class & Branch:** Third Year B.Tech – Computer Engineering
- **Department:** Department of Computer Engineering
- **Institution:** MIT Academy of Engineering, Alandi, Pune
- **Course & Activity:** DevOps Engineering – Internal Assessment (IA) Activity No. 1
- **Academic Year:** 2026–2027

---

## 📌 What We Covered & Implemented

### 1. Real-World Application Scenario & System Architecture
- **Application Context:** Selected **ShalaConnect**, a mission-critical school governance platform designed for Cluster Resource Centre (CRC) Heads across Maharashtra to streamline daily student attendance, Government Resolutions (GR), review meetings, and dynamic surveys.
- **Enterprise Tech Stack:** Implemented for a modern 3-tier microservice architecture:
  - **Runtime:** OpenJDK 21 LTS (Amazon Corretto).
  - **Backend Framework:** Spring Boot 3.2.3 (`shalaconnect-backend-1.0.0.jar`).
  - **Persistence Layer:** Spring Data JPA + Hibernate connected to PostgreSQL 15.
  - **Security:** Spring Security 6 with stateless JSON Web Tokens (JWT).
  - **Process Supervisor:** Linux `systemd` with automatic restart policy.
  - **Reverse Proxy:** Nginx 1.30 forwarding public HTTP Port 80 to internal Port 8080.
- **Elimination of Legacy Bottlenecks:** Replaced manual 45-minute SSH installations, configuration drift, and root execution vulnerabilities with automated, auditable, and idempotent Infrastructure as Code.

### 2. Closed-Loop DevOps Lifecycle Design
- Designed and documented an 8-stage continuous feedback loop:
  1. **Plan:** Agile user stories, sprints, and task tracking via Jira.
  2. **Code:** Java 21 microservice source code managed in Git.
  3. **Build:** Automated dependency resolution and fat JAR packaging using Apache Maven.
  4. **Test:** Automated unit testing via JUnit 5 and playbook syntax validation.
  5. **Release:** Semantic versioning and artifact release tagging (`v1.0.0`).
  6. **Deploy:** Declarative, agentless configuration management via Ansible.
  7. **Operate:** Process isolation, resource sandboxing, and supervisor management using `systemd`.
  8. **Monitor:** Continuous telemetry probe polling Spring Boot `/api/health` and Nginx reverse proxy.

### 3. Multi-Node AWS Cloud Infrastructure Topology
- Architected and deployed a canonical **Agentless Push Topology** across AWS EC2 instances in the Mumbai region (`ap-south-1`):
  - **Ansible Control Node (`13.201.133.251`):** Dedicated `t3.micro` instance running Amazon Linux 2023, Ansible Core 2.16+, Git, and Python 3.9, holding playbooks, roles, inventories, and credentials.
  - **Target Managed Application Server (`13.126.181.31`):** Dedicated `t3.micro` instance running Amazon Linux 2023, provisioned agentlessly over OpenSSH (Port 22).

### 4. Multi-Tier Inventory & Configuration Management
- **Centralized Runtime Configuration (`ansible.cfg`):**
  - Configured default remote user as `ec2-user`.
  - Enabled privilege escalation (`become = True`, `become_method = sudo`).
  - Disabled `host_key_checking` for non-blocking automation.
  - Enabled SSH multiplexing (`ControlMaster=auto`, `ControlPersist=60s`) and pipelining for rapid execution.
- **Dedicated Inventories:**
  - `inventory_aws_ec2.ini`: AWS production host definitions, SSH key paths, group memberships (`[app_servers]`, `[webservers]`), and environment variables (`app_port=8080`, `nginx_port=80`).
  - `inventory.ini`: Multi-tier environment inventory.
  - `inventory_local.ini`: Localhost loopback inventory for local development and testing.

### 5. Enterprise Modular Role Architecture (`roles/springboot_app`)
Structured automation logic into an enterprise-grade Ansible Role with single-responsibility tasks:
- **`setup_environment.yml`:** Automated DNF package installation of OpenJDK 21 Corretto, Maven, Nginx, and PostgreSQL 15 Server. Automated PostgreSQL cluster initialization (`postgresql-setup --initdb`), configured `pg_hba.conf` local trust authentication, created the `school_management` database, and provisioned a restricted system user `appuser` (Principle of Least Privilege).
- **`deploy_code.yml`:** Created target directories (`/opt/shalaconnect-app`, `/var/log/shalaconnect`), deployed the executable JAR artifact, and rendered production properties from Jinja2 templates.
- **`configure_service.yml`:** Rendered a hardened `systemd` service unit (`shalaconnect.service`) with auto-restart policies (`Restart=always`, `RestartSec=5`), security sandboxing (`ProtectSystem=full`), and journald logging.
- **`configure_nginx.yml`:** Configured Nginx reverse proxy on Port 80 routing to internal Port 8080, configured upload body size limits (`25M`), client header forwarding, and validated syntax.
- **`verify_health.yml`:** Automated smoke testing polling internal port 8080 and `/api/health` using the URI module, asserting `status == 200` and `status: "UP"`.
- **`handlers/main.yml`:** Event-driven handlers ensuring zero unnecessary service restarts (`systemctl daemon-reload`, `restart shalaconnect`, `restart postgresql`, `reload nginx`).

### 6. Idempotency & Live Execution Verification
- **Verified Zero-Drift Execution:** Master playbook execution completed across all 37 tasks with **0 failures** (`failed=0`). A consecutive re-run verified complete idempotency with **0 changes** (`changed=0`).
- **Verified Database Initialization:** PostgreSQL 15 verified with all 14 JPA domain tables (`users`, `schools`, `attendance_records`, `dynamic_forms`, `events`, etc.) initialized in `school_management`.
- **Live Public Telemetry:** Verified public endpoint at `http://13.126.181.31/api/health` returning **HTTP 200 OK** and payload:
  ```json
  {"status":"UP","service":"ShalaConnect API","timestamp":"2026-11-01T13:02:00.465554011"}
  ```

---

## 📁 Repository Directory Structure

```
DevOps_Ansible_Assignment/
│
├── ansible.cfg                                  # Global Ansible runtime & SSH configuration
├── README.md                                    # Project architecture & implementation summary
│
├── application/                                 # Spring Boot application runtime
│   ├── pom.xml                                  # Maven dependencies & plugins descriptor
│   ├── ShalaConnectBackendServer.java           # Standalone single-file Java 21 runner
│   └── README.md                                # Build & execution guidelines
│
├── diagrams/                                    # 300 DPI Publication-Grade Visualizations
│   ├── devops_lifecycle.png                     # Figure 1: 8-stage continuous feedback loop
│   ├── devops_architecture.png                  # Figure 2: AWS cloud delivery pipeline
│   └── ansible_workflow.png                     # Figure 3: Agentless SSH push topology
│
├── docs/                                        # In-Depth Academic Documentation
│   ├── DevOps_Case_Study.md                     # Comprehensive academic report (24 sections)
│   ├── DEMO_RECORDING_SCRIPT.md                 # 5-8 minute natural video presentation script
│   ├── Architecture.md                          # Cloud system & security architecture specification
│   ├── Workflow.md                              # CI/CD delivery workflow details
│   ├── Execution_Guide.md                       # Step-by-step local & AWS execution manual
│   └── Viva_Voce_Guide.md                       # 25 Technical Interview & Viva Voce Q&As
│
├── inventory/                                   # Target Host Inventories
│   ├── inventory_aws_ec2.ini                    # Dedicated AWS EC2 production inventory
│   ├── inventory.ini                            # Multi-tier unified host groups
│   └── inventory_local.ini                      # Localhost development & loopback inventory
│
├── playbooks/                                   # Declarative Orchestration Playbooks
│   ├── site.yml                                 # Master deployment entry point
│   ├── install_dependencies.yml                 # Standalone dependency installation play
│   ├── deploy_application.yml                   # Standalone artifact deployment play
│   ├── configure_nginx.yml                      # Standalone Nginx reverse proxy play
│   └── verify_deployment.yml                    # Standalone health verification play
│
└── roles/                                       # Enterprise Modular Role Hierarchy
    └── springboot_app/                          
        ├── defaults/main.yml                    # Default configurable variables (ports, paths)
        ├── vars/main.yml                        # Internal package names & constants
        ├── meta/main.yml                        # Role metadata & supported platforms
        ├── tasks/                               # Modular task breakdown
        │   ├── main.yml                         # Master task coordinator
        │   ├── setup_environment.yml            # OpenJDK 21, Maven, PostgreSQL & user setup
        │   ├── deploy_code.yml                  # Directory creation, JAR deploy & properties
        │   ├── configure_service.yml            # Systemd service unit registration
        │   ├── configure_nginx.yml              # Nginx reverse proxy server block
        │   └── verify_health.yml                # Automated HTTP /api/health probe
        ├── handlers/main.yml                    # Event-driven restart & reload handlers
        └── templates/                           # Dynamic Jinja2 configuration templates
            ├── app.service.j2                   # Systemd unit file template
            ├── nginx_site.conf.j2               # Nginx reverse proxy block template
            ├── application-prod.properties.j2   # Spring Boot production settings template
            └── app_env.j2                       # Environment variables template
```

---

## 📚 Academic Submission Deliverables
- **Official Academic Report (PDF):** [`DevOps_IA1_CaseStudy_Report_Yash_Sabale.pdf`](../DevOps_IA1_CaseStudy_Report_Yash_Sabale.pdf)
- **Editable Academic Report (DOCX):** [`DevOps_IA1_CaseStudy_Report_Yash_Sabale.docx`](../DevOps_IA1_CaseStudy_Report_Yash_Sabale.docx)
- **Video Demonstration Recording Script:** [`docs/DEMO_RECORDING_SCRIPT.md`](./docs/DEMO_RECORDING_SCRIPT.md)
- **Viva Voce Examination Questions & Answers:** [`docs/Viva_Voce_Guide.md`](./docs/Viva_Voce_Guide.md)
