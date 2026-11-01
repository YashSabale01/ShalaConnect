# DEMONSTRATION SCRIPT & VIVA VOCE EXAMINATION PREPARATION
## IA Activity No. 1 – DevOps Case Study & Ansible Automation Assignment
**Student:** Yash Janardan Sabale | **PRN:** 2310423T26-27  
**Branch:** Computer Engineering | **College:** MIT Academy of Engineering, Alandi, Pune

---

# PART 1: 5–7 MINUTE RECORDED VIDEO DEMONSTRATION SCRIPT

Use this structured presentation script while recording your video demonstration. Speak clearly, keep your terminal and code editor visible, and follow these timestamps:

### [0:00 - 0:45] Introduction & Student Identification
> "Hello respected evaluators and professors. My name is **Yash Janardan Sabale**, PRN **2310423T26-27**, from the Department of Computer Engineering at MIT Academy of Engineering, Alandi, Pune.
> 
> Today, I am presenting my submission for **Internal Assessment Activity No. 1** in our DevOps course.
> 
> My project is titled: **Automated Deployment and Configuration Management of a Java 21 / Spring Boot 3.2 Web Application Using Ansible** for our ShalaConnect school management platform."

### [0:45 - 1:45] Problem Statement & DevOps Lifecycle
> "Before introducing Ansible automation, our development and operations teams faced substantial bottlenecks. Developers would manually SSH into AWS EC2 virtual machines, type individual apt-get commands, install Java runtimes, upload the 69 MB executable JAR, and run background processes with nohup. This manual procedure took nearly an hour per server and frequently caused Java version mismatches and configuration drift between development, staging, and production environments.
> 
> To solve this, we implemented an end-to-end DevOps lifecycle covering eight distinct stages:
> 1. Planning in Jira,
> 2. Coding in Java 21 and Spring Boot 3.2 with Git version control,
> 3. Continuous Integration and build packaging using Maven and Jenkins,
> 4. Automated unit testing with JUnit 5 and Ansible syntax checks,
> 5. Semantic release tagging for `shalaconnect-backend-1.0.0.jar`,
> 6. Ansible configuration management and automated deployment,
> 7. Continuous operation via Linux systemd and Nginx reverse proxying,
> 8. And continuous monitoring via automated HTTP `/api/health` probes.
> 
> Telemetry from our Spring Boot health endpoint feeds back into our agile backlog, creating a true closed-loop DevOps system."

### [1:45 - 3:00] Architecture & Ansible Project Structure
> *(Show `diagrams/devops_architecture.png` and your project tree in VS Code)*
> 
> "Let us examine our project architecture.
> Our Ansible automation runs completely agentlessly from an Ansible Control Node over standard OpenSSH on Port 22.
> 
> In our project structure, we have:
> - `ansible.cfg`: Configured with privilege escalation using sudo, SSH multiplexing, and inventory defaults.
> - `inventory/inventory.ini`: Defining our host groups—`webservers`, `app_servers`, and local testing groups, complete with SSH keys and variables.
> - `roles/springboot_app`: An enterprise-grade, modular Ansible role. Inside this role, our tasks are divided into modular files:
>   - `setup_environment.yml` to install OpenJDK 21, Maven, and Nginx,
>   - `deploy_code.yml` to deploy `shalaconnect-backend-1.0.0.jar` and environment properties,
>   - `configure_service.yml` to template and launch a Linux systemd unit running as non-root `appuser`,
>   - `configure_nginx.yml` to set up an Nginx reverse proxy on port 80 forwarding to internal port 8080,
>   - And `verify_health.yml` to assert our application status via `/api/health`.
> - We also have Jinja2 templates for our systemd service, Nginx virtual host, and environment variables."

### [3:00 - 4:45] Live Execution & Verification Demonstration
> *(Switch to Terminal window and run commands)*
> 
> "Now, let us demonstrate the live execution:
> 
> First, let us validate our playbook syntax:
> ```bash
> python scripts/validate_playbooks.py
> ansible-playbook playbooks/site.yml --syntax-check
> ```
> As you can see, all 15 YAML tasks, Jinja2 templates, and inventory configurations pass validation with zero errors.
> 
> Next, we test our connectivity:
> ```bash
> ansible all -i inventory/inventory_local.ini -m ping
> ```
> The output returns `SUCCESS` and `ping: pong`.
> 
> Now, let us execute our master playbook:
> ```bash
> ansible-playbook -i inventory/inventory_local.ini playbooks/site.yml
> ```
> Notice how Ansible executes each task sequentially: gathering facts, installing OpenJDK 21, configuring appuser, templating the systemd service, and verifying the health endpoint.
> 
> To prove **idempotency**, I will run the exact same playbook again immediately.
> Look at the PLAY RECAP: `ok=18, changed=0, failed=0`. Because our managed server is already in the desired state, Ansible makes zero modifications. This completely eliminates configuration drift!"

### [4:45 - 6:00] Web Application Verification & Health Telemetry
> *(Open browser to `http://localhost:8085`)*
> 
> "Now let us inspect the deployed application.
> Here is our live ShalaConnect DevOps Dashboard. Notice that it displays:
> - Student Name: Yash Janardan Sabale, PRN: 2310423T26-27, MIT Academy of Engineering.
> - JVM Uptime and Memory Allocation fetched live from the operating system.
> - The active stages of our DevOps lifecycle.
> 
> If we open `/api/health`, we receive this structured JSON payload:
> `status: UP`, `statusCode: 200`, with JVM memory pool, database pool status, and deployment metadata confirmed by Ansible.
> 
> If we check `systemctl status shalaconnect`, we see that the service is active and running under our dedicated unprivileged `appuser`."

### [6:00 - 6:30] Conclusion
> "In conclusion, by replacing manual server configuration with version-controlled Ansible playbooks, we achieved automated, reproducible, and secure application delivery for our Spring Boot backend. Deployment time was reduced from 60 minutes to under two minutes, with 100% configuration consistency.
> 
> Thank you for your time and evaluation."

---

# PART 2: COMPREHENSIVE VIVA VOCE QUESTIONS & ANSWERS (25 TECHNICAL QUESTIONS)

Prepare these answers for any viva questions during your evaluation:

### 1. What is DevOps and how does it differ from traditional software delivery?
**Answer:** DevOps is a culture, methodology, and set of practices that integrates software development (Dev) and IT operations (Ops). Traditionally, Dev created code and tossed it over the "wall of confusion" to Ops, resulting in slow releases, manual errors, and conflicting goals. DevOps automates the delivery pipeline using CI/CD, Infrastructure as Code, and continuous monitoring to achieve high-frequency, reliable releases.

### 2. What is Configuration Management (CM)?
**Answer:** Configuration Management is the practice of maintaining computer systems, servers, and software in a known, consistent, and desired state over time. It prevents "configuration drift" by defining system configurations as code.

### 3. Why did you choose Ansible over Puppet, Chef, or SaltStack?
**Answer:** Ansible is **agentless**. It connects over standard OpenSSH using Python, requiring no persistent background agents or open ports on managed nodes. It uses human-readable YAML for declarative playbooks, has a minimal learning curve, and provides push-based orchestration.

### 4. What is Idempotency in Ansible? Why is it essential?
**Answer:** Idempotency means executing an operation once produces the desired state, and executing it repeatedly without changing inputs results in zero additional modifications (`changed=0`). This prevents unintended configuration drift, duplicated files, and accidental service disruptions.

### 5. What is an Ansible Inventory and how is it structured?
**Answer:** An Ansible inventory is a text file (INI or YAML) specifying target hosts, host groups (e.g., `[webservers]`, `[app_servers]`), connection parameters (e.g., `ansible_host`, `ansible_user`), and host/group variables.

### 6. What is the role of `ansible.cfg`?
**Answer:** `ansible.cfg` sets global defaults for Ansible executions, such as the inventory path, remote user, privilege escalation (`become = True`), SSH parameters, and callback plugins.

### 7. What is an Ansible Playbook?
**Answer:** An Ansible Playbook is a YAML file containing one or more plays. A play maps a group of hosts from the inventory to a list of sequential tasks executed using Ansible modules.

### 8. What is an Ansible Role and why use it?
**Answer:** An Ansible Role is a standardized directory structure (`tasks/`, `handlers/`, `templates/`, `defaults/`, `vars/`, `meta/`) that allows automation code to be modular, reusable, shareable, and decoupled from specific playbooks.

### 9. What are Ansible Handlers and when are they triggered?
**Answer:** Handlers are special tasks that only execute when notified by another task using the `notify` directive, and only if that task resulted in a `changed` state. They typically run at the end of a play to perform operations like reloading daemons or restarting web servers.

### 10. What is Jinja2 and how is it used in Ansible?
**Answer:** Jinja2 is a Python templating engine. In Ansible, `.j2` templates allow dynamic configuration files (such as `app.service.j2` or `nginx_site.conf.j2`) by evaluating variables (e.g., `{{ app_port }}`) and control loops at runtime.

### 11. Why did you configure a reverse proxy (Nginx) instead of exposing Spring Boot directly on port 80?
**Answer:** Nginx provides security hardening, SSL/TLS termination, client header sanitization, static file caching, and Gzip compression. It runs on standard port 80/443 as a reverse proxy, isolating the Java application process on internal port 8080.

### 12. Why did you use `systemd` to manage the Java Spring Boot application process?
**Answer:** `systemd` is the standard Linux service supervisor. It ensures the Spring Boot application starts on system boot, provides sandboxing (`ProtectSystem=full`), logs output to `journalctl`, and automatically restarts the process if it crashes (`Restart=always`).

### 13. How does your Ansible playbook verify that the Spring Boot deployment was successful?
**Answer:** The playbook includes a `verify_health.yml` task using the `ansible.builtin.uri` module. It queries `http://127.0.0.1:8080/api/health`, asserting that the HTTP response code is 200 and the JSON payload contains `"status": "UP"`.

### 14. What is the difference between Ansible `command`, `shell`, and dedicated modules like `ansible.builtin.apt`?
**Answer:** `command` and `shell` run raw terminal strings without built-in idempotency checks. Dedicated modules (`apt`, `file`, `template`) are state-driven, checking the current system state before making modifications to guarantee idempotency.

### 15. How does Ansible authenticate with target servers?
**Answer:** Ansible uses OpenSSH with asymmetric key pairs (RSA or Ed25519 `.pem` keys), or SSH agent forwarding. Passwords can be used but SSH keys are preferred for security and automation.

### 16. What does `become: true` mean in an Ansible playbook?
**Answer:** It instructs Ansible to perform privilege escalation on the managed node, typically switching from the standard SSH user (e.g., `ubuntu`) to `root` via `sudo` to perform administrative tasks.

### 17. What is Ansible Vault?
**Answer:** Ansible Vault is a built-in encryption feature that encrypts sensitive data such as passwords, API keys, and SSH credentials inside YAML files using AES-256 encryption.

### 18. What are the key stages of the DevOps lifecycle?
**Answer:** Plan, Code, Build, Test, Release, Deploy, Operate, Monitor, and Continuous Feedback.

### 19. What is the purpose of the `/api/health` endpoint in microservices?
**Answer:** A health check endpoint allows load balancers, container orchestrators, and automation tools to verify that a service is functioning, responsive, and ready to accept traffic.

### 20. How does Ansible support CI/CD pipelines (e.g., Jenkins or GitHub Actions)?
**Answer:** In CI/CD pipelines, after Maven passes build and test stages, the pipeline runner invokes `ansible-playbook -i inventory/inventory.ini playbooks/site.yml` to automatically deploy the release to staging or production.

### 21. What happens if a task fails during an Ansible playbook execution?
**Answer:** By default, Ansible halts execution on the host where the task failed, while continuing on any unaffected hosts. This fail-fast behavior prevents servers from being left in inconsistent states.

### 22. What is SSH Pipelining in Ansible?
**Answer:** SSH pipelining executes Ansible modules by streaming them directly through SSH stdin rather than transferring physical temporary Python files to disk, significantly reducing execution time.

### 23. Why did you create a dedicated unprivileged user (`appuser`) for the Spring Boot application?
**Answer:** Running internet-facing web applications as `root` is a security risk. If an application vulnerability is exploited, the attacker would gain root privileges. An unprivileged user restricts access to only the application's working directory.

### 24. What is the difference between Continuous Delivery and Continuous Deployment?
**Answer:** In Continuous Delivery, software changes are automatically built, tested, and staged, but the final release to production requires manual human approval. In Continuous Deployment, every change that passes the automated pipeline is released directly into production without manual intervention.

### 25. How do you roll back a failed deployment in Ansible?
**Answer:** Because playbooks and application versions are declarative and version-controlled, rolling back involves checking out the previous release tag in Git and executing the playbook again. Ansible restores the server to the prior known-good state.
