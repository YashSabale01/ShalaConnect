import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, ArrowStyle

os.makedirs("Project_Management_Submissions/Assignment_1_WBS/Diagrams", exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E0'

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

def draw_scope_hierarchy():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title Banner
    ax.add_patch(FancyBboxPatch((0.5, 8.2), 15.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(8.0, 8.55, "SHALACONNECT - COMPREHENSIVE PROJECT SCOPE HIERARCHY & BOUNDARIES",
            color=WHITE, fontsize=14, fontweight='bold', ha='center', va='center')

    # Level 0: Project Core
    ax.add_patch(FancyBboxPatch((5.0, 6.9), 6.0, 0.9, boxstyle="round,pad=0.1", fc=SLATE, ec=NAVY, lw=2))
    ax.text(8.0, 7.45, "ShalaConnect Core Platform", color=WHITE, fontsize=12, fontweight='bold', ha='center')
    ax.text(8.0, 7.15, "School Education Cluster Governance (Java 21 / Spring Boot 3.2 / React 18 / AWS)",
            color='#E2E8F0', fontsize=8.5, ha='center')

    # Left Container: In-Scope Deliverables
    ax.add_patch(FancyBboxPatch((0.5, 0.5), 9.6, 6.0, boxstyle="round,pad=0.1", fc=WHITE, ec=GREEN, lw=2.5))
    ax.add_patch(FancyBboxPatch((0.7, 5.9), 9.2, 0.5, boxstyle="round,pad=0.05", fc=GREEN, ec=GREEN))
    ax.text(5.3, 6.15, "AUTHORIZED IN-SCOPE PROJECT CAPABILITIES (100% BASELINE)", color=WHITE, fontsize=10.5, fontweight='bold', ha='center')

    in_scope_items = [
        ("1. Multi-Tenant School Registry & Administration", "Centralized profile management, UDISE+ validation, accreditation tracking across 20 cluster schools."),
        ("2. Teacher Rationalization & Service Allocation", "Subject-wise teacher allocation, transfer logs, qualification mapping to satisfy RTE 10-point ratios."),
        ("3. Student Enrollment & Automated Promotion", "Student life-cycle records, category management, bulk CSV roster ingestion with format sanitization."),
        ("4. Mobile PWA Daily Attendance & Geo-Fencing", "Offline-first attendance capture, GPS 100m geofence validation, mock-location anti-spoofing."),
        ("5. School Inspection & Compliance Scoring Engine", "Standardized RTE compliance audits, infrastructure scores, digital inspection report generator."),
        ("6. Document Vault & OCR Certificate Verification", "Secure AWS S3 document vault, Tesseract OCR automated certificate and scan verification."),
        ("7. District Analytics BI Dashboard & Alerts", "Real-time cluster KPIs, student-teacher ratio visualizations, automated parent SMS notifications.")
    ]

    for idx, (title, desc) in enumerate(in_scope_items):
        y_pos = 5.2 - (idx * 0.75)
        ax.add_patch(FancyBboxPatch((0.8, y_pos), 9.0, 0.65, boxstyle="round,pad=0.08", fc=LIGHT_BLUE, ec='#90CDF4', lw=1.2))
        ax.text(1.0, y_pos + 0.42, title, color=NAVY, fontsize=9.5, fontweight='bold', ha='left')
        ax.text(1.0, y_pos + 0.18, desc, color=TEXT_DARK, fontsize=7.5, ha='left')

    # Right Container: Explicit Out-of-Scope Exclusions
    ax.add_patch(FancyBboxPatch((10.4, 0.5), 5.1, 6.0, boxstyle="round,pad=0.1", fc=WHITE, ec=RED, lw=2.5))
    ax.add_patch(FancyBboxPatch((10.6, 5.9), 4.7, 0.5, boxstyle="round,pad=0.05", fc=RED, ec=RED))
    ax.text(12.95, 6.15, "EXPLICIT OUT-OF-SCOPE EXCLUSIONS", color=WHITE, fontsize=10.5, fontweight='bold', ha='center')

    out_scope_items = [
        ("Hardware Procurement & Subsidies", "No supply or maintenance of school tablets, PCs, or biometric hardware devices."),
        ("Direct Banking & Fee Payments", "No direct payment gateway integration for student tuition fee collections or vendor payouts."),
        ("Payroll & Salary Computation", "No core accounting or monthly payroll disbursal calculation for teaching faculty."),
        ("Pre-2020 Archive Digitization", "Excludes manual retrospective data entry of legacy paper archives pre-dating 2020."),
        ("Private On-Premise Servers", "Excludes deployment or maintenance on private on-premise district physical servers.")
    ]

    for idx, (title, desc) in enumerate(out_scope_items):
        y_pos = 5.0 - (idx * 1.05)
        ax.add_patch(FancyBboxPatch((10.7, y_pos), 4.5, 0.9, boxstyle="round,pad=0.08", fc='#FFF5F5', ec='#FEB2B2', lw=1.2))
        ax.text(10.9, y_pos + 0.62, f"[EXCL] {title}", color=RED, fontsize=9.0, fontweight='bold', ha='left')
        ax.text(10.9, y_pos + 0.25, desc, color=TEXT_DARK, fontsize=7.5, ha='left', wrap=True)

    # Connecting Arrows
    ax.annotate("", xy=(5.3, 6.5), xytext=(7.0, 6.9), arrowprops=dict(arrowstyle="->", lw=2, color=GREEN))
    ax.annotate("", xy=(12.9, 6.5), xytext=(9.0, 6.9), arrowprops=dict(arrowstyle="->", lw=2, color=RED, ls="--"))

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.2)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_1_WBS/Diagrams/scope_hierarchy.png", dpi=300)
    plt.close()
    print("Scope hierarchy diagram generated successfully!")

def draw_wbs_master_architecture():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 8.2), 15.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(8.0, 8.55, "SHALACONNECT - LEVEL 1 & LEVEL 2 MASTER WORK BREAKDOWN STRUCTURE (100% RULE)",
            color=WHITE, fontsize=13, fontweight='bold', ha='center', va='center')

    # Root Node
    ax.add_patch(FancyBboxPatch((5.5, 7.1), 5.0, 0.8, boxstyle="round,pad=0.1", fc=SLATE, ec=NAVY, lw=2))
    ax.text(8.0, 7.55, "1.0 ShalaConnect Governance Platform", color=WHITE, fontsize=11, fontweight='bold', ha='center')
    ax.text(8.0, 7.28, "Total Cost Baseline: INR 4,10,000 | 54 Working Days CPM", color='#E2E8F0', fontsize=8, ha='center')

    # 5 Level-1 Phases
    phase_configs = [
        ("1.1 Project Inception & Requirements", "3 Work Packages | INR 60,000", 1.8, '#2B6CB0'),
        ("1.2 Architectural Foundation", "4 Work Packages | INR 1,32,000", 4.9, '#2C7A7B'),
        ("1.3 Core Educational Modules", "9 Work Packages | INR 1,49,000", 8.0, '#C05621'),
        ("1.4 Testing & Quality Assurance", "3 Work Packages | INR 33,500", 11.1, '#6B46C1'),
        ("1.5 Deployment & Handover", "2 Work Packages | INR 35,500", 14.2, '#2F855A')
    ]

    for title, sub, x_center, color in phase_configs:
        # Phase Box
        ax.add_patch(FancyBboxPatch((x_center - 1.4, 5.6), 2.8, 0.9, boxstyle="round,pad=0.08", fc=color, ec=NAVY, lw=1.5))
        ax.text(x_center, 6.15, title, color=WHITE, fontsize=8.5, fontweight='bold', ha='center', wrap=True)
        ax.text(x_center, 5.82, sub, color='#E2E8F0', fontsize=7.2, ha='center')
        # Connector from Root
        ax.annotate("", xy=(x_center, 6.5), xytext=(8.0, 7.1), arrowprops=dict(arrowstyle="->", lw=1.5, color=SLATE))

    # Level 2 Deliverables Boxes below each phase
    l2_deliverables = [
        # Phase 1.1
        [("1.1.1 Stakeholder SRS v1.0", "Signed SRS, user personas"),
         ("1.1.2 C4 Architecture Blueprint", "High-level specs, component APIs"),
         ("1.1.3 Regulatory Compliance Checklist", "NEP 2020 & DPDPA 2023 review")],
        # Phase 1.2
        [("1.2.1 PostgreSQL 16 Multi-Tenant DDL", "Schema partitioning, Liquibase"),
         ("1.2.2 AWS Cloud VPC & Terraform", "Terraform IAC, ALB, S3, Security"),
         ("1.2.3 Spring Boot 3.2 Services Setup", "Security filters, Maven base"),
         ("1.2.4 Docker Containerization & ECS", "Multi-stage build, ECS Fargate")],
        # Phase 1.3
        [("1.3.1 Auth & RBAC Security Engine", "JWT lifecycle, BCrypt hashing"),
         ("1.3.2 School Profile & Registry APIs", "UDISE+ validation, CRUD services"),
         ("1.3.3 Teacher Allocation Module", "Subject mapping, transfer ledger"),
         ("1.3.4 Student Enrollment & Bulk CSV", "Admissions, class promotion"),
         ("1.3.5 Mobile PWA Attendance & Geo", "HTML5 Geofence 100m, SQLite sync"),
         ("1.3.6 School Inspection & Audit Engine", "RTE 10-point checklist scores"),
         ("1.3.7 District Analytics BI Dashboard", "React 18 charts, cluster KPIs"),
         ("1.3.8 S3 Document Vault & OCR Engine", "Tesseract certificate scanning"),
         ("1.3.9 Automated SMS Alert Gateway", "Transactional Twilio notifications")],
        # Phase 1.4
        [("1.4.1 Playwright E2E Integration Suite", "Automated business journeys"),
         ("1.4.2 Apache JMeter Load & Scalability", "1,000 concurrent user simulation"),
         ("1.4.3 OWASP ZAP Security Audit", "Vulnerability scans, pentest fix")],
        # Phase 1.5
        [("1.5.1 Pilot District UAT Acceptance", "20 Cluster Headmaster sign-off"),
         ("1.5.2 Production Deployment & Handover", "Route 53 DNS cutover, manuals")]
    ]

    for p_idx, l2_list in enumerate(l2_deliverables):
        x_center = phase_configs[p_idx][2]
        total_items = len(l2_list)
        box_h = 0.45 if total_items > 4 else 0.65
        spacing = 0.52 if total_items > 4 else 0.78
        y_start = 5.3

        for i, (deliv_title, deliv_desc) in enumerate(l2_list):
            y_box = y_start - (i * spacing) - box_h
            ax.add_patch(FancyBboxPatch((x_center - 1.4, y_box), 2.8, box_h, boxstyle="round,pad=0.05", fc=WHITE, ec=BORDER_GRAY, lw=1))
            ax.text(x_center - 1.3, y_box + box_h * 0.65, deliv_title, color=NAVY, fontsize=7.2, fontweight='bold', ha='left')
            ax.text(x_center - 1.3, y_box + box_h * 0.25, deliv_desc, color=TEXT_MUTED, fontsize=6.2, ha='left')
            # Line connector from phase
            ax.plot([x_center, x_center], [y_start, y_box + box_h], color=BORDER_GRAY, lw=0.8)

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.2)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_1_WBS/Diagrams/wbs_hierarchy.png", dpi=300)
    plt.close()
    print("Master WBS hierarchy diagram generated successfully!")

def draw_stakeholder_matrix():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 9.1), 13.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(7.0, 9.45, "SHALACONNECT - STAKEHOLDER POWER-INTEREST ANALYSIS (2x2 GRID)",
            color=WHITE, fontsize=13, fontweight='bold', ha='center', va='center')

    # Grid Container
    ax.add_patch(Rectangle((1.5, 1.2), 11.0, 7.2, fc=WHITE, ec=BORDER_GRAY, lw=2))

    # Quadrant Dividers
    ax.plot([7.0, 7.0], [1.2, 8.4], color='#A0AEC0', lw=2, ls='--')
    ax.plot([1.5, 12.5], [4.8, 4.8], color='#A0AEC0', lw=2, ls='--')

    # Quadrant 1: Top-Right (HIGH POWER, HIGH INTEREST) -> MANAGE CLOSELY
    ax.add_patch(FancyBboxPatch((7.2, 5.0), 5.1, 3.2, boxstyle="round,pad=0.1", fc='#EBF8FF', ec='#90CDF4', lw=1.5))
    ax.text(9.75, 7.95, "MANAGE CLOSELY (High Power / High Interest)", color='#2B6CB0', fontsize=10.5, fontweight='bold', ha='center')
    
    stk_q1 = [
        ("Dr. Academic Sponsor (MITAOE Faculty Board)", "Executive steering, institutional sign-off, budget authorization.", "Bi-weekly milestone reviews"),
        ("District Education Officer (DEO, Zilla Parishad)", "Statutory adoption, pilot district authorization, UAT sign-off.", "Fortnightly executive demo"),
        ("Lead Systems Architect & PM (Yash Sabale)", "Technical governance, CPM schedule tracking, EVM control.", "Daily standup & sprint review")
    ]
    for idx, (name, role, comm) in enumerate(stk_q1):
        y = 7.4 - (idx * 0.9)
        ax.add_patch(FancyBboxPatch((7.4, y), 4.7, 0.75, boxstyle="round,pad=0.06", fc=WHITE, ec='#BEE3F8', lw=1))
        ax.text(7.5, y + 0.52, f"• {name}", color=NAVY, fontsize=8.0, fontweight='bold', ha='left')
        ax.text(7.65, y + 0.30, role, color=TEXT_DARK, fontsize=6.8, ha='left')
        ax.text(7.65, y + 0.12, f"Comm: {comm}", color='#2B6CB0', fontsize=6.5, fontstyle='italic', ha='left')

    # Quadrant 2: Top-Left (HIGH POWER, LOW INTEREST) -> KEEP SATISFIED
    ax.add_patch(FancyBboxPatch((1.7, 5.0), 5.1, 3.2, boxstyle="round,pad=0.1", fc='#FEFCBF', ec='#FAF089', lw=1.5))
    ax.text(4.25, 7.95, "KEEP SATISFIED (High Power / Low Interest)", color='#B7791F', fontsize=10.5, fontweight='bold', ha='center')
    
    stk_q2 = [
        ("State IT Directorate / Data Protection Officer", "DPDPA 2023 legal compliance, cloud security guidelines.", "Monthly security compliance reports"),
        ("MITAOE Department Quality Assurance Cell", "Academic curriculum alignment, accreditation records.", "Mid-term & final audit dossiers")
    ]
    for idx, (name, role, comm) in enumerate(stk_q2):
        y = 7.1 - (idx * 1.1)
        ax.add_patch(FancyBboxPatch((1.9, y), 4.7, 0.85, boxstyle="round,pad=0.06", fc=WHITE, ec='#F6E05E', lw=1))
        ax.text(2.0, y + 0.60, f"• {name}", color='#744210', fontsize=8.0, fontweight='bold', ha='left')
        ax.text(2.15, y + 0.35, role, color=TEXT_DARK, fontsize=6.8, ha='left')
        ax.text(2.15, y + 0.15, f"Comm: {comm}", color='#B7791F', fontsize=6.5, fontstyle='italic', ha='left')

    # Quadrant 3: Bottom-Right (LOW POWER, HIGH INTEREST) -> KEEP INFORMED
    ax.add_patch(FancyBboxPatch((7.2, 1.4), 5.1, 3.2, boxstyle="round,pad=0.1", fc='#F0FFF4', ec='#9AE6B4', lw=1.5))
    ax.text(9.75, 4.35, "KEEP INFORMED (Low Power / High Interest)", color='#276749', fontsize=10.5, fontweight='bold', ha='center')
    
    stk_q3 = [
        ("Cluster Headmasters (20 Pilot ZP Schools)", "School registry testing, teacher assignment feedback.", "Weekly feedback sprint sessions"),
        ("Primary School Teachers (150+ Faculty)", "Daily geo-attendance app usage, class enrollment inputs.", "PWA user manuals & WhatsApp helpdesk"),
        ("Student Parents & School Management Committees", "Daily attendance SMS notifications, academic alerts.", "Automated transactional SMS")
    ]
    for idx, (name, role, comm) in enumerate(stk_q3):
        y = 3.8 - (idx * 0.9)
        ax.add_patch(FancyBboxPatch((7.4, y), 4.7, 0.75, boxstyle="round,pad=0.06", fc=WHITE, ec='#C6F6D5', lw=1))
        ax.text(7.5, y + 0.52, f"• {name}", color='#22543D', fontsize=8.0, fontweight='bold', ha='left')
        ax.text(7.65, y + 0.30, role, color=TEXT_DARK, fontsize=6.8, ha='left')
        ax.text(7.65, y + 0.12, f"Comm: {comm}", color='#276749', fontsize=6.5, fontstyle='italic', ha='left')

    # Quadrant 4: Bottom-Left (LOW POWER, LOW INTEREST) -> MONITOR
    ax.add_patch(FancyBboxPatch((1.7, 1.4), 5.1, 3.2, boxstyle="round,pad=0.1", fc='#EDF2F7', ec='#CBD5E0', lw=1.5))
    ax.text(4.25, 4.35, "MONITOR (Low Power / Low Interest)", color='#4A5568', fontsize=10.5, fontweight='bold', ha='center')
    
    stk_q4 = [
        ("Third-Party Cloud & SMS Vendors (AWS, Twilio)", "Infrastructure hosting, API uptime, SMS gateway deliverability.", "Automated CloudWatch alerts"),
        ("General Academic Community & Peer Students", "Project awareness, open-source code repo visibility.", "Public GitHub documentation")
    ]
    for idx, (name, role, comm) in enumerate(stk_q4):
        y = 3.5 - (idx * 1.1)
        ax.add_patch(FancyBboxPatch((1.9, y), 4.7, 0.85, boxstyle="round,pad=0.06", fc=WHITE, ec='#E2E8F0', lw=1))
        ax.text(2.0, y + 0.60, f"• {name}", color='#2D3748', fontsize=8.0, fontweight='bold', ha='left')
        ax.text(2.15, y + 0.35, role, color=TEXT_DARK, fontsize=6.8, ha='left')
        ax.text(2.15, y + 0.15, f"Comm: {comm}", color='#4A5568', fontsize=6.5, fontstyle='italic', ha='left')

    # Axis Labels
    ax.text(7.0, 0.7, "LEVEL OF STAKEHOLDER INTEREST  →", color=NAVY, fontsize=11, fontweight='bold', ha='center')
    ax.text(0.8, 4.8, "STAKEHOLDER POWER / INFLUENCE  →", color=NAVY, fontsize=11, fontweight='bold', va='center', rotation=90)

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10.2)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_1_WBS/Diagrams/stakeholder_matrix.png", dpi=300)
    plt.close()
    print("Stakeholder power-interest matrix generated successfully!")

def draw_organization_structure():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 7.6), 14.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(7.5, 7.95, "SHALACONNECT - PROJECT GOVERNANCE & ORGANIZATIONAL HIERARCHY",
            color=WHITE, fontsize=13, fontweight='bold', ha='center', va='center')

    # Level 1: Executive Steering Board
    ax.add_patch(FancyBboxPatch((5.0, 6.4), 5.0, 0.8, boxstyle="round,pad=0.1", fc='#2A4365', ec=NAVY, lw=1.5))
    ax.text(7.5, 6.9, "PROJECT STEERING COMMITTEE", color=WHITE, fontsize=10, fontweight='bold', ha='center')
    ax.text(7.5, 6.6, "MITAOE Faculty Board & District Education Officer (DEO)", color='#E2E8F0', fontsize=7.5, ha='center')

    # Level 2: Project Manager / Solutions Architect
    ax.add_patch(FancyBboxPatch((5.2, 5.0), 4.6, 0.85, boxstyle="round,pad=0.1", fc=SLATE, ec=NAVY, lw=2))
    ax.text(7.5, 5.55, "PROJECT MANAGER & LEAD ARCHITECT", color=WHITE, fontsize=10.5, fontweight='bold', ha='center')
    ax.text(7.5, 5.25, "Yash Sabale (Full-Stack Engineering & Governance)", color='#FEFCBF', fontsize=8, ha='center')

    # Connect L1 to L2
    ax.annotate("", xy=(7.5, 5.85), xytext=(7.5, 6.4), arrowprops=dict(arrowstyle="->", lw=2, color=NAVY))

    # Level 3: Specialized Functional Leads
    roles = [
        ("Database & Storage Lead", "PostgreSQL 16 Multi-Tenancy\nLiquibase DDL & RDS Multi-AZ", 1.5, '#2C7A7B'),
        ("Backend Services Lead", "Spring Boot 3.2 Microservices\nJWT RBAC, API Performance", 4.5, '#2B6CB0'),
        ("Frontend & PWA Lead", "React 18 & Vite Ecosystem\nOffline PWA & Geofencing", 7.5, '#C05621'),
        ("DevOps & Cloud Lead", "AWS ECS Fargate & ALB\nTerraform IAC & GitHub CI/CD", 10.5, '#6B46C1'),
        ("Quality & Security Lead", "Playwright E2E & Load Testing\nOWASP ZAP & SonarQube", 13.5, '#2F855A')
    ]

    for title, desc, x, color in roles:
        ax.add_patch(FancyBboxPatch((x - 1.3, 2.7), 2.6, 1.4, boxstyle="round,pad=0.08", fc=WHITE, ec=color, lw=2))
        ax.add_patch(FancyBboxPatch((x - 1.3, 3.65), 2.6, 0.45, boxstyle="round,pad=0.04", fc=color, ec=color))
        ax.text(x, 3.88, title, color=WHITE, fontsize=8.0, fontweight='bold', ha='center')
        ax.text(x, 3.15, desc, color=TEXT_DARK, fontsize=7.0, ha='center', va='center')

        # Connector from PM
        ax.plot([7.5, x], [4.6, 4.6], color=SLATE, lw=1.2)
        ax.plot([x, x], [4.6, 4.1], color=SLATE, lw=1.2)
        ax.annotate("", xy=(x, 4.1), xytext=(x, 4.3), arrowprops=dict(arrowstyle="->", lw=1.2, color=SLATE))

    ax.plot([7.5, 7.5], [5.0, 4.6], color=SLATE, lw=1.2)

    # Bottom Callout: Key Stakeholder Working Groups
    ax.add_patch(FancyBboxPatch((0.8, 0.5), 13.4, 1.5, boxstyle="round,pad=0.1", fc=LIGHT_BLUE, ec='#90CDF4', lw=1.2))
    ax.text(7.5, 1.7, "DISTRICT WORKING GROUPS & FIELD LIAISONS", color=NAVY, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(3.5, 1.1, "• 20 Cluster Headmaster Pilot Panel (Weekly Feedback)\n• 150+ ZP Primary Teachers (UAT Testing & Usability)", color=TEXT_DARK, fontsize=8, ha='left')
    ax.text(9.5, 1.1, "• District IT Officer & Block Education Officers (Regulatory)\n• Student Parents SMC Committees (Notification Audit)", color=TEXT_DARK, fontsize=8, ha='left')

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_1_WBS/Diagrams/project_organization_structure.png", dpi=300)
    plt.close()
    print("Project organization structure diagram generated successfully!")

if __name__ == "__main__":
    draw_scope_hierarchy()
    draw_wbs_master_architecture()
    draw_stakeholder_matrix()
    draw_organization_structure()
    print("All Assignment 1 diagrams successfully redesigned and exported!")
