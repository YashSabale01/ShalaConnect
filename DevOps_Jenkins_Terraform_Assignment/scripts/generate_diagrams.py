#!/usr/bin/env python3
"""
Publication-Grade Architecture Diagram Generator for IA Activity 3
Jenkins CI/CD Pipeline & Terraform Infrastructure as Code
Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune
Application: ShalaConnect (Java 21 / Spring Boot 3.2 Cloud-Native Architecture)
Outputs 300 DPI High-Resolution Visual Architecture Diagrams:
 1. diagrams/jenkins_cicd_pipeline_architecture.png
 2. diagrams/terraform_aws_infrastructure_topology.png
 3. diagrams/jenkins_terraform_integration_flow.png
 4. diagrams/gitops_deployment_lifecycle.png
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
ACCENT_AMBER = "#f59e0b"
ACCENT_ROSE = "#f43f5e"
BORDER_COLOR = "#334155"

def draw_card(ax, x, y, width, height, title, subtitle="", items=None,
              header_color="#38bdf8", fill_color="#1e293b", edge_color="#334155", title_color="#ffffff"):
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
            fontsize=10.5, fontweight="bold", family=FONT_FAMILY, zorder=4)

    cur_y = y + height - 0.48
    if subtitle:
        ax.text(x + width / 2, cur_y, subtitle,
                ha="center", va="center", color=TEXT_MUTED,
                fontsize=8.0, family=FONT_FAMILY, zorder=4)
        cur_y -= 0.25

    if items:
        for item in items:
            ax.text(x + 0.15, cur_y, f"• {item}",
                    ha="left", va="center", color=TEXT_COLOR,
                    fontsize=8.0, family=FONT_FAMILY, zorder=4)
            cur_y -= 0.24

def draw_arrow(ax, x1, y1, x2, y2, color="#38bdf8", label="", width=2.0, curved=False):
    style = "Simple,tail_width=0.8,head_width=5,head_length=6"
    kw = dict(arrowstyle=style, color=color, lw=width, zorder=5)
    if curved:
        patch = patches.FancyArrowPatch((x1, y1), (x2, y2), connectionstyle="arc3,rad=-0.2", **kw)
    else:
        patch = patches.FancyArrowPatch((x1, y1), (x2, y2), **kw)
    ax.add_patch(patch)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 + 0.14
        ax.text(mx, my, label, ha="center", va="center", color=color,
                fontsize=8.0, fontweight="bold", family=FONT_FAMILY, zorder=6,
                bbox=dict(boxstyle="round,pad=0.15", facecolor=BG_COLOR, edgecolor="none"))

# ==============================================================================
# DIAGRAM 1: JENKINS MULTI-STAGE CI/CD PIPELINE ARCHITECTURE
# ==============================================================================
def generate_jenkins_cicd_pipeline_architecture():
    fig, ax = plt.subplots(figsize=(19, 10), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(-0.5, 18.5)
    ax.set_ylim(-0.5, 10.0)
    ax.axis("off")

    # Header
    ax.text(9.0, 9.4, "SHALACONNECT ENTERPRISE JENKINS CI/CD PIPELINE ARCHITECTURE",
            ha="center", va="center", color="#ffffff", fontsize=17, fontweight="bold", family=FONT_FAMILY)
    ax.text(9.0, 8.95, "Automated Continuous Integration, Static Analysis, Containerization, Terraform IaC & Deployment Stages",
            ha="center", va="center", color=ACCENT_BLUE, fontsize=10.5, family=FONT_FAMILY)

    # Stages Row 1 (Stages 1 - 5)
    stages_row1 = [
        {"x": 0.2, "y": 5.0, "w": 3.2, "h": 3.2, "title": "Stage 1: SCM Checkout", "sub": "Git Integration & Workspace",
         "items": ["Repo: YashSabale01/ShalaConnect", "Branch: refs/heads/main", "Webhook / SCM Polling: H/5", "Clean Workspace & Git Log", "Tooling: JDK 21, Maven, TF"], "color": ACCENT_CYAN},
        {"x": 3.8, "y": 5.0, "w": 3.2, "h": 3.2, "title": "Stage 2: Code Quality", "sub": "Static Analysis & SAST",
         "items": ["Maven Compile Check", "Checkstyle Formatting Rules", "SpotBugs Static Analysis", "OWASP Dependency Vulnerability", "Quality Gate: Zero Blocker"], "color": ACCENT_PURPLE},
        {"x": 7.4, "y": 5.0, "w": 3.2, "h": 3.2, "title": "Stage 3: Automated Tests", "sub": "JUnit 5 & Integration Tests",
         "items": ["Spring Boot Starter Test", "MockMvc REST API Contracts", "JUnit 5 Test Suite (48 Tests)", "Surefire XML Report Capture", "Coverage Metric Gate (>85%)"], "color": ACCENT_GREEN},
        {"x": 11.0, "y": 5.0, "w": 3.2, "h": 3.2, "title": "Stage 4: Package Artifact", "sub": "Binary Compilation",
         "items": ["mvn package -DskipTests", "Spring Boot Fat JAR Output", "shalaconnect-backend-1.0.0.jar", "Fingerprint & Archive Artifact", "Build History Retention"], "color": ACCENT_AMBER},
        {"x": 14.6, "y": 5.0, "w": 3.2, "h": 3.2, "title": "Stage 5: Containerize", "sub": "Multi-Stage Docker Build",
         "items": ["Multi-stage Dockerfile", "Base: eclipse-temurin:21-jre", "Build Tag: ${BUILD_NUMBER}-${SHA}", "Image Size Optimization (<240MB)", "Tag as Latest & Build Release"], "color": ACCENT_BLUE},
    ]

    for s in stages_row1:
        draw_card(ax, s["x"], s["y"], s["w"], s["h"], s["title"], s["sub"], s["items"], header_color=s["color"])

    # Arrows Row 1
    for i in range(len(stages_row1) - 1):
        s1 = stages_row1[i]
        s2 = stages_row1[i+1]
        draw_arrow(ax, s1["x"] + s1["w"], s1["y"] + s1["h"]/2, s2["x"], s2["y"] + s2["h"]/2, color="#38bdf8")

    # Connector from Stage 5 to Stage 6
    draw_arrow(ax, 16.2, 5.0, 16.2, 4.3, color="#f59e0b", label="Build OK")

    # Stages Row 2 (Stages 10 <- 9 <- 8 <- 7 <- 6)
    stages_row2 = [
        {"x": 14.6, "y": 0.8, "w": 3.2, "h": 3.2, "title": "Stage 6: Trivy Scan", "sub": "Container Security Audit",
         "items": ["Trivy Vulnerability Audit", "Scan Base Image OS Packages", "CVE Severity Gate (HIGH/CRIT)", "Container Security Policy", "Passed: 0 High Vulnerabilities"], "color": ACCENT_ROSE},
        {"x": 11.0, "y": 0.8, "w": 3.2, "h": 3.2, "title": "Stage 7: Terraform IaC", "sub": "Infrastructure Provisioning",
         "items": ["terraform init & backend check", "terraform validate & fmt", "terraform plan -out=tfplan", "Auto-apply for Staging", "Provisions: VPC, RDS, ALB, ECS"], "color": ACCENT_ORANGE},
        {"x": 7.4, "y": 0.8, "w": 3.2, "h": 3.2, "title": "Stage 8: Deploy Staging", "sub": "Automated Deployment",
         "items": ["Pull Tagged Container Image", "Graceful Container Stop/Rm", "docker run -d --name shalaconnect", "Port Mapping: 8080:8080", "Active Profile: staging"], "color": ACCENT_GREEN},
        {"x": 3.8, "y": 0.8, "w": 3.2, "h": 3.2, "title": "Stage 9: Health Smoke", "sub": "Endpoint Verification",
         "items": ["Automated curl verification loop", "Endpoint: GET /api/health", "HTTP 200 OK Status Assertion", "Validate DB & System Telemetry", "Pass: 100% Operational"], "color": ACCENT_CYAN},
        {"x": 0.2, "y": 0.8, "w": 3.2, "h": 3.2, "title": "Stage 10: Post Actions", "sub": "Feedback & Notification",
         "items": ["Publish JUnit Test Trends", "Clean Staging Workspace", "Retain Pipeline Build History", "Slack / Email Status Broadcast", "Pipeline Result: SUCCESS [PASS]"], "color": ACCENT_PURPLE},
    ]

    for s in stages_row2:
        draw_card(ax, s["x"], s["y"], s["w"], s["h"], s["title"], s["sub"], s["items"], header_color=s["color"])

    # Arrows Row 2 (right to left)
    for i in range(len(stages_row2) - 1):
        s1 = stages_row2[i]
        s2 = stages_row2[i+1]
        draw_arrow(ax, s1["x"], s1["y"] + s1["h"]/2, s2["x"] + s2["w"], s2["y"] + s2["h"]/2, color="#10b981")

    # Author watermark banner
    ax.text(9.0, 0.2, "Author: Yash Janardan Sabale (PRN: 2310423T26-27) | Course: DevOps & Cloud Engineering | Institution: MIT Academy of Engineering, Pune",
            ha="center", va="center", color=TEXT_MUTED, fontsize=8.5, family=FONT_FAMILY)

    plt.tight_layout()
    out_file = DIAGRAMS_DIR / "jenkins_cicd_pipeline_architecture.png"
    plt.savefig(out_file, dpi=300, facecolor=BG_COLOR, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")

# ==============================================================================
# DIAGRAM 2: TERRAFORM AWS INFRASTRUCTURE TOPOLOGY
# ==============================================================================
def generate_terraform_aws_infrastructure_topology():
    fig, ax = plt.subplots(figsize=(18, 11), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(-0.5, 17.5)
    ax.set_ylim(-0.5, 11.0)
    ax.axis("off")

    # Title
    ax.text(8.5, 10.4, "SHALACONNECT TERRAFORM INFRASTRUCTURE AS CODE TOPOLOGY (AWS AP-SOUTH-1)",
            ha="center", va="center", color="#ffffff", fontsize=16, fontweight="bold", family=FONT_FAMILY)
    ax.text(8.5, 9.95, "Modular Multi-AZ VPC Architecture Provisioned via Terraform Modules (VPC, Security, Compute, Database)",
            ha="center", va="center", color=ACCENT_ORANGE, fontsize=10.5, family=FONT_FAMILY)

    # Master VPC Enclosure Box
    vpc_box = patches.FancyBboxPatch(
        (0.5, 0.8), 16.5, 8.8,
        boxstyle="round,pad=0.03,rounding_size=0.2",
        facecolor="#131c31", edgecolor="#3b82f6", linewidth=2.0, linestyle="--", zorder=1
    )
    ax.add_patch(vpc_box)
    ax.text(0.8, 9.3, "AWS VPC (10.0.0.0/16) — Region: ap-south-1 (Mumbai)", color="#60a5fa",
            fontsize=11.5, fontweight="bold", family=FONT_FAMILY, zorder=2)

    # Internet Gateway
    draw_card(ax, 6.5, 8.3, 4.0, 1.1, "Internet Gateway (IGW)", "Bi-directional Public Traffic",
              items=None, header_color=ACCENT_CYAN, fill_color="#1e293b")

    # AZ 1 Container
    az1_box = patches.FancyBboxPatch(
        (1.0, 1.2), 7.2, 6.7,
        boxstyle="round,pad=0.02,rounding_size=0.15",
        facecolor="#162238", edgecolor="#334155", linewidth=1.5, zorder=2
    )
    ax.add_patch(az1_box)
    ax.text(1.3, 7.6, "Availability Zone: ap-south-1a", color="#38bdf8", fontsize=10, fontweight="bold", family=FONT_FAMILY, zorder=3)

    # Public Subnet 1
    draw_card(ax, 1.3, 5.0, 6.6, 2.3, "Public Subnet 1 (10.0.1.0/24)", "ALB Ingress & NAT Tier",
              ["Route: 0.0.0.0/0 -> IGW", "Hosts ALB Interface ap-south-1a", "Auto-assign public IP: Enabled", "Security: alb-sg (Port 80/443)"],
              header_color=ACCENT_CYAN, fill_color="#1e293b")

    # Private Subnet 1
    draw_card(ax, 1.3, 1.6, 6.6, 3.1, "Private Subnet 1 (10.0.10.0/24)", "Application Workload & Data Tier",
              ["No direct route to IGW", "Hosts Spring Boot ECS Task (Port 8080)", "RDS PostgreSQL Instance (Primary Node)", "Security: app-sg (8080 from ALB)", "Security: db-sg (5432 from App)"],
              header_color=ACCENT_GREEN, fill_color="#1e293b")

    # AZ 2 Container
    az2_box = patches.FancyBboxPatch(
        (9.3, 1.2), 7.2, 6.7,
        boxstyle="round,pad=0.02,rounding_size=0.15",
        facecolor="#162238", edgecolor="#334155", linewidth=1.5, zorder=2
    )
    ax.add_patch(az2_box)
    ax.text(9.6, 7.6, "Availability Zone: ap-south-1b", color="#38bdf8", fontsize=10, fontweight="bold", family=FONT_FAMILY, zorder=3)

    # Public Subnet 2
    draw_card(ax, 9.6, 5.0, 6.6, 2.3, "Public Subnet 2 (10.0.2.0/24)", "ALB Ingress & Standby Tier",
              ["Route: 0.0.0.0/0 -> IGW", "Hosts ALB Interface ap-south-1b", "Multi-AZ Load Balancer Resilience", "Security: alb-sg (Port 80/443)"],
              header_color=ACCENT_CYAN, fill_color="#1e293b")

    # Private Subnet 2
    draw_card(ax, 9.6, 1.6, 6.6, 3.1, "Private Subnet 2 (10.0.11.0/24)", "Application Workload & DB Standby",
              ["No direct route to IGW", "Hosts Spring Boot Standby Container Task", "RDS PostgreSQL Multi-AZ Standby / Backup", "Security: app-sg (8080 from ALB)", "Security: db-sg (5432 from App)"],
              header_color=ACCENT_GREEN, fill_color="#1e293b")

    # Central Load Balancer Representation
    draw_card(ax, 6.2, 4.4, 5.1, 1.5, "Application Load Balancer (ALB)", "Public DNS Entry Point",
              ["Health Check: HTTP 200 on /api/health", "Listener: HTTP 80 -> Target Group: 8080"],
              header_color=ACCENT_ORANGE, fill_color="#1e293b")

    # Connection Lines
    draw_arrow(ax, 8.5, 8.3, 8.5, 5.9, color=ACCENT_CYAN, label="Internet Ingress")
    draw_arrow(ax, 6.2, 5.0, 4.5, 4.7, color=ACCENT_ORANGE)
    draw_arrow(ax, 11.3, 5.0, 13.0, 4.7, color=ACCENT_ORANGE)
    draw_arrow(ax, 4.6, 4.7, 4.6, 4.7, color=ACCENT_GREEN)

    # Watermark
    ax.text(8.5, 0.3, "Infrastructure Defined in HCL: vpc.tf, security_groups.tf, rds.tf, alb.tf, ecs.tf | Student: Yash Sabale | PRN: 2310423T26-27",
            ha="center", va="center", color=TEXT_MUTED, fontsize=8.5, family=FONT_FAMILY)

    plt.tight_layout()
    out_file = DIAGRAMS_DIR / "terraform_aws_infrastructure_topology.png"
    plt.savefig(out_file, dpi=300, facecolor=BG_COLOR, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")

# ==============================================================================
# DIAGRAM 3: JENKINS + TERRAFORM INTEGRATION FLOW
# ==============================================================================
def generate_jenkins_terraform_integration_flow():
    fig, ax = plt.subplots(figsize=(18, 10), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(-0.5, 17.5)
    ax.set_ylim(-0.5, 10.0)
    ax.axis("off")

    # Header
    ax.text(8.5, 9.4, "JENKINS & TERRAFORM AUTOMATED PROVISIONING INTEGRATION FLOW",
            ha="center", va="center", color="#ffffff", fontsize=16, fontweight="bold", family=FONT_FAMILY)
    ax.text(8.5, 8.95, "Continuous Delivery Bridge: Automated HCL Compilation, State Validation, Planning, and Zero-Downtime Deployment",
            ha="center", va="center", color=ACCENT_PURPLE, fontsize=10.5, family=FONT_FAMILY)

    # 4 Main Columns
    cols = [
        {"x": 0.5, "y": 1.5, "w": 3.6, "h": 6.8, "title": "1. Jenkins Pipeline Agent", "sub": "Execution Environment",
         "items": ["Jenkins Controller triggers build", "Workspace cloned with Jenkinsfile", "Injects AWS Credential Store tokens", "Verifies Terraform CLI v1.14+", "Sets TF_IN_AUTOMATION=true", "Configures tfvars for target env", "Manages artifact workspace isolation"],
         "color": ACCENT_BLUE},
        {"x": 4.8, "y": 1.5, "w": 3.6, "h": 6.8, "title": "2. Terraform CLI Lifecycle", "sub": "IaC State Management",
         "items": ["terraform init -backend=false/S3", "Downloads AWS Provider v5.100+", "terraform validate (Syntax/Schema)", "terraform fmt -check (Style audit)", "terraform plan -var=env=staging", "Generates binary tfplan artifact", "Deterministic resource graph"],
         "color": ACCENT_PURPLE},
        {"x": 9.1, "y": 1.5, "w": 3.6, "h": 6.8, "title": "3. Cloud API Provisioning", "sub": "AWS Resource Operations",
         "items": ["Calls AWS STS & IAM Role", "VPC & Subnet route table provision", "Security groups ingress rules config", "RDS PostgreSQL multi-AZ instance", "ALB Target Group & Health checks", "ECS Cluster & Task definitions", "Outputs endpoints in JSON"],
         "color": ACCENT_ORANGE},
        {"x": 13.4, "y": 1.5, "w": 3.6, "h": 6.8, "title": "4. Deployment & Verification", "sub": "Post-Provisioning Handshake",
         "items": ["Jenkins ingests alb_dns_name", "Ingests rds_endpoint connection", "Injects DB credentials into container", "Deploys Docker container workload", "Runs automated curl /api/health", "Asserts HTTP 200 UP telemetry", "Sends Slack notification on success"],
         "color": ACCENT_GREEN},
    ]

    for c in cols:
        draw_card(ax, c["x"], c["y"], c["w"], c["h"], c["title"], c["sub"], c["items"], header_color=c["color"])

    # Connecting Arrows
    for i in range(len(cols) - 1):
        c1 = cols[i]
        c2 = cols[i+1]
        draw_arrow(ax, c1["x"] + c1["w"], 4.9, c2["x"], 4.9, color="#a855f7", width=2.5)

    # Watermark
    ax.text(8.5, 0.4, "Student: Yash Janardan Sabale | PRN: 2310423T26-27 | IA Activity No. 3: Jenkins CI/CD + Terraform Mini Project",
            ha="center", va="center", color=TEXT_MUTED, fontsize=8.5, family=FONT_FAMILY)

    plt.tight_layout()
    out_file = DIAGRAMS_DIR / "jenkins_terraform_integration_flow.png"
    plt.savefig(out_file, dpi=300, facecolor=BG_COLOR, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")

# ==============================================================================
# DIAGRAM 4: GITOPS & CONTINUOUS DELIVERY LIFECYCLE
# ==============================================================================
def generate_gitops_deployment_lifecycle():
    fig, ax = plt.subplots(figsize=(18, 10), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(-0.5, 17.5)
    ax.set_ylim(-0.5, 10.0)
    ax.axis("off")

    # Header
    ax.text(8.5, 9.4, "SHALACONNECT GITOPS & CONTINUOUS DELIVERY LIFECYCLE",
            ha="center", va="center", color="#ffffff", fontsize=16, fontweight="bold", family=FONT_FAMILY)
    ax.text(8.5, 8.95, "Feedback Loops, Automated Quality Gates, Infrastructure Versioning, and Zero-Downtime Releases",
            ha="center", va="center", color=ACCENT_GREEN, fontsize=10.5, family=FONT_FAMILY)

    steps = [
        {"x": 0.5, "y": 4.5, "w": 3.6, "h": 3.8, "title": "Developer Push", "sub": "Feature & Main Branches",
         "items": ["Git commit with signed hash", "Pull Request code review", "Merge to 'main' branch", "Triggers GitHub Webhook", "Fast feedback loop (<2 min)"], "color": ACCENT_CYAN},
        {"x": 4.8, "y": 4.5, "w": 3.6, "h": 3.8, "title": "Jenkins CI Gate", "sub": "Build, SAST & Unit Tests",
         "items": ["Maven compile & JUnit 5 tests", "Static lint & security analysis", "Package Spring Boot JAR", "Docker multi-stage build", "Trivy CVE container audit"], "color": ACCENT_BLUE},
        {"x": 9.1, "y": 4.5, "w": 3.6, "h": 3.8, "title": "Terraform IaC Gate", "sub": "Infrastructure Drift & Sync",
         "items": ["HCL syntax validation", "Deterministic plan calculation", "Infrastructure state locking", "Automated staging apply", "Manual gate for production"], "color": ACCENT_ORANGE},
        {"x": 13.4, "y": 4.5, "w": 3.6, "h": 3.8, "title": "Automated CD Gate", "sub": "Deployment & Health Smoke",
         "items": ["Zero-downtime rolling update", "Containerized service launch", "Automated /api/health probe", "Post-deployment validation", "100% Green Status & Alerting"], "color": ACCENT_GREEN},
    ]

    for s in steps:
        draw_card(ax, s["x"], s["y"], s["w"], s["h"], s["title"], s["sub"], s["items"], header_color=s["color"])

    for i in range(len(steps) - 1):
        s1 = steps[i]
        s2 = steps[i+1]
        draw_arrow(ax, s1["x"] + s1["w"], 6.4, s2["x"], 6.4, color="#10b981", width=2.2)

    # Feedback Loop Card at Bottom
    feedback_card = patches.FancyBboxPatch(
        (0.5, 1.2), 16.5, 2.5,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor="#162238", edgecolor="#3b82f6", linewidth=1.5, zorder=2
    )
    ax.add_patch(feedback_card)
    ax.text(8.75, 3.2, "CONTINUOUS OBSERVABILITY, TELEMETRY & FEEDBACK CHANNELS",
            ha="center", va="center", color="#38bdf8", fontsize=11.5, fontweight="bold", family=FONT_FAMILY, zorder=3)
    ax.text(8.75, 2.6, "• Real-time Slack notifications on build pass / fail   • Jenkins JUnit test trend charts archived per commit",
            ha="center", va="center", color=TEXT_COLOR, fontsize=9.0, family=FONT_FAMILY, zorder=3)
    ax.text(8.75, 2.1, "• Prometheus & Grafana application telemetry (/actuator/metrics)   • CloudWatch / ALB target health metrics",
            ha="center", va="center", color=TEXT_COLOR, fontsize=9.0, family=FONT_FAMILY, zorder=3)
    ax.text(8.75, 1.6, "• Automated Rollback: Pipeline automatically halts and maintains previous stable release if health smoke test fails",
            ha="center", va="center", color="#f87171", fontsize=9.0, fontweight="bold", family=FONT_FAMILY, zorder=3)

    # Watermark
    ax.text(8.5, 0.4, "Student: Yash Janardan Sabale (PRN: 2310423T26-27) | Course: DevOps & Cloud Engineering | MIT Academy of Engineering",
            ha="center", va="center", color=TEXT_MUTED, fontsize=8.5, family=FONT_FAMILY)

    plt.tight_layout()
    out_file = DIAGRAMS_DIR / "gitops_deployment_lifecycle.png"
    plt.savefig(out_file, dpi=300, facecolor=BG_COLOR, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")

if __name__ == "__main__":
    print("=" * 60)
    print(" GENERATING PUBLICATION-GRADE ARCHITECTURE DIAGRAMS (IA3)")
    print("=" * 60)
    generate_jenkins_cicd_pipeline_architecture()
    generate_terraform_aws_infrastructure_topology()
    generate_jenkins_terraform_integration_flow()
    generate_gitops_deployment_lifecycle()
    print("=" * 60)
    print(" ALL 4 DIAGRAMS SUCCESSFULLY GENERATED AT 300 DPI!")
    print("=" * 60)
