# DEVOPS DEPLOYMENT & PIPELINE WORKFLOW
## ShalaConnect Continuous Configuration Pipeline (Spring Boot)
**Student:** Yash Janardan Sabale | **PRN:** 2310423T26-27 | **MIT Academy of Engineering, Pune**

---

### End-to-End Workflow Stages

The ShalaConnect automation workflow governs every change from local developer workstations to production environments.

```
+---------------------------------------------------------------------------------------+
|                       WORKFLOW STATE TRANSITION & GATE CHECKS                         |
+---------------------------------------------------------------------------------------+
|                                                                                       |
| [1. Plan] ------> [2. Code] ------> [3. Build] ------> [4. Test]                      |
| (Jira Backlog)    (Java 21/Git)     (Maven Package)    (JUnit 5 / Mockito)            |
|                                                              |                        |
|                                                              v (Gate: All Tests Pass) |
| [8. Monitor] <--- [7. Operate] <--- [6. Deploy] <----- [5. Release]                   |
| (/api/health)     (systemd/Nginx)   (Ansible Play)     (shalaconnect.jar)             |
|       |                                                                               |
|       +---------------------> [9. Feedback Loop] --------------------+                |
|                                                                      |                |
|                                                                      v                |
|                                                             (Sprint Planning)         |
+---------------------------------------------------------------------------------------+
```

---

### Stage-by-Stage Workflow Breakdown

#### Stage 1: Planning & Backlog Refinement
- Feature requirements, operational tickets, and security updates are prioritized.
- User stories and tasks are tracked in Jira with explicit acceptance criteria.

#### Stage 2: Code Authoring & Version Control
- Developers write Spring controllers, JPA repositories, and security configurations in Java 21.
- Code is pushed to GitHub with branch protection rules enforcing peer review.

#### Stage 3: Automated Build & Packaging
- GitHub webhook triggers Jenkins pipeline.
- Maven executes `mvn clean package` to compile source code and bundle dependencies into `shalaconnect-backend-1.0.0.jar`.

#### Stage 4: Automated Testing & Syntax Audit
- Automated JUnit unit tests and Mockito integration tests execute.
- Ansible syntax checking script (`validate_playbooks.py` and `ansible-playbook --syntax-check`) validates all playbooks, roles, and Jinja2 templates.

#### Stage 5: Release Tagging & Staging
- Successful builds receive an immutable semantic version tag (e.g., `v1.0.0`).
- Target environments (`staging`, `production`) are targeted within the Ansible inventory.

#### Stage 6: Ansible Deployment Orchestration
- Ansible Control Node executes `ansible-playbook playbooks/site.yml`.
- Playbook tasks run sequentially:
  - Updates system APT repository caches.
  - Installs OpenJDK 21, Maven, PostgreSQL client, and Nginx.
  - Creates dedicated `appuser` and `/opt/shalaconnect-app` directory.
  - Copies `shalaconnect-backend-1.0.0.jar` and renders `.env`.
  - Templates systemd unit file (`app.service.j2`) and restarts daemon.
  - Templates Nginx reverse proxy configuration (`nginx_site.conf.j2`) and validates syntax with `nginx -t`.

#### Stage 7: Operation & Runtime Daemonization
- Application process is actively supervised by `systemd`.
- In the event of an unhandled runtime exception, `systemd` automatically restarts the process after 5 seconds (`Restart=always`).
- System reboots trigger automated startup without manual intervention.

#### Stage 8: Automated Verification & Continuous Monitoring
- Ansible `uri` module polls `http://127.0.0.1:8080/api/health`.
- Validates HTTP 200 OK and confirms `"status": "UP"`.
- Continuous background probes stream uptime, memory, and CPU metrics to CloudWatch.

#### Stage 9: Feedback & Retrospective Loop
- Telemetry data, error logs (`journalctl -u shalaconnect`), and traffic metrics are reviewed.
- Anomalies automatically generate backlog tickets for iterative resolution in subsequent sprints.
