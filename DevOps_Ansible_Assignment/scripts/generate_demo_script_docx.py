import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCX_OUT = BASE_DIR / "DEMO_RECORDING_SCRIPT.docx"

doc = docx.Document()
for sec in doc.sections:
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.8)
    sec.right_margin = Inches(0.8)

PRIMARY = RGBColor(15, 23, 42)
SECONDARY = RGBColor(2, 132, 199)
ACCENT = RGBColor(13, 148, 136)

# Title
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("VIDEO DEMONSTRATION SCRIPT: WORD REPORT + GITHUB + LIVE AWS\n")
r.bold = True
r.font.size = Pt(14)
r.font.color.rgb = SECONDARY

r2 = p.add_run("DevOps IA Activity No. 1 – Case Study & Ansible Automation\n")
r2.bold = True
r2.font.size = Pt(12)
r2.font.color.rgb = PRIMARY

r3 = p.add_run("Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune\n")
r3.font.size = Pt(10)
r3.italic = True

def add_section(sec_num, title, timer, on_screen, speech):
    h = doc.add_heading(f"{sec_num}. {title} ({timer})", level=2)
    h.paragraph_format.space_before = Pt(10)
    
    p_screen = doc.add_paragraph()
    r_s = p_screen.add_run("🖥️ WHAT TO SHOW ON SCREEN: ")
    r_s.bold = True
    r_s.font.color.rgb = ACCENT
    p_screen.add_run(on_screen)
    
    p_speech = doc.add_paragraph()
    r_sp = p_speech.add_run("🗣️ SPOKEN SCRIPT (WORD-FOR-WORD):\n")
    r_sp.bold = True
    r_sp.font.color.rgb = SECONDARY
    r_sp_text = p_speech.add_run(speech)
    r_sp_text.italic = True
    r_sp_text.font.size = Pt(10.5)

add_section(
    "Section 1", "Title Page & Student Profile", "0:00 – 0:45",
    "Open Word Document Report (DevOps_IA1_CaseStudy_Report_Yash_Sabale.docx) on Page 1 showing student profile and title.",
    '''"Hello respected evaluator. My name is Yash Janardan Sabale, PRN 2310423T26-27, Third Year B.Tech Computer Engineering at MIT Academy of Engineering, Alandi, Pune.

Today, I am demonstrating my submission for Internal Assessment Activity No. 1: DevOps Case Study and Ansible Automation for Academic Year 2026–2027.

For this assignment, I have analyzed and implemented DevOps automation for ShalaConnect, a real-world educational governance platform for Cluster Resource Centre Heads. The backend is an enterprise service built on Java 21 LTS, Spring Boot 3.2.3, and PostgreSQL 15, deployed onto a multi-node AWS EC2 cloud architecture using Ansible."'''
)

add_section(
    "Section 2", "Rubric Compliance & DevOps Architecture Diagrams", "0:45 – 2:00",
    "Scroll to Rubric Table, then scroll to Figure 1 (Lifecycle), Figure 2 (Pipeline), and Figure 3 (Ansible Push Architecture).",
    '''"As outlined in our rubric compliance matrix, this project fulfills all 4 evaluation criteria: complete DevOps architecture, multi-tier Ansible inventory, modular Ansible roles, and verified live execution.

Here in Figure 1 is our end-to-end DevOps Lifecycle. We replaced the legacy manual deployment process with an automated 8-stage feedback loop: Plan, Code in Java 21, Build with Maven, Test with JUnit, Release to GitHub, Deploy agentlessly via Ansible, Operate under Linux systemd, and Monitor via /api/health telemetry.

Figure 2 illustrates our cloud delivery pipeline: code commits trigger automated build and packaging, after which Ansible orchestrates provisioning across AWS EC2.

Figure 3 details our Ansible Agentless Push Architecture. From our dedicated Control Node at Public IP 13.201.133.251, Ansible connects over OpenSSH port 22 to configure our Managed Application Node at Public IP 13.126.181.31, requiring zero agents on the target machine."'''
)

add_section(
    "Section 3", "Authentic Live Execution Evidence in Report", "2:00 – 3:30",
    "Scroll through Section 3 showing all 12 screenshots: AWS Console instances, SSH connection, inventory, ping, playbook recap, systemd, database tables, and curl.",
    '''"Now, let's review the 12 authentic execution screenshots captured during our live cloud deployment:

• Evidence 1 & 2 show the AWS Management Console launching our dedicated Control Node with instance ID i-06ec3b172d5dd0868 and Public IP 13.201.133.251.
• Evidence 3 & 4 show the target APP instance running in Mumbai with Public IP 13.126.181.31.
• Evidence 5 & 6 show SSH access from our Windows terminal into the Control Node using shalaconnect-key.pem, syncing the repo, and verifying inventory_aws_ec2.ini.
• Evidence 7 demonstrates the Ansible Ad-Hoc Ping. Running ansible all -m ping confirms successful agentless communication with ok: [ec2-app-server].
• Evidence 8 & 9 capture our master playbook execution. Notice our initialization banner displaying my name: Yash Janardan Sabale (PRN: 2310423T26-27). The final PLAY RECAP confirms 37 tasks OK and zero failures (failed=0).
• Evidence 10 verifies the remote systemd daemon: shalaconnect.service is active and running with Tomcat on port 8080.
• Evidence 11 verifies PostgreSQL 15, listing all 14 JPA domain tables generated in our school_management database.
• Evidence 12 shows our live curl probe to http://13.126.181.31/api/health, returning HTTP 200 OK and status UP via Nginx reverse proxy."'''
)

add_section(
    "Section 4", "Codebase Walkthrough on GitHub", "3:30 – 5:00",
    "Switch to GitHub browser tab (YashSabale01/ShalaConnect). Open ansible.cfg, inventory_aws_ec2.ini, playbooks/site.yml, and roles/springboot_app/tasks/.",
    '''"Now let's examine the version-controlled codebase hosted on my GitHub repository under DevOps_Ansible_Assignment.

First, in ansible.cfg, we define global orchestration parameters: remote_user = ec2-user, privilege escalation with become = True and become_method = sudo, and optimized SSH multiplexing.

In inventory_aws_ec2.ini, we define our managed target ec2-app-server at 13.126.181.31, configure SSH keys, and group webservers and app servers along with centralized port variables.

Here is our master orchestration entry point, site.yml. It targets hosts: all, gathers system facts, verifies the OS family, and invokes our enterprise role.

Our role is structured into modular task files following industry best practices:
• In setup_environment.yml, we install OpenJDK 21 Corretto, Maven, Nginx, and PostgreSQL 15, initialize the database, configure trust authentication, and create a restricted system user appuser.
• In deploy_code.yml, we create /opt/shalaconnect-app, deploy our executable JAR, and render production properties from Jinja2 templates.
• In configure_service.yml, we template our systemd unit file with automatic 5-second restart policies and process sandboxing.
• In configure_nginx.yml, we deploy an Nginx reverse proxy configuration forwarding external Port 80 traffic to internal Port 8080.
• In verify_health.yml, we automated post-deployment smoke testing using the URI module to poll the /api/health endpoint."'''
)

add_section(
    "Section 5", "Live Browser Telemetry & Conclusion", "5:00 – 5:30",
    "Switch to live browser tab (http://13.126.181.31/api/health) and hit Refresh.",
    '''"Finally, here is the live, public verification on our running AWS EC2 instance at http://13.126.181.31/api/health.

As you can see on screen, the Nginx reverse proxy forwards to Spring Boot, which queries our PostgreSQL database and returns HTTP 200 OK with JSON payload: {"status": "UP", "service": "ShalaConnect API", "timestamp": "..."}.

In conclusion, this project successfully automated the entire infrastructure and deployment lifecycle of ShalaConnect. Deployment duration was cut from 45 minutes to under two minutes, configuration drift was eliminated, and security was hardened.

All report documents, diagrams, playbooks, and evidence have been compiled and submitted.

Thank you very much!"'''
)

# Viva Q&A
doc.add_page_break()
doc.add_heading("Top 5 Viva Voce Questions & High-Scoring Answers", level=1)
vivas = [
    ("1. Why is Ansible called agentless?", "Unlike Puppet or Chef, target managed nodes do not need any agent software installed. Ansible executes over standard OpenSSH (Port 22) and standard Python."),
    ("2. What is Idempotency in Ansible?", "An operation can be executed multiple times without changing the final state beyond the initial application. If a package is already installed, Ansible reports ok instead of changed."),
    ("3. Why did you separate Control Node and Managed Node on AWS?", "To reflect enterprise DevOps topology: the Control Node houses the automation engine, playbooks, and secrets, pushing changes remotely to target nodes without exposing automation tools to public traffic."),
    ("4. Why use an Ansible Role instead of a single playbook?", "Roles enforce separation of concerns (tasks, templates, handlers, vars, defaults), making playbooks modular, reusable, testable, and easier to maintain."),
    ("5. Why put Nginx in front of Spring Boot?", "Nginx serves as a reverse proxy listening on standard HTTP Port 80, buffering slow clients, handling static assets, and forwarding API requests to internal port 8080 without exposing Java directly to the internet.")
]
for q, a in vivas:
    p_q = doc.add_paragraph()
    r_q = p_q.add_run(q)
    r_q.bold = True
    r_q.font.color.rgb = SECONDARY
    doc.add_paragraph(a)

doc.save(str(DOCX_OUT))
print(f"Successfully generated: {DOCX_OUT.name}")
