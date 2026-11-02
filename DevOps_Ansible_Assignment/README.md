# ShalaConnect: Ansible Automation & Configuration Management
## Enterprise Automated Deployment Pipeline for Java 21 / Spring Boot 3.2 on AWS EC2 & Linux
**Student Name:** Yash Janardan Sabale | **PRN:** 2310423T26-27  
**Department:** Computer Engineering | **Institution:** MIT Academy of Engineering, Alandi, Pune  

---

## 📌 Executive Summary

This repository contains the production-grade **Ansible Configuration Management & Continuous Deployment** automation suite for the **ShalaConnect** educational platform. 

It completely eliminates manual server provisioning, human configuration errors, and environment drift. Using declarative, agentless Ansible automation, it sets up target environments from bare-metal Linux/AWS EC2 to a fully operational, monitored Spring Boot production microservice behind an Nginx reverse proxy in under 2 minutes.

### Key Architectural Highlights
- **100% Agentless & Secure:** Communicates over OpenSSH (Port 22) using standard Python runtime on managed nodes.
- **Idempotent Execution:** Running playbooks repeatedly produces `changed=0`, ensuring zero configuration drift.
- **Enterprise Modular Roles:** Follows official Ansible best practices with dedicated `tasks`, `handlers`, `templates`, `defaults`, and `vars`.
- **Zero-Downtime Service Supervisor:** Configures hardened Linux `systemd` daemons with auto-restart policies and unprivileged system users (`appuser`).
- **Production Edge Proxy:** Implements Nginx reverse proxy (Port 80 ➔ 8080) with client header forwarding and Gzip compression.
- **Automated Health Probing:** Built-in HTTP 200 telemetry assertions against `/api/health` before completing deployment.

---

## 📁 Repository Directory Structure

Only clean, absolute project files are maintained here:

```
DevOps_Ansible_Assignment/
│
├── README.md                            # Master Architecture & Explanation Guide
├── ansible.cfg                          # Global Ansible runtime configuration
│
├── inventory/                           # Target host definitions & groupings
│   ├── inventory.ini                    # Multi-environment unified inventory
│   ├── inventory_aws_ec2.ini            # AWS EC2 production instances
│   └── inventory_local.ini              # Localhost / WSL2 development inventory
│
├── playbooks/                           # Declarative orchestration playbooks
│   ├── site.yml                         # Master entry point (orchestrates complete deployment)
│   ├── install_dependencies.yml         # Standalone: OpenJDK 21, Maven, PostgreSQL client
│   ├── deploy_application.yml           # Standalone: App directories, JAR transfer & systemd
│   ├── configure_nginx.yml              # Standalone: Nginx reverse proxy configuration
│   └── verify_deployment.yml            # Standalone: Health probe & telemetry assertions
│
├── roles/                               # Enterprise modular role hierarchy
│   └── springboot_app/                  
│       ├── defaults/main.yml            # Overridable default variables (ports, paths, versions)
│       ├── vars/main.yml                # OS-specific packages & internal constants
│       ├── meta/main.yml                # Role metadata & supported platforms
│       ├── tasks/                       # Modular task breakdown
│       │   ├── main.yml                 # Master task coordinator
│       │   ├── setup_environment.yml    # APT updates, OpenJDK 21 & Nginx packages
│       │   ├── deploy_code.yml          # Directory creation, JAR transfer & configs
│       │   ├── configure_service.yml    # Linux systemd service unit registration
│       │   ├── configure_nginx.yml      # Nginx virtual host setup & symlinking
│       │   └── verify_health.yml        # HTTP /api/health probe assertion
│       ├── handlers/
│       │   └── main.yml                 # Event-driven systemd & Nginx restart handlers
│       └── templates/                   # Dynamic Jinja2 configuration templates
│           ├── app.service.j2           # Systemd unit file template
│           ├── nginx_site.conf.j2       # Nginx reverse proxy server block template
│           ├── application-prod.properties.j2  # Spring Boot production settings
│           └── app_env.j2               # Environment variables template
│
├── application/                         # Application source code
│   ├── README.md                        # Maven packaging instructions
│   ├── pom.xml                          # Maven build dependencies & plugins
│   └── ShalaConnectBackendServer.java   # Spring Boot 3.2.3 microservice with /api/health
│
├── diagrams/                            # Visual architecture workflows
│   ├── devops_architecture.png          # System interaction & control node flow
│   ├── devops_lifecycle.png             # 8-stage closed-loop DevOps lifecycle
│   └── ansible_workflow.png             # Control node to target nodes push execution
│
└── docs/                                # In-depth technical documentation
    ├── Architecture.md                  # Comprehensive architectural design document
    ├── Execution_Guide.md               # Step-by-step setup & execution walkthrough
    ├── Workflow.md                      # Pipeline stages, idempotency & rollback procedures
    ├── DevOps_Case_Study.md             # Theoretical analysis, benefits & comparisons
    └── Viva_Voce_Guide.md               # 25 Technical Interview & Viva Voce Q&As
```

---

## 🛠️ Deep Dive: Project File Explanations

When explaining this project to an evaluator, interviewer, or client, use this structure:

### 1. Global Configuration (`ansible.cfg`)
Sets up project-level defaults:
- Points to the default inventory file.
- Disables `host_key_checking` so automated scripts do not block on interactive SSH prompts.
- Configures privilege escalation (`become = True`, `become_method = sudo`) so administrative tasks run seamlessly without interactive password prompts.

### 2. Inventory Files (`inventory/`)
Separates environments cleanly:
- **`inventory_aws_ec2.ini`**: Defines production AWS EC2 public IPs, `ansible_user=ubuntu`, and the SSH private key path (`ansible_ssh_private_key_file`).
- **`inventory_local.ini`**: Uses `ansible_connection=local` to allow testing on a local Linux or WSL2 machine without needing external cloud instances.
- **`inventory.ini`**: Grouped configuration supporting multiple tiers (`[webservers]`, `[appservers]`, `[dbservers]`).

### 3. Master Playbook (`playbooks/site.yml`)
The single entry point for deployment. It targets the managed group (`all` or `app_servers`), verifies connectivity, applies the `springboot_app` role, and runs post-deployment verification.

### 4. Modular Role (`roles/springboot_app/`)
Enforces the single responsibility principle:
- **`tasks/setup_environment.yml`**: Updates the package index, installs OpenJDK 21, Maven, PostgreSQL client, and Nginx.
- **`tasks/deploy_code.yml`**: Creates a dedicated system user (`appuser`), creates `/opt/shalaconnect-app`, copies the compiled JAR, and deploys `.env` and `application-prod.properties`.
- **`tasks/configure_service.yml`**: Renders `app.service.j2` into `/etc/systemd/system/shalaconnect.service`, reloads systemd daemon, and enables the service.
- **`tasks/configure_nginx.yml`**: Renders `nginx_site.conf.j2` into `/etc/nginx/sites-available/`, enables the site, and tests Nginx syntax.
- **`tasks/verify_health.yml`**: Queries `http://127.0.0.1:8080/api/health` with automatic retries, ensuring the application is up and running.
- **`handlers/main.yml`**: Restarts `shalaconnect` and reloads `nginx` only when their configuration templates change.

### 5. Application Source (`application/`)
Contains the Spring Boot backend (`ShalaConnectBackendServer.java`) and `pom.xml`. The executable artifact can be built locally using `mvn clean package`.

---

## 🚀 Execution & Verification Commands

### Step 1: Validate Host Connectivity (Ad-Hoc Ping)
```bash
ansible all -i inventory/inventory_aws_ec2.ini -m ping
```

### Step 2: Validate Playbook Syntax
```bash
ansible-playbook -i inventory/inventory_aws_ec2.ini playbooks/site.yml --syntax-check
```

### Step 3: Execute Full End-to-End Deployment
```bash
ansible-playbook -i inventory/inventory_aws_ec2.ini playbooks/site.yml
```

### Step 4: Verify Idempotency (Zero Changes on Re-Run)
```bash
ansible-playbook -i inventory/inventory_aws_ec2.ini playbooks/site.yml
# Expected Play Recap: changed=0, failed=0
```

### Step 5: Test Live Application Endpoint
```bash
curl -i http://<YOUR_TARGET_IP>/api/health
```
**Expected HTTP 200 Output:**
```json
{
  "status": "UP",
  "application": "ShalaConnect Backend",
  "version": "1.0.0",
  "environment": "production",
  "runtime": {
    "javaVersion": "21",
    "jvmVendor": "Eclipse Adoptium / OpenJDK",
    "freeMemoryBytes": 184549376,
    "totalMemoryBytes": 268435456
  },
  "database": {
    "status": "CONNECTED",
    "provider": "PostgreSQL 16"
  }
}
```

---

## 📚 Technical Documentation & Viva Preparation
- **Architecture & Security:** See [`docs/Architecture.md`](./docs/Architecture.md)
- **Deployment Workflow & Idempotency:** See [`docs/Workflow.md`](./docs/Workflow.md)
- **Detailed Execution Guide:** See [`docs/Execution_Guide.md`](./docs/Execution_Guide.md)
- **Theoretical Case Study:** See [`docs/DevOps_Case_Study.md`](./docs/DevOps_Case_Study.md)
- **25 Viva Voce Examination Questions & Answers:** See [`docs/Viva_Voce_Guide.md`](./docs/Viva_Voce_Guide.md)
