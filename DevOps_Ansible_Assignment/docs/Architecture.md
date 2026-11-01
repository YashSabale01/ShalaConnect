# SYSTEM ARCHITECTURE SPECIFICATION
## ShalaConnect DevOps & Ansible Automation Platform (Java Spring Boot)
**Student:** Yash Janardan Sabale | **PRN:** 2310423T26-27 | **MIT Academy of Engineering, Pune**

---

### Architectural Overview
The ShalaConnect DevOps automation architecture is built on an **agentless, push-based model** that orchestrates application configuration across cloud Linux servers using Ansible over OpenSSH (Port 22) to deploy the **Java 21 Spring Boot 3.2.3 Backend**.

```
+---------------------------------------------------------------------------------------+
|                                END-TO-END SYSTEM TOPOLOGY                             |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  [Developer] --------> [GitHub Repository] --------> [Jenkins CI Server]              |
|                             (SCM)                     (Maven Clean Package)           |
|                                                                   |                   |
|                                                                   v                   |
|                                                      [Ansible Control Node]           |
|                                                        - ansible.cfg                  |
|                                                        - inventory/inventory.ini      |
|                                                        - roles/springboot_app         |
|                                                                   |                   |
|                                                                   | SSH (Port 22)     |
|                                                                   v                   |
| +-----------------------------------------------------------------------------------+ |
| | AWS EC2 Cloud Target Instance (Ubuntu 22.04 LTS)                                  | |
| |                                                                                   | |
| |   [Nginx Reverse Proxy (Port 80)]                                                 | |
| |        |                                                                          | |
| |        | proxy_pass http://127.0.0.1:8080                                         | |
| |        v                                                                          | |
| |   [Java 21 Spring Boot Backend (Port 8080)] <--- Managed by Linux systemd         | |
| |        |                                                                          | |
| |        v                                                                          | |
| |   [Health Probe: /api/health] --------> [Continuous Monitoring & Telemetry]        | |
| +-----------------------------------------------------------------------------------+ |
|                                                                                       |
+---------------------------------------------------------------------------------------+
```

---

### Component Breakdown

#### 1. Source Code & Configuration Repository (GitHub)
- Houses all Java Spring Boot backend source code (`pom.xml`, controllers, services, entities, security filters).
- Stores declarative Ansible playbooks, roles, inventory files, and configuration templates.
- Enforces branch protection, pull request reviews, and cryptographic commit signing.

#### 2. Continuous Integration Server (Jenkins)
- Detects commits via GitHub Webhooks.
- Executes `mvn clean package -DskipTests=false` to compile bytecode and run JUnit test suites.
- Packages the production executable fat JAR (`shalaconnect-backend-1.0.0.jar`).
- Triggers the Ansible Control Node upon successful artifact validation.

#### 3. Ansible Control Node
- Operates on Linux/WSL2 without requiring external daemon infrastructure.
- Reads global configurations from `ansible.cfg`.
- Resolves managed target hostnames and variables from `inventory/inventory.ini`.
- Executes tasks sequentially using idempotent Ansible modules (`apt`, `user`, `file`, `template`, `systemd`, `uri`).

#### 4. Target Infrastructure (AWS EC2 Managed Nodes)
- Ubuntu 22.04 LTS virtual instances hosted in public/private subnets.
- OpenJDK 21 LTS runtime and PostgreSQL client packages installed.
- Dedicated service user (`appuser`) without administrative shell privileges.
- Hardened `systemd` daemon managing process lifetimes, crashes, and reboots.
- High-performance Nginx reverse proxy terminating public HTTP traffic on port 80 and forwarding requests to internal port 8080.

#### 5. Verification & Telemetry Subsystem
- Real-time telemetry exposed via `GET /api/health`.
- Validated programmatically within the deployment playbook using `ansible.builtin.uri`.
- Feeds uptime, memory allocation, and response latency to external monitoring tools (CloudWatch, Prometheus).
