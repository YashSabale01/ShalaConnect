# Comprehensive Viva Voce & Technical Interview Guide
## DevOps Case Study & Ansible Automation for ShalaConnect
**Student:** Yash Janardan Sabale | **PRN:** 2310423T26-27  
**Department:** Computer Engineering | **Institution:** MIT Academy of Engineering, Alandi, Pune

---

## 25 Essential Technical Viva Questions & Answers

Use this guide to master and explain every technical aspect of the Ansible automation architecture, playbooks, roles, and deployment strategy.

---

### 1. What is DevOps and how does it differ from traditional software delivery?
**Answer:**  
DevOps is a set of practices, cultural philosophies, and tools that combines software development (**Dev**) and IT operations (**Ops**). Traditionally, development teams wrote code and tossed it "over the wall" to operations teams for deployment, leading to configuration drift, finger-pointing, and long release cycles. DevOps unifies both disciplines under continuous integration, automated testing, infrastructure as code, and continuous monitoring to achieve high-frequency, reliable releases with zero manual friction.

---

### 2. What is Configuration Management (CM)?
**Answer:**  
Configuration Management is the discipline of maintaining systems, servers, applications, and operating environments in a consistent, known, and reproducible desired state throughout their lifecycle. It eliminates snowflake servers and manual configuration drift by defining infrastructure state declaratively as code.

---

### 3. Why did you choose Ansible over Puppet, Chef, or SaltStack?
**Answer:**  
1. **Agentless Architecture:** Ansible requires no daemons or agents on target machines; it communicates securely over standard OpenSSH (Port 22) using Python.
2. **Declarative YAML Syntax:** Playbooks are human-readable, reducing cognitive load and onboarding overhead.
3. **Idempotency:** Tasks describe the target state rather than a series of commands, preventing side effects during re-runs.
4. **Push-Based Orchestration:** Control nodes push changes on demand, giving developers immediate feedback and control during deployments.

---

### 4. What is Idempotency in Ansible? Why is it essential?
**Answer:**  
Idempotency ensures that executing a playbook once brings the system to the desired state, and executing it repeatedly without changes produces zero modifications (`changed=0`). This prevents accidental service disruptions, duplicated configuration blocks, and corrupt state when re-running playbooks in production.

---

### 5. What is an Ansible Inventory and how is it structured?
**Answer:**  
An inventory defines the managed target nodes. It groups servers logically (e.g., `[webservers]`, `[app_servers]`, `[dbservers]`) and assigns connection variables such as `ansible_host`, `ansible_user`, and `ansible_ssh_private_key_file`. Group variables under `[group_name:vars]` allow shared configuration across multiple nodes.

---

### 6. What is the role of `ansible.cfg`?
**Answer:**  
`ansible.cfg` defines default execution behavior for Ansible. In this project:
- `inventory = ./inventory/inventory.ini` sets the default host file.
- `remote_user = ubuntu` defines the SSH user.
- `host_key_checking = False` disables interactive SSH fingerprint prompts for automated pipelines.
- `[privilege_escalation]` configures `become = True` with `become_method = sudo` for administrative operations.

---

### 7. What is an Ansible Playbook?
**Answer:**  
A playbook is a YAML document containing one or more plays. Each play targets a specific group of hosts from the inventory and executes a sequence of tasks mapped to Ansible modules (e.g., `apt`, `copy`, `template`, `systemd`).

---

### 8. What is an Ansible Role and why use it?
**Answer:**  
An Ansible Role is a standardized directory structure that organizes automation tasks, handlers, variables, defaults, templates, and metadata into modular components. Roles provide:
- Separation of concerns.
- Reusability across multiple environments (dev, staging, prod).
- Clean playbook files that simply invoke the role with parameter overrides.

---

### 9. What are Ansible Handlers and when are they triggered?
**Answer:**  
Handlers are event-driven tasks that execute only when notified by another task using the `notify` directive, and only if that task caused a state change (`changed: true`). Handlers run once at the end of a play, preventing unnecessary service restarts when multiple tasks modify configuration files.

---

### 10. What is Jinja2 and how is it used in Ansible?
**Answer:**  
Jinja2 is a templating engine for Python. In Ansible, `.j2` templates allow dynamic generation of configuration files (such as `app.service.j2` and `nginx_site.conf.j2`) by injecting runtime variables (e.g., `{{ app_port }}`, `{{ java_opts }}`) and conditional logic into static configuration files.

---

### 11. Why configure Nginx as a reverse proxy instead of exposing Spring Boot directly on port 80?
**Answer:**  
1. **Security Hardening:** Running Spring Boot directly on port 80 requires root privileges or complex port forwarding. Nginx runs on port 80 as an unprivileged process and forwards traffic internally to port 8080.
2. **Performance:** Nginx handles HTTP connection keep-alive, client request buffering, and static file caching efficiently.
3. **SSL/TLS Termination:** Nginx can terminate HTTPS certificates without modifying the Java application code.
4. **Header Sanitization:** Nginx adds security headers (`X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`).

---

### 12. Why manage the Spring Boot application using `systemd`?
**Answer:**  
`systemd` is the standard Linux service supervisor. It provides:
- Automatic startup on system boot (`enabled: yes`).
- Automatic crash recovery and restarts (`Restart=always`, `RestartSec=5`).
- Security isolation via dedicated unprivileged service account (`User=appuser`).
- Centralized log streaming and journal indexing via `journalctl -u shalaconnect`.

---

### 13. How does your Ansible playbook verify deployment success?
**Answer:**  
The `verify_health.yml` task uses the `ansible.builtin.uri` module to send an HTTP GET request to `http://127.0.0.1:8080/api/health`. It asserts that:
- The HTTP response status code is `200`.
- The returned JSON payload contains `"status": "UP"`.
- It retries up to 6 times with a 5-second backoff delay to allow the JVM to complete its startup sequence.

---

### 14. What are Ansible Variables and what is variable precedence?
**Answer:**  
Ansible variables store dynamic values (ports, versions, paths). Precedence defines which value wins when defined in multiple places. In our project:
- `defaults/main.yml` provides low-precedence defaults.
- `vars/main.yml` provides higher-precedence internal constants.
- Extra vars passed via CLI (`--extra-vars`) have the highest precedence.

---

### 15. How do you ensure secrets (passwords, tokens) are protected?
**Answer:**  
1. Passwords and database credentials are never hardcoded in git.
2. In production, Ansible Vault (`ansible-vault encrypt`) encrypts sensitive variable files with AES-256.
3. Decryption occurs strictly at runtime using `--vault-password-file` or environment keys.

---

### 16. What is the difference between `ansible.builtin.copy` and `ansible.builtin.template`?
**Answer:**  
- `copy`: Transfers static files byte-for-byte from the control node to the managed node without modification (e.g., JAR files).
- `template`: Parses a Jinja2 template (`.j2`), substitutes variables with evaluated values, and writes the rendered configuration file to the managed node.

---

### 17. How do you test Ansible playbooks for syntax errors before running them on production?
**Answer:**  
Use the built-in syntax validator:
```bash
ansible-playbook playbooks/site.yml --syntax-check
```
And perform a dry-run check without applying changes:
```bash
ansible-playbook playbooks/site.yml --check
```

---

### 18. What is the purpose of tags in Ansible playbooks?
**Answer:**  
Tags allow executing specific subsets of tasks within a large playbook. In our role:
- `tags: [setup, deps]` executes only package installations.
- `tags: [deploy, app]` deploys only the application JAR and properties.
- `tags: [nginx]` applies only Nginx configuration changes.
- `tags: [verify]` runs only health checks.

---

### 19. What is configuration drift and how does Ansible mitigate it?
**Answer:**  
Configuration drift occurs when manual ad-hoc changes (hotfixes, manual config edits) cause production servers to diverge from the documented standard. Ansible mitigates this by enforcing state declaratively: running the playbook overwrites manual drifts and restores the server to the exact desired baseline.

---

### 20. What is an Ansible Ad-Hoc command? When do you use it?
**Answer:**  
An ad-hoc command is a one-line Ansible execution for quick tasks without writing a playbook. Example:
```bash
ansible all -m ping
ansible app_servers -m shell -a "uptime"
```
Used for diagnostics, checking host connectivity, or rebooting servers.

---

### 21. How does Ansible manage permissions and user separation on the target server?
**Answer:**  
The playbook creates a dedicated non-login system user (`appuser`) and group (`appuser`). The application directory `/opt/shalaconnect-app` and log directory `/var/log/shalaconnect` are strictly owned by `appuser:appuser` with `0755` permissions, preventing unauthorized access.

---

### 22. What happens if a task fails during playbook execution?
**Answer:**  
By default, Ansible stops execution on that host immediately and marks it as failed in the Play Recap. Other unaffected hosts continue execution. To handle errors gracefully, Ansible provides `ignore_errors: true`, `failed_when`, and `block/rescue/always` constructs.

---

### 23. What role does Maven play in this DevOps pipeline?
**Answer:**  
Apache Maven manages dependencies, runs automated JUnit tests, and packages the Spring Boot backend into an executable fat JAR (`mvn clean package`). Ansible then automates the deployment of that compiled artifact onto target application servers.

---

### 24. How does Ansible integrate into a continuous CI/CD pipeline (e.g., Jenkins / GitHub Actions)?
**Answer:**  
In a full CI/CD pipeline:
1. Developer pushes code to GitHub.
2. CI server (Jenkins or GitHub Actions) compiles code and executes unit tests.
3. The CI runner executes `ansible-playbook -i inventory/inventory_aws_ec2.ini playbooks/site.yml`.
4. Ansible deploys the build artifact to EC2 staging/production and validates health before completing the pipeline run.

---

### 25. What are the key business and technical benefits of this automation?
**Answer:**  
- **Deployment Velocity:** Reduces provisioning and deployment time from ~60 minutes manually to <2 minutes.
- **Reliability:** 100% reproducible environments across dev, staging, and production.
- **Zero Human Error:** Eliminates misconfigurations, forgotten service restarts, and file permission errors.
- **Auditability:** Every infrastructure change is version-controlled, reviewed, and tracked in Git.
