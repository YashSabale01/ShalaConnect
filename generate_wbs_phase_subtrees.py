import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

os.makedirs("Project_Management_Submissions/Assignment_1_WBS/Diagrams", exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

NAVY = '#1B365D'
SLATE = '#2C5282'
LIGHT_BLUE = '#EBF8FF'
AMBER = '#D97706'
GREEN = '#059669'
RED = '#DC2626'
GRAY_BG = '#F7FAFC'
BORDER_GRAY = '#CBD5E0'
WHITE = '#FFFFFF'
TEXT_DARK = '#1A202C'
TEXT_MUTED = '#4A5568'

def draw_wbs_phase1_2():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 7.6), 14.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(7.5, 7.95, "SHALACONNECT - DETAILED WORK PACKAGE BREAKDOWN: PHASES 1.0 & 2.0",
            color=WHITE, fontsize=13, fontweight='bold', ha='center', va='center')

    # Phase 1 Header
    ax.add_patch(FancyBboxPatch((0.5, 6.4), 6.5, 0.7, boxstyle="round,pad=0.08", fc='#2B6CB0', ec=NAVY))
    ax.text(3.75, 6.75, "Phase 1.0: Project Inception & Requirements (INR 60,000 | 10d)", color=WHITE, fontsize=10, fontweight='bold', ha='center')

    p1_items = [
        ("1.1.1 Stakeholder Requirements Gathering", "Deliverable: Signed SRS v1.0, user persona catalog", "Duration: 3 Working Days | Cost: INR 18,000", "Lead Systems Analyst | Predecessors: None"),
        ("1.1.2 System Architecture & C4 Blueprints", "Deliverable: Component interaction specs, database ERD", "Duration: 4 Working Days | Cost: INR 24,000", "Solutions Architect | Predecessors: 1.1.1"),
        ("1.1.3 Regulatory Compliance & Privacy Framework", "Deliverable: DPDPA 2023 & NEP 2020 compliance signed checklist", "Duration: 3 Working Days | Cost: INR 18,000", "Legal & Compliance Specialist | Predecessors: 1.1.2")
    ]
    for idx, (t, d, dc, rp) in enumerate(p1_items):
        y = 5.2 - (idx * 1.5)
        ax.add_patch(FancyBboxPatch((0.5, y), 6.5, 1.3, boxstyle="round,pad=0.08", fc=WHITE, ec='#2B6CB0', lw=1.5))
        ax.text(0.7, y + 0.98, t, color=NAVY, fontsize=9.0, fontweight='bold', ha='left')
        ax.text(0.7, y + 0.70, d, color=TEXT_DARK, fontsize=7.8, ha='left')
        ax.text(0.7, y + 0.42, dc, color='#2B6CB0', fontsize=7.5, fontweight='bold', ha='left')
        ax.text(0.7, y + 0.16, rp, color=TEXT_MUTED, fontsize=7.2, ha='left')

    # Phase 2 Header
    ax.add_patch(FancyBboxPatch((7.8, 6.4), 6.7, 0.7, boxstyle="round,pad=0.08", fc='#2C7A7B', ec=NAVY))
    ax.text(11.15, 6.75, "Phase 2.0: Architectural Foundation (INR 1,32,000 | 18d)", color=WHITE, fontsize=10, fontweight='bold', ha='center')

    p2_items = [
        ("1.2.1 PostgreSQL 16 Multi-Tenancy DDL", "Deliverable: Tenant schemas, Liquibase migration codebase", "Duration: 4 Working Days | Cost: INR 30,000", "Database Administrator Lead | Predecessors: 1.1.2"),
        ("1.2.2 AWS Cloud VPC & Terraform IAC", "Deliverable: Terraform modules for VPC, subnets, ALB, S3", "Duration: 5 Working Days | Cost: INR 36,000", "DevOps Engineer | Predecessors: 1.2.1"),
        ("1.2.3 Spring Boot 3.2 Services Scaffolding", "Deliverable: Base Maven setup, Spring Security JWT filter", "Duration: 5 Working Days | Cost: INR 42,000", "Senior Backend Lead | Predecessors: 1.2.1"),
        ("1.2.4 Docker Containerization & ECS Fargate", "Deliverable: Multi-stage Dockerfile (<180MB), ECS tasks", "Duration: 4 Working Days | Cost: INR 24,000", "DevOps Engineer | Predecessors: 1.2.2, 1.2.3")
    ]
    for idx, (t, d, dc, rp) in enumerate(p2_items):
        y = 5.2 - (idx * 1.35)
        ax.add_patch(FancyBboxPatch((7.8, y), 6.7, 1.2, boxstyle="round,pad=0.08", fc=WHITE, ec='#2C7A7B', lw=1.5))
        ax.text(8.0, y + 0.90, t, color=NAVY, fontsize=8.8, fontweight='bold', ha='left')
        ax.text(8.0, y + 0.65, d, color=TEXT_DARK, fontsize=7.5, ha='left')
        ax.text(8.0, y + 0.40, dc, color='#2C7A7B', fontsize=7.2, fontweight='bold', ha='left')
        ax.text(8.0, y + 0.16, rp, color=TEXT_MUTED, fontsize=7.0, ha='left')

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_1_WBS/Diagrams/wbs_phase1_2_detail.png", dpi=300)
    plt.close()
    print("WBS Phase 1 & 2 detail generated successfully!")

def draw_wbs_phase3():
    fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 8.6), 15.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(8.0, 8.95, "SHALACONNECT - DETAILED WORK PACKAGE BREAKDOWN: PHASE 3.0 (CORE MODULES)",
            color=WHITE, fontsize=13, fontweight='bold', ha='center', va='center')

    # Phase 3 Header
    ax.add_patch(FancyBboxPatch((0.5, 7.8), 15.0, 0.6, boxstyle="round,pad=0.08", fc='#C05621', ec=NAVY))
    ax.text(8.0, 8.1, "Phase 3.0: Core Educational Services & Governance Modules (9 Work Packages | INR 1,49,000 | 40d)",
            color=WHITE, fontsize=10.5, fontweight='bold', ha='center')

    p3_items = [
        ("1.3.1 Authentication & RBAC Engine", "JWT lifecycle, BCrypt, role filters", "4d | INR 30,000", "Security Lead", "1.2.3"),
        ("1.3.2 School Registry & Profiles", "UDISE+ code validation, school CRUD", "5d | INR 26,500", "Backend Dev", "1.3.1"),
        ("1.3.3 Teacher Allocation Module", "Subject mapping, transfer ledger", "5d | INR 29,000", "Full-Stack Dev", "1.3.2"),
        ("1.3.4 Student Enrollment & Bulk CSV", "Admissions, class promotion, 500 rows/5s", "6d | INR 34,000", "Full-Stack Dev", "1.3.3"),
        ("1.3.5 Attendance & Geo-Fencing PWA", "Offline-first PWA, 100m geofence radius", "5d | INR 26,500", "Mobile Lead", "1.3.3"),
        ("1.3.6 School Inspection Engine", "RTE 10-point checklist scores, audit log", "4d | INR 21,500", "Backend Dev", "1.3.3"),
        ("1.3.7 District Analytics BI Dashboard", "React 18 charts, cluster KPIs, 1.2s p95", "4d | INR 24,000", "UI/UX Lead", "1.3.6"),
        ("1.3.8 S3 Document Vault & OCR", "Tesseract certificate scanning, >85% acc", "4d | INR 19,500", "AI/ML Lead", "1.3.6"),
        ("1.3.9 Automated SMS Alert Gateway", "Transactional Twilio notifications <10s", "3d | INR 18,000", "Full-Stack Dev", "1.3.7, 1.3.8")
    ]

    # Render as 3x3 Grid of clear cards
    for idx, (title, deliv, cost_dur, role, pred) in enumerate(p3_items):
        col = idx % 3
        row = idx // 3
        x = 0.5 + (col * 5.1)
        y = 5.3 - (row * 2.3)

        ax.add_patch(FancyBboxPatch((x, y), 4.8, 2.1, boxstyle="round,pad=0.08", fc=WHITE, ec='#C05621', lw=1.5))
        ax.add_patch(FancyBboxPatch((x, y + 1.55), 4.8, 0.55, boxstyle="round,pad=0.04", fc='#FEEBC8', ec='#FEEBC8'))
        ax.text(x + 0.2, y + 1.82, title, color='#7B341E', fontsize=9.0, fontweight='bold', ha='left')
        ax.text(x + 0.2, y + 1.25, f"Deliverable: {deliv}", color=TEXT_DARK, fontsize=7.8, ha='left')
        ax.text(x + 0.2, y + 0.88, f"Duration & Budget: {cost_dur}", color=NAVY, fontsize=7.8, fontweight='bold', ha='left')
        ax.text(x + 0.2, y + 0.52, f"Assigned: {role}", color='#2B6CB0', fontsize=7.5, ha='left')
        ax.text(x + 0.2, y + 0.20, f"Predecessors: {pred}", color=TEXT_MUTED, fontsize=7.2, fontstyle='italic', ha='left')

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.5)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_1_WBS/Diagrams/wbs_phase3_detail.png", dpi=300)
    plt.close()
    print("WBS Phase 3 detail generated successfully!")

def draw_wbs_phase4_5():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 7.6), 14.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(7.5, 7.95, "SHALACONNECT - DETAILED WORK PACKAGE BREAKDOWN: PHASES 4.0 & 5.0",
            color=WHITE, fontsize=13, fontweight='bold', ha='center', va='center')

    # Phase 4 Header
    ax.add_patch(FancyBboxPatch((0.5, 6.4), 6.6, 0.7, boxstyle="round,pad=0.08", fc='#6B46C1', ec=NAVY))
    ax.text(3.8, 6.75, "Phase 4.0: Quality Assurance & Testing (INR 33,500 | 12d)", color=WHITE, fontsize=10, fontweight='bold', ha='center')

    p4_items = [
        ("1.4.1 Playwright E2E Integration Suite", "Deliverable: Automated test scripts, 100% pass on critical paths", "Duration: 5 Working Days | Cost: INR 27,000", "Lead QA Engineer | Predecessors: 1.3.9"),
        ("1.4.2 Apache JMeter Load & Scalability Test", "Deliverable: 1,000 concurrent session test report, p95 < 500ms", "Duration: 4 Working Days | Cost: INR 22,000", "DevOps / QA Specialist | Predecessors: 1.4.1"),
        ("1.4.3 OWASP ZAP Security Audit & Pentest", "Deliverable: Zero high/critical CVEs, SonarQube Quality Gate A", "Duration: 3 Working Days | Cost: INR 18,500", "Security Auditor Lead | Predecessors: 1.4.1")
    ]
    for idx, (t, d, dc, rp) in enumerate(p4_items):
        y = 5.0 - (idx * 1.5)
        ax.add_patch(FancyBboxPatch((0.5, y), 6.6, 1.3, boxstyle="round,pad=0.08", fc=WHITE, ec='#6B46C1', lw=1.5))
        ax.text(0.7, y + 0.98, t, color=NAVY, fontsize=9.0, fontweight='bold', ha='left')
        ax.text(0.7, y + 0.70, d, color=TEXT_DARK, fontsize=7.8, ha='left')
        ax.text(0.7, y + 0.42, dc, color='#6B46C1', fontsize=7.5, fontweight='bold', ha='left')
        ax.text(0.7, y + 0.16, rp, color=TEXT_MUTED, fontsize=7.2, ha='left')

    # Phase 5 Header
    ax.add_patch(FancyBboxPatch((7.7, 6.4), 6.8, 0.7, boxstyle="round,pad=0.08", fc='#2F855A', ec=NAVY))
    ax.text(11.1, 6.75, "Phase 5.0: Deployment & Handover (INR 35,500 | 9d)", color=WHITE, fontsize=10, fontweight='bold', ha='center')

    p5_items = [
        ("1.5.1 Pilot District User Acceptance Testing (UAT)", "Deliverable: 20 cluster headmaster UAT test sign-off sheets", "Duration: 4 Working Days | Cost: INR 14,500", "Lead QA Engineer & PM | Predecessors: 1.4.2, 1.4.3"),
        ("1.5.2 Production Deployment & Operations Handover", "Deliverable: Route 53 DNS cutover, admin manuals, runbooks", "Duration: 5 Working Days | Cost: INR 21,000", "DevOps Engineer & PM | Predecessors: 1.4.3")
    ]
    for idx, (t, d, dc, rp) in enumerate(p5_items):
        y = 4.8 - (idx * 1.8)
        ax.add_patch(FancyBboxPatch((7.7, y), 6.8, 1.5, boxstyle="round,pad=0.08", fc=WHITE, ec='#2F855A', lw=1.5))
        ax.text(7.9, y + 1.15, t, color=NAVY, fontsize=9.0, fontweight='bold', ha='left')
        ax.text(7.9, y + 0.82, d, color=TEXT_DARK, fontsize=7.8, ha='left')
        ax.text(7.9, y + 0.50, dc, color='#2F855A', fontsize=7.5, fontweight='bold', ha='left')
        ax.text(7.9, y + 0.20, rp, color=TEXT_MUTED, fontsize=7.2, ha='left')

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_1_WBS/Diagrams/wbs_phase4_5_detail.png", dpi=300)
    plt.close()
    print("WBS Phase 4 & 5 detail generated successfully!")

if __name__ == "__main__":
    draw_wbs_phase1_2()
    draw_wbs_phase3()
    draw_wbs_phase4_5()
    print("All WBS Phase Sub-tree diagrams successfully generated!")
