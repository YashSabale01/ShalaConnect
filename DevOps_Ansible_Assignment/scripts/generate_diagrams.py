#!/usr/bin/env python3
"""
High-Resolution Professional DevOps Architecture & Lifecycle Diagram Generator
Target: ShalaConnect Java 21 / Spring Boot 3.2.3 Backend Platform
Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune
Outputs 300 DPI Publication-Grade PNG Diagrams:
 1. diagrams/devops_lifecycle.png
 2. diagrams/devops_architecture.png
 3. diagrams/ansible_workflow.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = BASE_DIR / "diagrams"
DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

FONT_FAMILY = "sans-serif"
BG_COLOR = "#0f172a"
CARD_BG = "#1e293b"
TEXT_COLOR = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#38bdf8"
ACCENT_GREEN = "#10b981"
ACCENT_PURPLE = "#a855f7"
ACCENT_ORANGE = "#f97316"
ACCENT_CYAN = "#06b6d4"
BORDER_COLOR = "#334155"

def draw_rounded_card(ax, x, y, width, height, title, subtitle="", items=None, header_color="#38bdf8", fill_color="#1e293b", edge_color="#334155", title_color="#ffffff"):
    rect = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor=fill_color, edgecolor=edge_color,
        linewidth=1.8, zorder=2
    )
    ax.add_patch(rect)
    
    stripe = patches.FancyBboxPatch(
        (x, y + height - 0.12), width, 0.12,
        boxstyle="round,pad=0.01,rounding_size=0.05",
        facecolor=header_color, edgecolor="none", zorder=3
    )
    ax.add_patch(stripe)

    ax.text(x + width / 2, y + height - 0.28, title,
            ha="center", va="center", color=title_color,
            fontsize=11.5, fontweight="bold", family=FONT_FAMILY, zorder=4)

    cur_y = y + height - 0.46
    if subtitle:
        ax.text(x + width / 2, cur_y, subtitle,
                ha="center", va="center", color=TEXT_MUTED,
                fontsize=9.0, fontstyle="italic", family=FONT_FAMILY, zorder=4)
        cur_y -= 0.25

    if items:
        for item in items:
            ax.text(x + 0.15, cur_y, f"• {item}",
                    ha="left", va="center", color="#cbd5e1",
                    fontsize=8.5, family=FONT_FAMILY, zorder=4)
            cur_y -= 0.22

def draw_arrow(ax, start, end, label="", color="#38bdf8", lw=2.0, rad=0.0, label_offset=(0, 0.15)):
    conn_style = f"arc3,rad={rad}" if rad != 0.0 else "arc3"
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops=dict(
            arrowstyle="->,head_width=0.45,head_length=0.7",
            color=color, lw=lw,
            connectionstyle=conn_style
        ),
        zorder=5
    )
    if label:
        mid_x = (start[0] + end[0]) / 2 + label_offset[0]
        mid_y = (start[1] + end[1]) / 2 + label_offset[1]
        bbox_props = dict(boxstyle="round,pad=0.2", fc="#090d16", ec=color, lw=1.0, alpha=0.95)
        ax.text(mid_x, mid_y, label, ha="center", va="center",
                color=TEXT_COLOR, fontsize=8.2, fontweight="bold",
                bbox=bbox_props, zorder=6)

# ==============================================================================
# DIAGRAM 1: DEVOPS LIFECYCLE (JAVA SPRING BOOT)
# ==============================================================================
def generate_diagram_1():
    print("[DIAGRAM 1] Generating DevOps Lifecycle (Java Spring Boot)...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(8.0, 8.4, "SHALACONNECT SPRING BOOT CONTINUOUS DEVOPS LIFECYCLE",
            ha="center", va="center", color="#ffffff", fontsize=18, fontweight="bold")
    ax.text(8.0, 7.95, "Plan → Code (Java 21) → Build (Maven) → Test (JUnit) → Release → Deploy (Ansible) → Operate (systemd) → Monitor (/api/health)",
            ha="center", va="center", color=ACCENT_BLUE, fontsize=10.5)

    stages = [
        {"title": "1. PLAN", "sub": "Agile Sprints", "items": ["Jira / Linear", "School User Stories", "Sprint Milestones"], "col": "#0284c7"},
        {"title": "2. CODE", "sub": "Java 21 / Spring Boot", "items": ["Spring Web / JPA", "Git & GitHub", "Branch Protection"], "col": "#06b6d4"},
        {"title": "3. BUILD", "sub": "Maven Build Engine", "items": ["mvn clean package", "Spring Boot Fat JAR", "Artifact Staging"], "col": "#10b981"},
        {"title": "4. TEST", "sub": "Automated Quality", "items": ["JUnit 5 & Mockito", "Security Spring Test", "Syntax Validation"], "col": "#84cc16"},
        {"title": "5. RELEASE", "sub": "Semantic Tagging", "items": ["shalaconnect-backend.jar", "v1.0.0 Release Tag", "Ansible Inventory"], "col": "#eab308"},
        {"title": "6. DEPLOY", "sub": "Ansible Automation", "items": ["roles/springboot_app", "OpenJDK 21 Setup", "app.service.j2 Systemd"], "col": "#f97316"},
        {"title": "7. OPERATE", "sub": "Process Supervision", "items": ["systemctl active", "Nginx Proxy :80->:8080", "JVM Memory Limits"], "col": "#ec4899"},
        {"title": "8. MONITOR", "sub": "Telemetry Probes", "items": ["GET /api/health", "HikariCP & JVM Heap", "Uptime & CloudWatch"], "col": "#a855f7"},
    ]

    card_w = 3.2
    card_h = 1.9

    top_y = 5.2
    xs_top = [0.8, 4.6, 8.4, 12.2]
    for i in range(4):
        s = stages[i]
        draw_rounded_card(ax, xs_top[i], top_y, card_w, card_h, s["title"], s["sub"], s["items"], header_color=s["col"])

    draw_arrow(ax, (xs_top[0] + card_w, top_y + card_h / 2), (xs_top[1], top_y + card_h / 2), label="Commit", color=ACCENT_BLUE)
    draw_arrow(ax, (xs_top[1] + card_w, top_y + card_h / 2), (xs_top[2], top_y + card_h / 2), label="Maven Trigger", color=ACCENT_CYAN)
    draw_arrow(ax, (xs_top[2] + card_w, top_y + card_h / 2), (xs_top[3], top_y + card_h / 2), label="JUnit Verify", color=ACCENT_GREEN)

    draw_arrow(ax, (xs_top[3] + card_w / 2, top_y), (xs_top[3] + card_w / 2, 4.1), label="Build Passed", color="#84cc16")

    bot_y = 2.2
    xs_bot = [12.2, 8.4, 4.6, 0.8]
    for i in range(4):
        s = stages[4 + i]
        draw_rounded_card(ax, xs_bot[i], bot_y, card_w, card_h, s["title"], s["sub"], s["items"], header_color=s["col"])

    draw_arrow(ax, (xs_bot[0], bot_y + card_h / 2), (xs_bot[1] + card_w, bot_y + card_h / 2), label="Ansible Run", color="#f97316")
    draw_arrow(ax, (xs_bot[1], bot_y + card_h / 2), (xs_bot[2] + card_w, bot_y + card_h / 2), label="systemd start", color="#ec4899")
    draw_arrow(ax, (xs_bot[2], bot_y + card_h / 2), (xs_bot[3] + card_w, bot_y + card_h / 2), label="Probe /api/health", color="#a855f7")

    feedback_box = patches.FancyBboxPatch(
        (4.5, 0.4), 7.0, 1.2,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor="#182234", edgecolor="#38bdf8", linewidth=1.5, zorder=2
    )
    ax.add_patch(feedback_box)
    ax.text(8.0, 1.2, "9. CONTINUOUS FEEDBACK & OBSERVABILITY LOOP", ha="center", va="center", color=ACCENT_BLUE, fontsize=11, fontweight="bold")
    ax.text(8.0, 0.75, "Spring Boot Actuator Telemetry & Error Logs fed directly back into Agile Sprint Backlog", ha="center", va="center", color="#cbd5e1", fontsize=8.5)

    draw_arrow(ax, (xs_bot[3] + card_w / 2, bot_y), (4.5, 1.0), label="Log Analysis", color="#a855f7", rad=0.2)
    draw_arrow(ax, (11.5, 1.0), (xs_top[0] + card_w / 2, top_y), label="Sprint Backlog Loop", color=ACCENT_BLUE, rad=0.25)

    ax.text(8.0, 0.15, "Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MIT Academy of Engineering, Pune",
            ha="center", va="center", color=TEXT_MUTED, fontsize=8.5)

    plt.tight_layout()
    output_path = DIAGRAMS_DIR / "devops_lifecycle.png"
    plt.savefig(output_path, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"  [SAVED] {output_path.name}")

# ==============================================================================
# DIAGRAM 2: DEVOPS ARCHITECTURE (JAVA SPRING BOOT)
# ==============================================================================
def generate_diagram_2():
    print("[DIAGRAM 2] Generating DevOps Architecture (Java Spring Boot)...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(8.0, 8.4, "SHALACONNECT SPRING BOOT SYSTEM & INFRASTRUCTURE ARCHITECTURE",
            ha="center", va="center", color="#ffffff", fontsize=17, fontweight="bold")
    ax.text(8.0, 7.95, "Developer → GitHub SCM → Jenkins CI (Maven) → Ansible Control Node → Target AWS EC2 (Java 21 / Nginx)",
            ha="center", va="center", color=ACCENT_CYAN, fontsize=10.5)

    card_w = 3.1
    card_h = 2.4
    y_flow = 4.8

    draw_rounded_card(ax, 0.6, y_flow, card_w, card_h, "1. Developer", "Workstation",
                      ["IntelliJ / VS Code", "Feature Branches", "mvn test pre-check", "git push origin main"],
                      header_color="#38bdf8")

    draw_rounded_card(ax, 4.4, y_flow, card_w, card_h, "2. GitHub SCM", "Central Repository",
                      ["backend/pom.xml & src/", "Pull Request Validation", "Webhook Dispatch", "Semantic Release Tags"],
                      header_color="#6366f1")

    draw_rounded_card(ax, 8.2, y_flow, card_w, card_h, "3. Jenkins CI/CD", "Maven Build Master",
                      ["mvn clean package", "JUnit 5 Test Pass", "Produces backend.jar", "Ansible Plugin Trigger"],
                      header_color="#10b981")

    draw_rounded_card(ax, 12.0, y_flow, card_w, card_h, "4. Ansible Control Node", "Orchestration Engine",
                      ["ansible.cfg defaults", "inventory/inventory.ini", "roles/springboot_app", "SSH Agent & Vault"],
                      header_color="#f97316")

    draw_arrow(ax, (3.7, y_flow + card_h / 2), (4.4, y_flow + card_h / 2), label="git push", color="#38bdf8")
    draw_arrow(ax, (7.5, y_flow + card_h / 2), (8.2, y_flow + card_h / 2), label="Webhook", color="#6366f1")
    draw_arrow(ax, (11.3, y_flow + card_h / 2), (12.0, y_flow + card_h / 2), label="Deploy Artifact", color="#10b981")

    draw_arrow(ax, (13.55, y_flow), (13.55, 3.8), label="SSH (Port 22)\nAgentless Push", color="#f97316", label_offset=(0.85, 0))

    server_box = patches.FancyBboxPatch(
        (3.0, 1.1), 12.2, 2.5,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor="#131d2e", edgecolor="#38bdf8", linewidth=2.0, zorder=2
    )
    ax.add_patch(server_box)
    ax.text(3.3, 3.35, "TARGET MANAGED NODE: AWS EC2 Ubuntu 22.04 LTS (54.210.120.45)",
            ha="left", va="center", color="#38bdf8", fontsize=11, fontweight="bold")

    draw_rounded_card(ax, 3.5, 1.35, 3.4, 1.8, "Nginx Reverse Proxy", "Port 80 (Public)",
                      ["SSL / HTTP Termination", "proxy_pass :8080", "Gzip & Static Buffers", "Access / Error Logging"],
                      header_color="#06b6d4")

    draw_rounded_card(ax, 7.5, 1.35, 3.5, 1.8, "Spring Boot Backend", "Port 8080 (Internal)",
                      ["systemd service daemon", "java -jar backend.jar", "HikariCP & PostgreSQL", "appuser unprivileged"],
                      header_color="#10b981")

    draw_rounded_card(ax, 11.5, 1.35, 3.3, 1.8, "Health & Telemetry", "Endpoint: /api/health",
                      ["HTTP 200 Telemetry", "JVM Memory & Heap stats", "PostgreSQL Pool status", "Verified via Ansible uri"],
                      header_color="#a855f7")

    draw_arrow(ax, (6.9, 2.25), (7.5, 2.25), label="proxy_pass", color="#06b6d4")
    draw_arrow(ax, (11.0, 2.25), (11.5, 2.25), label="Health Poll", color="#10b981")

    draw_rounded_card(ax, 0.6, 1.1, 2.0, 2.5, "Monitoring", "CloudWatch",
                      ["Prometheus", "Health Alerts", "Slack / Email", "Feedback Loop"],
                      header_color="#a855f7")
    draw_arrow(ax, (3.0, 1.8), (2.6, 1.8), label="Telemetry", color="#a855f7")
    draw_arrow(ax, (1.6, 3.6), (1.6, y_flow), label="Feedback", color="#a855f7")

    ax.text(8.0, 0.45, "DevOps IA Activity No. 1 | Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune",
            ha="center", va="center", color=TEXT_MUTED, fontsize=8.5)

    plt.tight_layout()
    output_path = DIAGRAMS_DIR / "devops_architecture.png"
    plt.savefig(output_path, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"  [SAVED] {output_path.name}")

# ==============================================================================
# DIAGRAM 3: ANSIBLE WORKFLOW & ARCHITECTURE (SPRING BOOT)
# ==============================================================================
def generate_diagram_3():
    print("[DIAGRAM 3] Generating Ansible Workflow & Architecture (Spring Boot)...")
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(8.0, 8.4, "ANSIBLE CONFIGURATION MANAGEMENT FOR SPRING BOOT BACKEND",
            ha="center", va="center", color="#ffffff", fontsize=17, fontweight="bold")
    ax.text(8.0, 7.95, "Ansible Control Node Components Transporting Over SSH to Configure OpenJDK 21, Spring Boot Daemon & Nginx",
            ha="center", va="center", color=ACCENT_ORANGE, fontsize=10.5)

    control_box = patches.FancyBboxPatch(
        (0.6, 1.2), 6.8, 6.2,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor="#141e30", edgecolor=ACCENT_ORANGE, linewidth=2.0, zorder=2
    )
    ax.add_patch(control_box)
    ax.text(4.0, 7.05, "ANSIBLE CONTROL NODE (Linux / WSL2)", ha="center", va="center",
            color=ACCENT_ORANGE, fontsize=12, fontweight="bold")

    draw_rounded_card(ax, 0.9, 4.8, 2.9, 1.9, "ansible.cfg", "Global Config",
                      ["inventory path", "become = sudo", "host_key_checking=F", "SSH ControlMaster"],
                      header_color="#f97316")

    draw_rounded_card(ax, 4.2, 4.8, 2.9, 1.9, "inventory.ini", "Host Catalog",
                      ["[webservers] groups", "[app_servers] tier", "ansible_host IP", "ansible_ssh_key"],
                      header_color="#eab308")

    draw_rounded_card(ax, 0.9, 1.6, 2.9, 2.8, "Playbooks & Roles", "Orchestration Code",
                      ["playbooks/site.yml", "roles/springboot_app/", "  ├── tasks/*.yml", "  ├── handlers/main.yml", "  ├── templates/*.j2", "  └── defaults/main.yml"],
                      header_color="#10b981")

    draw_rounded_card(ax, 4.2, 1.6, 2.9, 2.8, "Ansible Core Modules", "Execution Engine",
                      ["ansible.builtin.apt", "ansible.builtin.file", "ansible.builtin.copy", "ansible.builtin.template", "ansible.builtin.systemd", "ansible.builtin.uri"],
                      header_color="#38bdf8")

    target_box = patches.FancyBboxPatch(
        (10.2, 1.2), 5.2, 6.2,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor="#111c2e", edgecolor=ACCENT_GREEN, linewidth=2.0, zorder=2
    )
    ax.add_patch(target_box)
    ax.text(12.8, 7.05, "MANAGED TARGET NODES (Agentless)", ha="center", va="center",
            color=ACCENT_GREEN, fontsize=12, fontweight="bold")

    draw_rounded_card(ax, 10.5, 5.0, 4.6, 1.7, "OS & Java 21 Tier", "Dependencies Configured",
                      ["APT Cache Updated & Repos configured", "OpenJDK 21 JDK / JRE installed", "Nginx & PostgreSQL client installed"],
                      header_color="#06b6d4")

    draw_rounded_card(ax, 10.5, 3.1, 4.6, 1.7, "Application & Artifact Tier", "Directories & Deployments",
                      ["appuser & appgroup created", "/opt/shalaconnect-app populated", "shalaconnect-backend-1.0.0.jar deployed"],
                      header_color="#10b981")

    draw_rounded_card(ax, 10.5, 1.4, 4.6, 1.5, "Service & Reverse Proxy Tier", "Runtime State",
                      ["systemd service enabled & active", "Nginx reverse proxy routing port 80 -> 8080", "Health verified (/api/health HTTP 200 UP)"],
                      header_color="#a855f7")

    ssh_bus = patches.FancyBboxPatch(
        (7.6, 3.5), 2.4, 1.8,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor="#090d16", edgecolor=ACCENT_CYAN, linewidth=1.5, zorder=3
    )
    ax.add_patch(ssh_bus)
    ax.text(8.8, 4.9, "SSH TRANSPORT", ha="center", va="center", color=ACCENT_CYAN, fontsize=9.5, fontweight="bold")
    ax.text(8.8, 4.4, "OpenSSH (Port 22)", ha="center", va="center", color="#cbd5e1", fontsize=8.0)
    ax.text(8.8, 4.0, "Key-Based Auth (.pem)", ha="center", va="center", color="#cbd5e1", fontsize=8.0)
    ax.text(8.8, 3.65, "Zero Agents Required", ha="center", va="center", color="#34d399", fontsize=8.0, fontweight="bold")

    draw_arrow(ax, (7.1, 4.4), (7.6, 4.4), color=ACCENT_ORANGE, lw=2.5)
    draw_arrow(ax, (10.0, 4.4), (10.5, 4.4), color=ACCENT_GREEN, lw=2.5)

    ax.text(8.0, 0.45, "Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MIT Academy of Engineering, Pune",
            ha="center", va="center", color=TEXT_MUTED, fontsize=8.5)

    plt.tight_layout()
    output_path = DIAGRAMS_DIR / "ansible_workflow.png"
    plt.savefig(output_path, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"  [SAVED] {output_path.name}")

def main():
    print("=" * 70)
    print(" GENERATING HIGH-RESOLUTION 300 DPI SPRING BOOT ARCHITECTURE DIAGRAMS")
    print(" Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune")
    print("=" * 70)
    
    generate_diagram_1()
    generate_diagram_2()
    generate_diagram_3()
    
    print("=" * 70)
    print(" [SUCCESS] ALL 3 HIGH-RESOLUTION DIAGRAMS GENERATED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
