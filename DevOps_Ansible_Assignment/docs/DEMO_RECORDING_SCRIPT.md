# VIDEO DEMONSTRATION SCRIPT: WORD REPORT + GITHUB + LIVE AWS
## IA Activity No. 1 – DevOps Case Study & Ansible Automation Assignment
**Student:** Yash Janardan Sabale | **PRN:** 2310423T26-27  
**Branch:** Computer Engineering | **College:** MIT Academy of Engineering, Alandi, Pune  
**Target Architecture:** Multi-Node AWS EC2 (Control Node: `13.201.133.251` | App Server: `13.126.181.31`)

---

## 📋 PRE-RECORDING CHECKLIST
Before clicking **Record Screen**, make sure you have these 3 tabs open:
- [x] **Tab 1:** Microsoft Word with `DevOps_IA1_CaseStudy_Report_Yash_Sabale.docx` (Set zoom to 125%)
- [x] **Tab 2:** Web Browser open to your GitHub Repo: `https://github.com/YashSabale01/ShalaConnect/tree/main/DevOps_Ansible_Assignment`
- [x] **Tab 3:** Web Browser open to the live AWS endpoint: `http://13.126.181.31/api/health`

---

## 🎬 WORD-FOR-WORD SPOKEN SCRIPT (TIMED: 5 TO 6 MINUTES)

### 🕒 Section 1: Title Page & Student Profile (0:00 – 0:45)
**🖥️ ON SCREEN:** Show Page 1 of your Word Report (`DevOps_IA1_CaseStudy_Report_Yash_Sabale.docx`).

**🗣️ SPEAK THIS:**
> "Hello respected evaluator. My name is **Yash Janardan Sabale**, PRN **2310423T26-27**, Third Year B.Tech Computer Engineering at MIT Academy of Engineering, Alandi, Pune.
> 
> Today, I am demonstrating my submission for **Internal Assessment Activity No. 1: DevOps Case Study and Ansible Automation** for Academic Year 2026–2027.
> 
> For this assignment, I have analyzed and implemented DevOps automation for **ShalaConnect**, a real-world educational governance platform for Cluster Resource Centre Heads. The backend is an enterprise service built on **Java 21 LTS**, **Spring Boot 3.2.3**, and **PostgreSQL 15**, deployed onto a multi-node **AWS EC2** cloud architecture using **Ansible**."

---

### 🕒 Section 2: Rubric Compliance & DevOps Architecture Diagrams (0:45 – 2:00)
**🖥️ ON SCREEN:** Scroll down to the Rubric Table (Section 1), then to the 3 Architecture Diagrams (Section 2).

**🗣️ SPEAK THIS:**
> *(Pointing at Rubric Table)*  
> "As outlined in our rubric compliance matrix, this project fulfills all 4 evaluation criteria: complete DevOps architecture, multi-tier Ansible inventory, modular Ansible roles, and verified live execution.
> 
> *(Scroll to Figure 1 – Lifecycle Diagram)*  
> Here in Figure 1 is our end-to-end **DevOps Lifecycle**. We replaced the legacy manual deployment process with an automated 8-stage feedback loop: **Plan**, **Code** in Java 21, **Build** with Maven, **Test** with JUnit, **Release** to GitHub, **Deploy** agentlessly via Ansible, **Operate** under Linux systemd, and **Monitor** via `/api/health` telemetry.
> 
> *(Scroll to Figure 2 – DevOps Cloud Architecture)*  
> Figure 2 illustrates our cloud delivery pipeline. A code commit triggers automated build and packaging, after which Ansible orchestrates provisioning across AWS EC2.
> 
> *(Scroll to Figure 3 – Ansible Workflow)*  
> Figure 3 details our **Ansible Agentless Push Architecture**. From our dedicated **Control Node at Public IP `13.201.133.251`**, Ansible connects over OpenSSH port 22 to configure our **Managed Application Node at Public IP `13.126.181.31`**, requiring zero agents on the target machine."

---

### 🕒 Section 3: Authentic Execution Evidence in Word Report (2:00 – 3:30)
**🖥️ ON SCREEN:** Scroll to Section 3: "Authentic Live AWS EC2 & Ansible Execution Evidence". Scroll through the 12 screenshots.

**🗣️ SPEAK THIS:**
> "Now, let's review the 12 authentic execution screenshots captured during our live cloud deployment:
> 
> *(Show Evidence 1 & 2)*  
> • **Evidence 1 & 2** show the AWS Management Console launching our dedicated **Control Node** with instance ID `i-06ec3b172d5dd0868` and Public IP `13.201.133.251`.
> 
> *(Show Evidence 3 & 4)*  
> • **Evidence 3 & 4** show the target **APP instance** running in the Mumbai region with Public IP `13.126.181.31`.
> 
> *(Show Evidence 5 & 6)*  
> • **Evidence 5 & 6** show SSH access from our Windows terminal into the Control Node using `shalaconnect-key.pem`, syncing the repo, and verifying `inventory_aws_ec2.ini`.
> 
> *(Show Evidence 7)*  
> • **Evidence 7** demonstrates the **Ansible Ad-Hoc Ping**. Running `ansible all -m ping` confirms successful agentless communication with `ok: [ec2-app-server]`.
> 
> *(Show Evidence 8 & 9)*  
> • **Evidence 8 & 9** capture our master playbook execution. Notice our initialization banner displaying my name: **Yash Janardan Sabale (PRN: 2310423T26-27)**. The final PLAY RECAP confirms **37 tasks OK and zero failures (`failed=0`)**.
> 
> *(Show Evidence 10 & 11)*  
> • **Evidence 10** verifies the remote systemd daemon: `shalaconnect.service` is **active (running)** with Tomcat on port 8080.  
> • **Evidence 11** verifies PostgreSQL 15, listing all 14 JPA domain tables generated in our `school_management` database.
> 
> *(Show Evidence 12)*  
> • **Evidence 12** shows our live curl probe to `http://13.126.181.31/api/health`, returning **HTTP 200 OK** and status UP via Nginx reverse proxy."

---

### 🕒 Section 4: Codebase Walkthrough on GitHub (3:30 – 5:00)
**🖥️ ON SCREEN:** Switch tabs to GitHub: `https://github.com/YashSabale01/ShalaConnect/tree/main/DevOps_Ansible_Assignment`

**🗣️ SPEAK THIS:**
> "Now let's examine the version-controlled codebase hosted on my GitHub repository under `DevOps_Ansible_Assignment`.
> 
> *(Click open `ansible.cfg`)*  
> First, in **`ansible.cfg`**, we define global orchestration parameters. We configure `remote_user = ec2-user`, enable privilege escalation with `become = True` and `become_method = sudo`, and optimize SSH performance using ControlMaster multiplexing.
> 
> *(Go back and click open `inventory/inventory_aws_ec2.ini`)*  
> In our inventory file, we define our managed target `ec2-app-server` at `13.126.181.31`, specify the private SSH key path, and establish logical groups for webservers and app servers along with centralized variables for port 8080 and port 80.
> 
> *(Go back and click open `playbooks/site.yml`)*  
> Here is our master orchestration entry point, **`site.yml`**. It targets `hosts: all`, gathers system facts, verifies the operating system family, and invokes our enterprise role.
> 
> *(Navigate to `roles/springboot_app/tasks/`)*  
> Our role is structured into modular task files following industry best practices:  
> • In **`setup_environment.yml`**, we use the DNF module to install OpenJDK 21 Corretto, Maven, Nginx, and PostgreSQL 15. We also automate `postgresql-setup --initdb`, configure `pg_hba.conf` trust authentication, create the database, and create a restricted system user `appuser`.  
> • In **`deploy_code.yml`**, we create `/opt/shalaconnect-app`, deploy our executable JAR, and render production properties from Jinja2 templates.  
> • In **`configure_service.yml`**, we template our `shalaconnect.service` systemd unit file with automatic 5-second restart policies and process sandboxing.  
> • In **`configure_nginx.yml`**, we deploy an Nginx reverse proxy configuration forwarding external Port 80 traffic to internal Spring Boot Port 8080.  
> • In **`verify_health.yml`**, we automated post-deployment smoke testing using the URI module to poll the `/api/health` endpoint."

---

### 🕒 Section 5: Live Browser Telemetry & Conclusion (5:00 – 5:30)
**🖥️ ON SCREEN:** Switch to the live browser tab: `http://13.126.181.31/api/health` and hit Refresh.

**🗣️ SPEAK THIS:**
> *(Refresh browser tab)*  
> "Finally, here is the live, public verification on our running AWS EC2 instance at **`http://13.126.181.31/api/health`**.
> 
> As you can see on screen, the Nginx reverse proxy forwards to Spring Boot, which queries our PostgreSQL database and returns **HTTP 200 OK** with JSON payload:  
> `{"status": "UP", "service": "ShalaConnect API", "timestamp": "..."}`.
> 
> In conclusion, this project successfully automated the entire infrastructure and deployment lifecycle of ShalaConnect. Deployment duration was cut from 45 minutes to under two minutes, configuration drift was eliminated, and security was hardened.
> 
> All report documents, diagrams, playbooks, and evidence have been compiled and submitted.
> 
> Thank you very much!"

---

## 🎯 TOP 5 VIVA VOCE QUESTIONS & QUICK ANSWERS

1. **Q: Why is Ansible called agentless?**  
   *A:* Unlike Puppet or Chef, target managed nodes do not need any agent software installed. Ansible executes over standard OpenSSH (Port 22) and standard Python.

2. **Q: What is Idempotency in Ansible?**  
   *A:* An operation can be executed multiple times without changing the final state beyond the initial application. If a package is already installed, Ansible reports `ok` instead of `changed`.

3. **Q: Why did you separate Control Node and Managed Node on AWS?**  
   *A:* To reflect enterprise DevOps topology: the Control Node houses the automation engine, playbooks, and secrets, pushing changes remotely to target nodes without exposing automation tools to public traffic.

4. **Q: Why use an Ansible Role instead of a single playbook?**  
   *A:* Roles enforce separation of concerns (`tasks`, `templates`, `handlers`, `vars`, `defaults`), making playbooks modular, reusable, testable, and easier to maintain.

5. **Q: Why put Nginx in front of Spring Boot?**  
   *A:* Nginx serves as a reverse proxy listening on standard HTTP Port 80, buffering slow clients, handling static assets, and forwarding API requests to internal port 8080 without exposing Java directly to the internet.
