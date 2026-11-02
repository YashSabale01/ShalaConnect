import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

os.makedirs("Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams", exist_ok=True)
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

def draw_kanban_workflow():
    fig, ax = plt.subplots(figsize=(18, 9), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 8.1), 17.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(9.0, 8.45, "SHALACONNECT - AGILE KANBAN PULL FRAMEWORK & STAGE GOVERNANCE",
            color=WHITE, fontsize=13, fontweight='bold', ha='center', va='center')

    # 5 Column Definitions
    cols = [
        ("1. BACKLOG", "WIP: No Limit", "Prioritized work packages pending sprint intake.", 0.6, '#4A5568', '#EDF2F7'),
        ("2. READY FOR DEV", "WIP: Limit 5", "Elaborated specs, reviewed acceptance criteria.", 3.9, '#2B6CB0', '#EBF8FF'),
        ("3. IN PROGRESS", "WIP: Limit 3 (STRICT)", "Active coding in flight. Pull blocked if WIP >= 3.", 7.2, AMBER, '#FEFCBF'),
        ("4. TESTING & QA", "WIP: Limit 3 (STRICT)", "Playwright integration, JMeter load, OWASP pentest.", 10.5, '#6B46C1', '#FAF5FF'),
        ("5. DONE / VERIFIED", "WIP: No Limit", "100% Definition of Done (DoD) passed & accepted.", 13.8, GREEN, '#F0FFF4')
    ]

    for title, wip, desc, x, head_col, bg_col in cols:
        # Outer Column Container
        ax.add_patch(FancyBboxPatch((x, 1.2), 3.1, 6.5, boxstyle="round,pad=0.08", fc=bg_col, ec=BORDER_GRAY, lw=1.5))
        # Header Box
        ax.add_patch(FancyBboxPatch((x, 7.0), 3.1, 0.7, boxstyle="round,pad=0.04", fc=head_col, ec=head_col))
        ax.text(x + 1.55, 7.42, title, color=WHITE, fontsize=9.0, fontweight='bold', ha='center')
        ax.text(x + 1.55, 7.15, wip, color='#FEFCBF', fontsize=7.8, fontweight='bold', ha='center')
        # Subtitle policy
        ax.text(x + 1.55, 6.70, desc, color=TEXT_DARK, fontsize=6.8, ha='center', wrap=True)

    # Sample Task Cards in each column representing Day 35 Snapshot
    # Ready
    ax.add_patch(FancyBboxPatch((4.1, 5.2), 2.7, 1.0, boxstyle="round,pad=0.05", fc=WHITE, ec=RED, lw=1.5))
    ax.text(4.2, 5.9, "ACT-16: Automated SMS", color=NAVY, fontsize=7.5, fontweight='bold')
    ax.text(4.2, 5.6, "3d | INR 18,000 | CRITICAL", color=RED, fontsize=6.8, fontweight='bold')
    ax.text(4.2, 5.35, "Full-Stack Developer", color=TEXT_MUTED, fontsize=6.8)

    ax.add_patch(FancyBboxPatch((4.1, 3.9), 2.7, 1.0, boxstyle="round,pad=0.05", fc=WHITE, ec=RED, lw=1.5))
    ax.text(4.2, 4.6, "ACT-17: Integration QA", color=NAVY, fontsize=7.5, fontweight='bold')
    ax.text(4.2, 4.3, "5d | INR 27,000 | CRITICAL", color=RED, fontsize=6.8, fontweight='bold')
    ax.text(4.2, 4.05, "Lead QA Engineer", color=TEXT_MUTED, fontsize=6.8)

    # In Progress (2 items, limit 3)
    ax.add_patch(FancyBboxPatch((7.4, 5.2), 2.7, 1.0, boxstyle="round,pad=0.05", fc=WHITE, ec=RED, lw=2))
    ax.text(7.5, 5.9, "ACT-14: District BI Dashboard", color=NAVY, fontsize=7.5, fontweight='bold')
    ax.text(7.5, 5.6, "4d | INR 24,000 | CRITICAL", color=RED, fontsize=6.8, fontweight='bold')
    ax.text(7.5, 5.35, "UI Lead (Chart.js / React)", color=TEXT_MUTED, fontsize=6.8)

    # Testing & QA (2 items, limit 3)
    ax.add_patch(FancyBboxPatch((10.7, 5.2), 2.7, 1.0, boxstyle="round,pad=0.05", fc=WHITE, ec=RED, lw=2))
    ax.text(10.8, 5.9, "ACT-15: Document Vault OCR", color=NAVY, fontsize=7.5, fontweight='bold')
    ax.text(10.8, 5.6, "4d | INR 19,500 | CRITICAL", color=RED, fontsize=6.8, fontweight='bold')
    ax.text(10.8, 5.35, "AI/ML Lead (Tesseract Scan)", color=TEXT_MUTED, fontsize=6.8)

    # Done (13 Completed items)
    ax.add_patch(FancyBboxPatch((14.0, 5.2), 2.7, 1.2, boxstyle="round,pad=0.05", fc=WHITE, ec=GREEN, lw=1.5))
    ax.text(14.1, 6.05, "13 Tasks Completed (EV)", color=GREEN, fontsize=8.0, fontweight='bold')
    ax.text(14.1, 5.75, "ACT-01 to ACT-13 Accepted", color=NAVY, fontsize=7.2, fontweight='bold')
    ax.text(14.1, 5.48, "Total EV: INR 2,97,000", color='#276749', fontsize=7.2, fontweight='bold')
    ax.text(14.1, 5.25, "100% Quality Gates Passed", color=TEXT_MUTED, fontsize=6.8)

    # Pull Direction Arrows between columns
    for arrow_x in [3.7, 7.0, 10.3, 13.6]:
        ax.annotate("", xy=(arrow_x + 0.18, 4.5), xytext=(arrow_x - 0.18, 4.5),
                    arrowprops=dict(arrowstyle="->", lw=2.2, color=SLATE))

    # Little's Law Bottom Banner
    ax.add_patch(FancyBboxPatch((0.5, 0.4), 17.0, 0.65, boxstyle="round,pad=0.08", fc=NAVY, ec=NAVY))
    ax.text(9.0, 0.72, "LITTLE'S LAW ENGINE: WIP = Throughput (lambda = 0.37 tasks/day) x Cycle Time (W = 16.2 days). Strict WIP limit (<=6 in flight) prevents queue bottlenecks and context switching.",
            color=WHITE, fontsize=8.0, fontweight='bold', ha='center', va='center')

    ax.set_xlim(0, 18)
    ax.set_ylim(0, 9.0)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams/kanban_workflow_diagram.png", dpi=300)
    plt.close()
    print("Kanban workflow diagram generated successfully!")

def draw_raci_matrix():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 10.2), 15.0, 0.65, boxstyle="round,pad=0.08", fc=NAVY, ec=NAVY))
    ax.text(8.0, 10.52, "SHALACONNECT - RESPONSIBILITY ASSIGNMENT MATRIX (RACI) WITH SINGLE ACCOUNTABILITY",
            color=WHITE, fontsize=12, fontweight='bold', ha='center', va='center')

    # Roles
    roles = ["PM / Lead Architect", "Backend Lead", "Frontend / PWA", "DBA Lead", "DevOps Engineer", "QA & Security"]
    wbs_tasks = [
        ("1.1.1 Stakeholder Requirements", ["A", "C", "C", "C", "I", "C"]),
        ("1.1.2 Architecture & C4 Blueprints", ["A", "C", "C", "C", "C", "C"]),
        ("1.1.3 Regulatory Compliance Review", ["A", "I", "I", "I", "I", "C"]),
        ("1.2.1 PostgreSQL 16 Multi-Tenancy", ["C", "C", "I", "A", "C", "I"]),
        ("1.2.2 Cloud VPC & Terraform IAC", ["C", "I", "I", "C", "A", "C"]),
        ("1.2.3 Spring Boot 3.2 Scaffolding", ["C", "A", "C", "C", "C", "I"]),
        ("1.2.4 Docker & ECS Fargate Setup", ["I", "C", "I", "I", "A", "C"]),
        ("1.3.1 Authentication & RBAC Engine", ["C", "A", "C", "C", "C", "C"]),
        ("1.3.2 School Registry Profile APIs", ["I", "A", "C", "C", "I", "I"]),
        ("1.3.3 Teacher Allocation Module", ["I", "A", "C", "C", "I", "I"]),
        ("1.3.4 Student Enrollment Bulk CSV", ["I", "A", "C", "C", "I", "I"]),
        ("1.3.5 Attendance PWA & Geofencing", ["I", "C", "A", "I", "I", "C"]),
        ("1.3.6 School Inspection Audit Engine", ["I", "A", "C", "C", "I", "I"]),
        ("1.3.7 District Analytics BI Dashboard", ["I", "C", "A", "I", "I", "I"]),
        ("1.3.8 Document Vault OCR Engine", ["C", "A", "C", "C", "C", "I"]),
        ("1.3.9 Automated SMS Alert Gateway", ["I", "A", "C", "I", "C", "I"]),
        ("1.4.1 Playwright E2E Integration", ["I", "C", "C", "I", "C", "A"]),
        ("1.4.2 JMeter Load & Scalability", ["I", "C", "I", "C", "C", "A"]),
        ("1.4.3 OWASP ZAP Security Audit", ["C", "C", "I", "I", "C", "A"]),
        ("1.5.1 Pilot District UAT Sign-Off", ["A", "C", "C", "I", "I", "C"]),
        ("1.5.2 Production DNS Cutover", ["C", "C", "I", "I", "A", "C"]),
    ]

    # Draw Table Headers
    ax.add_patch(Rectangle((0.5, 9.4), 6.5, 0.6, fc=SLATE, ec=BORDER_GRAY))
    ax.text(3.75, 9.7, "WBS Work Package", color=WHITE, fontsize=8.5, fontweight='bold', ha='center')

    for col_idx, role in enumerate(roles):
        x = 7.0 + (col_idx * 1.45)
        ax.add_patch(Rectangle((x, 9.4), 1.45, 0.6, fc=SLATE, ec=BORDER_GRAY))
        ax.text(x + 0.725, 9.7, role, color=WHITE, fontsize=6.8, fontweight='bold', ha='center', wrap=True)

    # Draw Matrix Rows
    y_start = 9.4
    row_h = 0.38

    for row_idx, (task_name, assignments) in enumerate(wbs_tasks):
        y = y_start - ((row_idx + 1) * row_h)
        bg = WHITE if row_idx % 2 == 0 else '#F7FAFC'

        # Task Name Cell
        ax.add_patch(Rectangle((0.5, y), 6.5, row_h, fc=bg, ec=BORDER_GRAY))
        ax.text(0.7, y + 0.12, task_name, color=NAVY, fontsize=7.2, fontweight='bold', ha='left')

        # RACI Cells
        for col_idx, raci_val in enumerate(assignments):
            x = 7.0 + (col_idx * 1.45)
            # Highlight 'A' in amber/gold
            cell_bg = '#FEFCBF' if raci_val == 'A' else bg
            ax.add_patch(Rectangle((x, y), 1.45, row_h, fc=cell_bg, ec=BORDER_GRAY))
            text_color = RED if raci_val == 'A' else (NAVY if raci_val == 'R' else TEXT_MUTED)
            ax.text(x + 0.725, y + 0.12, raci_val, color=text_color, fontsize=8.5, fontweight='bold' if raci_val in ['A', 'R'] else 'normal', ha='center')

    # Legend at bottom
    ax.add_patch(FancyBboxPatch((0.5, 0.5), 15.0, 0.6, boxstyle="round,pad=0.06", fc=WHITE, ec=BORDER_GRAY))
    ax.text(8.0, 0.78, "RACI LEGEND: R = Responsible (Does work) | A = Accountable (Single owner - exactly one 'A' per row) | C = Consulted (Provides input) | I = Informed (Notified)",
            color=NAVY, fontsize=7.5, fontweight='bold', ha='center')

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams/raci_matrix_diagram.png", dpi=300)
    plt.close()
    print("RACI matrix diagram generated successfully!")

def draw_execution_workflow():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 7.6), 14.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(7.5, 7.95, "SHALACONNECT - EXECUTION CONTROL & ISSUE ESCALATION WORKFLOW",
            color=WHITE, fontsize=12, fontweight='bold', ha='center', va='center')

    # Workflow Steps
    steps = [
        ("1. Daily Standup (15m)", "Review In Progress tasks\nIdentify blockers & WIP limits", 1.8, 5.4, '#2B6CB0'),
        ("2. Blocker Detection", "Task stalled > 4 hours?\nWIP limit breached?", 5.2, 5.4, AMBER),
        ("3. Internal Resolution", "Peer pair-programming\nDevOps infrastructure fix", 8.6, 5.4, '#2C7A7B'),
        ("4. QA Verification Gate", "Playwright automated test\n100% acceptance gate", 12.0, 5.4, GREEN),
        ("5. Formal CCB Escalation", "Scope alteration / Regulatory shift\nSponsor approval needed?", 5.2, 2.4, RED),
        ("6. Management Reserve", "Drawdown from INR 34,000 reserve\nBaseline updated & versioned", 9.5, 2.4, '#6B46C1')
    ]

    for title, desc, x, y, col in steps:
        ax.add_patch(FancyBboxPatch((x - 1.4, y - 0.7), 2.8, 1.4, boxstyle="round,pad=0.08", fc=WHITE, ec=col, lw=2))
        ax.add_patch(FancyBboxPatch((x - 1.4, y + 0.35), 2.8, 0.35, boxstyle="round,pad=0.03", fc=col, ec=col))
        ax.text(x, y + 0.52, title, color=WHITE, fontsize=7.8, fontweight='bold', ha='center')
        ax.text(x, y - 0.15, desc, color=TEXT_DARK, fontsize=7.0, ha='center', va='center')

    # Horizontal Flow Arrows (1 -> 2 -> 3 -> 4)
    ax.annotate("", xy=(3.6, 5.4), xytext=(3.2, 5.4), arrowprops=dict(arrowstyle="->", lw=2, color=SLATE))
    ax.annotate("", xy=(7.0, 5.4), xytext=(6.6, 5.4), arrowprops=dict(arrowstyle="->", lw=2, color=SLATE))
    ax.annotate("", xy=(10.4, 5.4), xytext=(10.0, 5.4), arrowprops=dict(arrowstyle="->", lw=2, color=SLATE))

    # Escalation Path from 2 down to 5
    ax.annotate("Unresolved >24h", xy=(5.2, 3.1), xytext=(5.2, 4.7),
                arrowprops=dict(arrowstyle="->", lw=2, color=RED, ls='--'),
                color=RED, fontsize=7.2, fontweight='bold', ha='right')

    # From 5 to 6
    ax.annotate("Scope Impact Approved", xy=(7.9, 2.4), xytext=(6.6, 2.4),
                arrowprops=dict(arrowstyle="->", lw=2, color=RED),
                color=RED, fontsize=7.2, fontweight='bold', ha='center', va='bottom')

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams/execution_monitoring_workflow.png", dpi=300)
    plt.close()
    print("Execution monitoring workflow diagram generated successfully!")

def draw_evm_scurve():
    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)

    days = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 54]
    # Planned Value (PV)
    pv = [0, 35000, 75000, 120000, 175000, 230000, 280000, 320000, 355000, 385000, 402000, 410000]
    # Earned Value (EV) up to Day 35
    ev_days = [0, 5, 10, 15, 20, 25, 30, 35]
    ev = [0, 35000, 75000, 115000, 168000, 220000, 265000, 297000]
    # Actual Cost (AC) up to Day 35
    ac = [0, 33000, 71000, 109000, 160000, 210000, 252000, 282857]

    # Plot Curves
    ax.plot(days, pv, color='#2B6CB0', lw=2.5, label='Planned Value (PV Baseline)')
    ax.plot(ev_days, ev, color=GREEN, lw=3.0, marker='o', label='Earned Value (EV = INR 2,97,000 at Day 35)')
    ax.plot(ev_days, ac, color=RED, lw=2.5, marker='s', ls='--', label='Actual Cost (AC = INR 2,82,857 at Day 35)')

    # Projected EAC Curve from Day 35 to Day 54
    eac_days = [35, 40, 45, 50, 54]
    eac_proj = [282857, 315000, 345000, 372000, 390476]
    ax.plot(eac_days, eac_proj, color='#805AD5', lw=2.0, ls=':', label='Forecasted Expenditure (EAC = INR 3,90,476)')

    # Vertical Audit Line at Day 35
    ax.axvline(35, color=AMBER, lw=2.0, ls='-.', label='Mid-Project Audit Baseline (Day 35)')

    # Highlight Variances at Day 35
    ax.annotate("CV = +INR 14,143 (Under Budget, CPI=1.05)", xy=(35, 282857), xytext=(22, 230000),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=GREEN),
                color=GREEN, fontsize=8.5, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc=WHITE, ec=GREEN))

    ax.annotate("SV = -INR 23,000 (Minor Lag, SPI=0.93)", xy=(35, 297000), xytext=(22, 340000),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=AMBER),
                color=AMBER, fontsize=8.5, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc=WHITE, ec=AMBER))

    ax.set_xlabel("Working Days along Critical Path Timeline (0 to 54 Days)", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_ylabel("Cost & Earned Value (INR)", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_title("SHALACONNECT - DAY 35 EARNED VALUE MANAGEMENT (EVM) PERFORMANCE S-CURVE", fontsize=13, fontweight='bold', color=NAVY, pad=15)
    ax.set_xlim(0, 55)
    ax.set_ylim(0, 440000)
    ax.grid(color=BORDER_GRAY, ls=':', lw=0.8)
    ax.legend(loc='upper left', frameon=True, facecolor=WHITE, edgecolor=BORDER_GRAY, fontsize=9)

    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams/evm_scurve_analysis.png", dpi=300)
    plt.close()
    print("EVM S-Curve diagram generated successfully!")

def draw_cost_performance_dashboard():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    fig.patch.set_facecolor(GRAY_BG)

    # Left: CPI Progression Across Milestones
    milestones = ["Day 10", "Day 20", "Day 25", "Day 30", "Day 35 (Audit)"]
    cpi_vals = [1.056, 1.050, 1.047, 1.051, 1.050]
    ax1.plot(milestones, cpi_vals, color=GREEN, marker='o', lw=2.5)
    ax1.axhline(1.0, color=RED, ls='--', lw=1.5, label='Efficiency Parity (CPI = 1.0)')
    ax1.set_ylim(0.9, 1.15)
    ax1.set_ylabel("Cost Performance Index (CPI)", fontsize=10, fontweight='bold', color=NAVY)
    ax1.set_title("CPI Efficiency Trend (Sustained > 1.0 Favorable)", fontsize=11, fontweight='bold', color=NAVY)
    ax1.grid(color=BORDER_GRAY, ls=':', lw=0.8)
    ax1.legend(loc='lower right', facecolor=WHITE)

    # Right: Cost Variance by Control Account
    cas = ["CA-01", "CA-02", "CA-03", "CA-04", "CA-05"]
    cv_vals = [3200, 6800, 4143, 0, 0] # Favorable cost savings
    bars = ax2.bar(cas, cv_vals, color='#2B6CB0', width=0.5)
    for b in bars:
        h = b.get_height()
        if h > 0:
            ax2.text(b.get_x() + b.get_width()/2, h + 200, f"+INR {h:,.0f}", ha='center', fontsize=8.5, fontweight='bold', color=GREEN)

    ax2.set_ylabel("Cost Variance (INR)", fontsize=10, fontweight='bold', color=NAVY)
    ax2.set_title("Cost Variance (CV = EV - AC) by Control Account\nTotal Surplus: +INR 14,143 (Under Budget)", fontsize=11, fontweight='bold', color=NAVY)
    ax2.set_ylim(0, 8500)
    ax2.grid(axis='y', color=BORDER_GRAY, ls=':', lw=0.8)

    plt.suptitle("SHALACONNECT - COST PERFORMANCE INDEX & CONTROL ACCOUNT AUDIT", fontsize=13, fontweight='bold', color=NAVY, y=0.98)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams/cost_performance_dashboard.png", dpi=300)
    plt.close()
    print("Cost performance dashboard generated successfully!")

def draw_schedule_performance_dashboard():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    fig.patch.set_facecolor(GRAY_BG)

    # Left: SPI Progression Across Milestones
    milestones = ["Day 10", "Day 20", "Day 25", "Day 30", "Day 35 (Audit)"]
    spi_vals = [1.000, 0.960, 0.956, 0.946, 0.928]
    ax1.plot(milestones, spi_vals, color=AMBER, marker='s', lw=2.5)
    ax1.axhline(1.0, color=GREEN, ls='--', lw=1.5, label='On-Schedule Parity (SPI = 1.0)')
    ax1.set_ylim(0.85, 1.1)
    ax1.set_ylabel("Schedule Performance Index (SPI)", fontsize=10, fontweight='bold', color=NAVY)
    ax1.set_title("SPI Progression (Minor Latency in OCR Non-Critical Path)", fontsize=11, fontweight='bold', color=NAVY)
    ax1.grid(color=BORDER_GRAY, ls=':', lw=0.8)
    ax1.legend(loc='lower left', facecolor=WHITE)

    # Right: Float Buffer Utilization
    buffer_cats = ["Deterministic CP (54d)", "OCR Path Latency (2d)", "Operational Buffer (26d)", "Semester Limit (80d)"]
    buffer_vals = [54, 2, 26, 80]
    colors = [RED, AMBER, '#2B6CB0', NAVY]
    bars = ax2.bar(buffer_cats, buffer_vals, color=colors, width=0.55)
    for b in bars:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 2, f"{h} Days", ha='center', fontsize=9.0, fontweight='bold', color=NAVY)

    ax2.set_ylabel("Working Days", fontsize=10, fontweight='bold', color=NAVY)
    ax2.set_title("Schedule Buffer Protection Against Overrun\n(26-Day Operational Buffer Absorbs Minor SV)", fontsize=11, fontweight='bold', color=NAVY)
    ax2.set_ylim(0, 95)
    ax2.grid(axis='y', color=BORDER_GRAY, ls=':', lw=0.8)

    plt.suptitle("SHALACONNECT - SCHEDULE PERFORMANCE INDEX & FLOAT BUFFER AUDIT", fontsize=13, fontweight='bold', color=NAVY, y=0.98)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams/schedule_performance_dashboard.png", dpi=300)
    plt.close()
    print("Schedule performance dashboard generated successfully!")

if __name__ == "__main__":
    draw_kanban_workflow()
    draw_raci_matrix()
    draw_execution_workflow()
    draw_evm_scurve()
    draw_cost_performance_dashboard()
    draw_schedule_performance_dashboard()
    print("All Assignment 3 diagrams successfully generated!")
