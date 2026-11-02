import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

os.makedirs("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams", exist_ok=True)
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

def draw_aon_network_diagram():
    fig, ax = plt.subplots(figsize=(20, 11), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title Banner
    ax.add_patch(FancyBboxPatch((0.5, 10.1), 19.0, 0.75, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(10.0, 10.48, "SHALACONNECT - COMPLETE ACTIVITY-ON-NODE (AON) CPM NETWORK DIAGRAM",
            color=WHITE, fontsize=14, fontweight='bold', ha='center', va='center')

    # Legend Block
    ax.add_patch(FancyBboxPatch((13.5, 8.8), 5.8, 1.1, boxstyle="round,pad=0.08", fc=WHITE, ec=BORDER_GRAY, lw=1.2))
    ax.text(16.4, 9.68, "Standard CPM Node Legend (7-Block Standard)", color=NAVY, fontsize=8.5, fontweight='bold', ha='center')
    ax.text(14.0, 9.38, "ES: Early Start", color=TEXT_DARK, fontsize=7.2)
    ax.text(16.2, 9.38, "D: Duration (Days)", color=TEXT_DARK, fontsize=7.2)
    ax.text(18.2, 9.38, "EF: Early Finish", color=TEXT_DARK, fontsize=7.2)
    ax.text(14.0, 9.08, "LS: Late Start", color=TEXT_DARK, fontsize=7.2)
    ax.text(16.2, 9.08, "TF: Total Float", color=RED, fontsize=7.2, fontweight='bold')
    ax.text(18.2, 9.08, "LF: Late Finish", color=TEXT_DARK, fontsize=7.2)

    # 21 Activities Position Coordinates & Data
    # (id, name, dur, es, ef, ls, lf, tf, is_crit, x, y)
    nodes = [
        ("ACT-01", "Requirements", 3, 0, 3, 0, 3, 0, True, 1.2, 5.0),
        ("ACT-02", "Arch & Specs", 4, 3, 7, 3, 7, 0, True, 3.4, 5.0),
        ("ACT-03", "Compliance", 3, 7, 10, 38, 41, 31, False, 5.6, 7.8),
        ("ACT-04", "DB Schema", 4, 7, 11, 7, 11, 0, True, 5.6, 5.0),
        ("ACT-05", "Cloud VPC", 5, 11, 16, 12, 17, 1, False, 7.8, 7.0),
        ("ACT-06", "Spring Core", 5, 11, 16, 11, 16, 0, True, 7.8, 5.0),
        ("ACT-07", "Docker ECS", 4, 16, 20, 37, 41, 21, False, 9.8, 7.0),
        ("ACT-08", "Auth RBAC", 4, 16, 20, 16, 20, 0, True, 9.8, 5.0),
        ("ACT-09", "School Reg", 5, 20, 25, 20, 25, 0, True, 11.8, 5.0),
        ("ACT-10", "Teacher Alloc", 5, 25, 30, 25, 30, 0, True, 13.8, 5.0),
        ("ACT-11", "Student Enr", 6, 30, 36, 35, 41, 5, False, 15.6, 7.4),
        ("ACT-12", "Attendance", 5, 30, 35, 36, 41, 6, False, 15.6, 6.2),
        ("ACT-13", "Inspection", 4, 30, 34, 30, 34, 0, True, 15.6, 5.0),
        ("ACT-14", "District BI", 4, 34, 38, 34, 38, 0, True, 17.6, 5.6),
        ("ACT-15", "Doc Vault", 4, 34, 38, 34, 38, 0, True, 17.6, 4.4),
        ("ACT-16", "SMS Gateway", 3, 38, 41, 38, 41, 0, True, 17.6, 2.6),
        ("ACT-17", "Integration", 5, 41, 46, 41, 46, 0, True, 14.8, 1.8),
        ("ACT-18", "Load Test", 4, 46, 50, 46, 50, 0, False, 12.0, 1.8),
        ("ACT-19", "Security Pent", 3, 46, 49, 46, 49, 0, True, 9.2, 1.8),
        ("ACT-20", "Pilot UAT", 4, 49, 53, 50, 54, 1, False, 6.4, 2.8),
        ("ACT-21", "Prod Cutover", 5, 49, 54, 49, 54, 0, True, 6.4, 1.2),
    ]

    node_dict = {n[0]: n for n in nodes}

    # Helper function to render a standard 7-box CPM node
    def draw_cpm_node(act_id, name, dur, es, ef, ls, lf, tf, is_crit, x, y):
        w = 1.7
        h = 0.95
        fc_head = RED if is_crit else SLATE
        ec_box = RED if is_crit else '#4A5568'
        lw = 2.2 if is_crit else 1.2

        # Outer card
        ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.03", fc=WHITE, ec=ec_box, lw=lw))
        # Top Header (ES | Dur | EF)
        ax.add_patch(FancyBboxPatch((x - w/2, y + h*0.15), w, h*0.35, boxstyle="round,pad=0.01", fc=fc_head, ec=fc_head))
        ax.text(x - w*0.33, y + h*0.30, str(es), color=WHITE, fontsize=7.5, fontweight='bold', ha='center')
        ax.text(x, y + h*0.30, f"{dur}d", color='#FEFCBF', fontsize=7.5, fontweight='bold', ha='center')
        ax.text(x + w*0.33, y + h*0.30, str(ef), color=WHITE, fontsize=7.5, fontweight='bold', ha='center')

        # Middle Label (ID: Name)
        ax.text(x, y - h*0.05, f"{act_id}: {name}", color=NAVY, fontsize=7.0, fontweight='bold', ha='center')

        # Bottom Row (LS | TF | LF)
        ax.text(x - w*0.33, y - h*0.36, str(ls), color=TEXT_MUTED, fontsize=7.0, ha='center')
        ax.text(x, y - h*0.36, f"TF={tf}", color=RED if is_crit else TEXT_DARK, fontsize=7.2, fontweight='bold' if is_crit else 'normal', ha='center')
        ax.text(x + w*0.33, y - h*0.36, str(lf), color=TEXT_MUTED, fontsize=7.0, ha='center')

    # Draw Nodes
    for n in nodes:
        act_id, name, dur, es, ef, ls, lf, tf, is_crit, x, y = n
        draw_cpm_node(act_id, name, dur, es, ef, ls, lf, tf, is_crit, x, y)

    # Dependency Connections (from_id, to_id, is_crit)
    edges = [
        ("ACT-01", "ACT-02", True),
        ("ACT-02", "ACT-03", False),
        ("ACT-02", "ACT-04", True),
        ("ACT-04", "ACT-05", False),
        ("ACT-04", "ACT-06", True),
        ("ACT-05", "ACT-07", False),
        ("ACT-06", "ACT-07", False),
        ("ACT-06", "ACT-08", True),
        ("ACT-08", "ACT-09", True),
        ("ACT-09", "ACT-10", True),
        ("ACT-10", "ACT-11", False),
        ("ACT-10", "ACT-12", False),
        ("ACT-10", "ACT-13", True),
        ("ACT-13", "ACT-14", True),
        ("ACT-13", "ACT-15", True),
        ("ACT-14", "ACT-16", True),
        ("ACT-15", "ACT-16", True),
        ("ACT-16", "ACT-17", True),
        ("ACT-03", "ACT-17", False),
        ("ACT-07", "ACT-17", False),
        ("ACT-11", "ACT-17", False),
        ("ACT-12", "ACT-17", False),
        ("ACT-17", "ACT-18", False),
        ("ACT-17", "ACT-19", True),
        ("ACT-18", "ACT-20", False),
        ("ACT-19", "ACT-20", False),
        ("ACT-19", "ACT-21", True),
    ]

    for u_id, v_id, is_crit in edges:
        u = node_dict[u_id]
        v = node_dict[v_id]
        ux, uy = u[9], u[10]
        vx, vy = v[9], v[10]

        color = RED if is_crit else '#A0AEC0'
        lw = 2.4 if is_crit else 1.2
        ls = '-' if is_crit else '--'

        # Arrow calculation offset
        dx = vx - ux
        dy = vy - uy
        start_x = ux + 0.85 if dx > 0 else (ux - 0.85 if dx < 0 else ux)
        start_y = uy
        end_x = vx - 0.85 if dx > 0 else (vx + 0.85 if dx < 0 else vx)
        end_y = vy

        ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
                    arrowprops=dict(arrowstyle="->", lw=lw, color=color, ls=ls, shrinkA=3, shrinkB=3))

    # Critical Path Bottom Note
    ax.add_patch(FancyBboxPatch((0.5, 0.4), 19.0, 0.55, boxstyle="round,pad=0.08", fc='#FFF5F5', ec=RED, lw=1.5))
    ax.text(10.0, 0.67, "MATHEMATICAL CRITICAL PATH (54 WORKING DAYS, TF=0): ACT-01 -> ACT-02 -> ACT-04 -> ACT-06 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-13 -> ACT-14 -> ACT-16 -> ACT-17 -> ACT-19 -> ACT-21",
            color=RED, fontsize=8.5, fontweight='bold', ha='center', va='center')

    ax.set_xlim(0, 20)
    ax.set_ylim(0, 11)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/aon_network_diagram.png", dpi=300)
    plt.close()
    print("AON Network diagram generated successfully!")

def draw_critical_path_traversal():
    fig, ax = plt.subplots(figsize=(18, 6), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 4.9), 17.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(9.0, 5.25, "SHALACONNECT - DEDICATED CRITICAL PATH TRAVERSAL (13 ZERO-FLOAT ACTIVITIES)",
            color=WHITE, fontsize=12, fontweight='bold', ha='center', va='center')

    cp_nodes = [
        ("ACT-01", "Reqs", 3, 0, 3),
        ("ACT-02", "Arch", 4, 3, 7),
        ("ACT-04", "DB Schema", 4, 7, 11),
        ("ACT-06", "Spring", 5, 11, 16),
        ("ACT-08", "Auth", 4, 16, 20),
        ("ACT-09", "School Reg", 5, 20, 25),
        ("ACT-10", "Teacher", 5, 25, 30),
        ("ACT-13", "Inspection", 4, 30, 34),
        ("ACT-14", "Dist BI", 4, 34, 38),
        ("ACT-16", "SMS Gate", 3, 38, 41),
        ("ACT-17", "Integ QA", 5, 41, 46),
        ("ACT-19", "Security", 3, 46, 49),
        ("ACT-21", "Cutover", 5, 49, 54),
    ]

    for idx, (act_id, name, dur, es, ef) in enumerate(cp_nodes):
        x = 0.8 + (idx * 1.25)
        y = 2.6

        # Circle Node
        circle = plt.Circle((x, y), 0.45, fc=RED, ec=NAVY, lw=2)
        ax.add_patch(circle)
        ax.text(x, y + 0.08, act_id, color=WHITE, fontsize=7.2, fontweight='bold', ha='center')
        ax.text(x, y - 0.18, f"{dur}d", color='#FEFCBF', fontsize=7.0, fontweight='bold', ha='center')

        # Text below
        ax.text(x, y - 0.75, name, color=NAVY, fontsize=7.2, fontweight='bold', ha='center')
        ax.text(x, y - 1.05, f"d{es} - d{ef}", color=TEXT_MUTED, fontsize=6.8, ha='center')

        # Arrow to next
        if idx < len(cp_nodes) - 1:
            next_x = 0.8 + ((idx + 1) * 1.25)
            ax.annotate("", xy=(next_x - 0.48, y), xytext=(x + 0.48, y),
                        arrowprops=dict(arrowstyle="->", lw=2.2, color=RED))

    # Bottom Timeline Bar
    ax.add_patch(FancyBboxPatch((0.8, 0.6), 15.5, 0.4, boxstyle="round,pad=0.04", fc=WHITE, ec=BORDER_GRAY))
    ax.text(0.8, 0.35, "Day 0 (Start)", color=NAVY, fontsize=8, fontweight='bold', ha='center')
    ax.text(8.5, 0.35, "Continuous Zero-Float Sequence (Total Float = 0 Days)", color=RED, fontsize=8.5, fontweight='bold', ha='center')
    ax.text(16.3, 0.35, "Day 54 (Finish)", color=GREEN, fontsize=8, fontweight='bold', ha='center')

    ax.set_xlim(0, 18)
    ax.set_ylim(0, 5.8)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/critical_path_traversal.png", dpi=300)
    plt.close()
    print("Critical path traversal diagram generated successfully!")

def draw_gantt_chart():
    fig, ax = plt.subplots(figsize=(18, 11), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)

    # 21 Activities with (id, name, start, dur, is_crit)
    gantt_data = [
        ("ACT-01", "Requirements Gathering", 0, 3, True),
        ("ACT-02", "Arch & Specs Blueprint", 3, 4, True),
        ("ACT-03", "Regulatory Compliance", 7, 3, False),
        ("ACT-04", "DB Schema Multi-Tenant", 7, 4, True),
        ("ACT-05", "Cloud VPC & Terraform", 11, 5, False),
        ("ACT-06", "Spring Boot Core Setup", 11, 5, True),
        ("ACT-07", "Docker Containerization", 16, 4, False),
        ("ACT-08", "Authentication & RBAC", 16, 4, True),
        ("ACT-09", "School Registry Profile", 20, 5, True),
        ("ACT-10", "Teacher Allocation Module", 25, 5, True),
        ("ACT-11", "Student Enrollment Bulk", 30, 6, False),
        ("ACT-12", "Attendance Geo-Fencing", 30, 5, False),
        ("ACT-13", "School Inspection Audit", 30, 4, True),
        ("ACT-14", "District Analytics BI", 34, 4, True),
        ("ACT-15", "Document Vault & OCR", 34, 4, True),
        ("ACT-16", "Automated SMS Alerting", 38, 3, True),
        ("ACT-17", "Playwright Integration", 41, 5, True),
        ("ACT-18", "JMeter Load Scalability", 46, 4, False),
        ("ACT-19", "Security OWASP Pentest", 46, 3, True),
        ("ACT-20", "Pilot District UAT", 49, 4, False),
        ("ACT-21", "Production DNS Cutover", 49, 5, True),
    ]

    y_pos = range(len(gantt_data))
    
    for idx, (act_id, name, start, dur, is_crit) in enumerate(gantt_data):
        y = len(gantt_data) - 1 - idx
        color = RED if is_crit else SLATE
        ax.barh(y, dur, left=start, height=0.6, color=color, edgecolor=NAVY, lw=1.2, alpha=0.9)
        # Text label inside/next to bar
        ax.text(start + dur/2, y, f"{dur}d", color=WHITE, fontsize=7.5, fontweight='bold', ha='center', va='center')
        ax.text(-0.5, y, f"{act_id}: {name}", color=NAVY, fontsize=8.0, fontweight='bold' if is_crit else 'normal', ha='right', va='center')

    # Gridlines and weeks
    ax.set_yticks([])
    ax.set_xticks(range(0, 85, 5))
    ax.set_xlim(-12, 80)
    ax.set_ylim(-1, len(gantt_data))

    # Vertical Markers
    ax.axvline(54, color=RED, lw=2.0, ls='--', label='Critical Path Finish (Day 54)')
    ax.axvline(80, color=NAVY, lw=2.0, ls=':', label='Academic Semester Limit (Day 80 / 16 Wks)')
    ax.axvspan(54, 80, color='#EBF8FF', alpha=0.5, label='Scheduled Operational Buffer (26 Days)')

    # Week Secondary Labels at top
    ax.set_xlabel("Working Days (Academic Semester: 16 Weeks / 80 Working Days)", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_title("SHALACONNECT - 16-WEEK SCHEDULE BASELINE GANTT CHART (CRITICAL PATH IN RED)", fontsize=13, fontweight='bold', color=NAVY, pad=15)
    ax.grid(axis='x', color=BORDER_GRAY, ls=':', lw=0.8)
    ax.legend(loc='lower right', frameon=True, facecolor=WHITE, edgecolor=BORDER_GRAY, fontsize=9)

    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/gantt_chart.png", dpi=300)
    plt.close()
    print("Gantt chart diagram generated successfully!")

def draw_resource_allocation():
    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)

    weeks = [f"W{i}" for i in range(1, 17)]
    # Person-days per week for 5 roles
    analyst_arch = [15, 18, 12, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dev_backend  = [0, 5, 15, 20, 22, 22, 18, 15, 12, 8, 4, 0, 0, 0, 0, 0]
    dev_frontend = [0, 0, 0, 5, 12, 18, 20, 20, 16, 12, 5, 0, 0, 0, 0, 0]
    devops_cloud = [0, 0, 5, 12, 15, 10, 5, 4, 4, 8, 15, 18, 10, 5, 2, 0]
    qa_security  = [0, 0, 0, 0, 0, 5, 8, 10, 15, 20, 22, 22, 18, 12, 5, 2]

    ax.bar(weeks, analyst_arch, label="Systems Analyst / Architect", color='#2B6CB0', width=0.6)
    ax.bar(weeks, dev_backend, bottom=analyst_arch, label="Backend Developers (Spring/Postgres)", color='#2C7A7B', width=0.6)
    bottom2 = [i+j for i,j in zip(analyst_arch, dev_backend)]
    ax.bar(weeks, dev_frontend, bottom=bottom2, label="Frontend & Mobile Leads (React/PWA)", color='#C05621', width=0.6)
    bottom3 = [i+j for i,j in zip(bottom2, dev_frontend)]
    ax.bar(weeks, devops_cloud, bottom=bottom3, label="DevOps & Cloud Engineers (AWS/Terraform)", color='#6B46C1', width=0.6)
    bottom4 = [i+j for i,j in zip(bottom3, devops_cloud)]
    ax.bar(weeks, qa_security, bottom=bottom4, label="QA Engineers & Security Auditors", color='#2F855A', width=0.6)

    ax.set_ylabel("Staffing Effort (Person-Days / Week)", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_xlabel("Academic Schedule Timeline (Weeks 1 to 16)", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_title("SHALACONNECT - RESOURCE UTILIZATION & STAFFING HISTOGRAM", fontsize=13, fontweight='bold', color=NAVY, pad=15)
    ax.grid(axis='y', color=BORDER_GRAY, ls=':', lw=0.8)
    ax.legend(loc='upper right', frameon=True, facecolor=WHITE, edgecolor=BORDER_GRAY, fontsize=9)

    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/resource_allocation_chart.png", dpi=300)
    plt.close()
    print("Resource allocation chart generated successfully!")

def draw_budget_breakdown():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5), dpi=300)
    fig.patch.set_facecolor(GRAY_BG)

    # Left: Control Accounts Distribution Donut
    labels_ca = [
        "CA-01: Inception\n(INR 60,000)",
        "CA-02: Foundation\n(INR 1,32,000)",
        "CA-03: Core Modules\n(INR 1,49,000)",
        "CA-04: Testing & QA\n(INR 33,500)",
        "CA-05: Handover\n(INR 35,500)"
    ]
    sizes_ca = [60000, 132000, 149000, 33500, 35500]
    colors_ca = ['#2B6CB0', '#2C7A7B', '#C05621', '#6B46C1', '#2F855A']

    wedges, texts, autotexts = ax1.pie(sizes_ca, labels=labels_ca, colors=colors_ca, autopct='%1.1f%%',
                                       startangle=140, pctdistance=0.75,
                                       wedgeprops=dict(width=0.45, edgecolor=WHITE, lw=2))
    for t in texts: t.set_fontsize(8.5); t.set_color(NAVY); t.set_fontweight('bold')
    for at in autotexts: at.set_fontsize(8.0); at.set_color(WHITE); at.set_fontweight('bold')
    ax1.set_title("Cost Baseline (BAC = INR 4,10,000)\nDistribution by Control Account", fontsize=11, fontweight='bold', color=NAVY)

    # Right: Total Budget Aggregation (Baseline + Contingency + Management)
    components = ["Cost Baseline (BAC)", "Contingency (10%)", "Management (7%)", "Total Budget"]
    amounts = [410000, 41000, 34000, 485000]
    colors_bars = ['#2B6CB0', AMBER, '#805AD5', GREEN]

    bars = ax2.bar(components, amounts, color=colors_bars, width=0.55, edgecolor=NAVY, lw=1.2)
    for b in bars:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 8000, f"INR {h:,.0f}", ha='center', fontsize=9.0, fontweight='bold', color=NAVY)

    ax2.set_ylabel("Amount in INR", fontsize=10, fontweight='bold', color=NAVY)
    ax2.set_title("Total Project Budget Hierarchy\n(Direct + Indirect + Reserves = INR 4,85,000)", fontsize=11, fontweight='bold', color=NAVY)
    ax2.set_ylim(0, 540000)
    ax2.grid(axis='y', color=BORDER_GRAY, ls=':', lw=0.8)

    plt.suptitle("SHALACONNECT - COST BASELINE AGGREGATION & BUDGET COMPOSITION", fontsize=13, fontweight='bold', color=NAVY, y=0.98)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/budget_breakdown_chart.png", dpi=300)
    plt.close()
    print("Budget breakdown chart generated successfully!")

def draw_scurve_chart():
    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)

    weeks = list(range(1, 17))
    # Cumulative Planned Value S-Curve data
    cum_pv = [15000, 39000, 72000, 110000, 162000, 222000, 270000, 312000, 350000, 374000, 386000, 392000, 400000, 407000, 410000, 410000]
    weekly_spend = [15000, 24000, 33000, 38000, 52000, 60000, 48000, 42000, 38000, 24000, 12000, 6000, 8000, 7000, 3000, 0]

    # Plot S-Curve
    ax.plot(weeks, cum_pv, color='#2B6CB0', lw=3.0, marker='o', markersize=6, label='Cumulative Planned Value (S-Curve BAC)')
    ax.fill_between(weeks, cum_pv, color='#EBF8FF', alpha=0.6)

    # Plot Weekly Spend bars on secondary axis
    ax2 = ax.twinx()
    ax2.bar([w - 0.2 for w in weeks], weekly_spend, width=0.4, color='#A0AEC0', alpha=0.45, label='Weekly Time-Phased Cash Flow')
    ax2.set_ylabel("Weekly Cash Flow (INR)", fontsize=10, fontweight='bold', color=TEXT_MUTED)
    ax2.set_ylim(0, 80000)

    # Target Baseline Line
    ax.axhline(410000, color=GREEN, lw=1.5, ls='--', label='Approved Cost Baseline (BAC = INR 4,10,000)')

    ax.set_xlabel("Academic Schedule Timeline (Weeks 1 to 16)", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_ylabel("Cumulative Planned Expenditure (INR)", fontsize=11, fontweight='bold', color=NAVY)
    ax.set_title("SHALACONNECT - TIME-PHASED CUMULATIVE BUDGET S-CURVE BASELINE", fontsize=13, fontweight='bold', color=NAVY, pad=15)
    ax.set_xticks(weeks)
    ax.set_xticklabels([f"W{w}" for w in weeks])
    ax.set_ylim(0, 460000)
    ax.grid(color=BORDER_GRAY, ls=':', lw=0.8)

    # Combine legends
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor=WHITE, edgecolor=BORDER_GRAY, fontsize=9)

    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/scurve_chart.png", dpi=300)
    plt.close()
    print("S-Curve diagram generated successfully!")

if __name__ == "__main__":
    draw_aon_network_diagram()
    draw_critical_path_traversal()
    draw_gantt_chart()
    draw_resource_allocation()
    draw_budget_breakdown()
    draw_scurve_chart()
    print("All Assignment 2 diagrams successfully generated!")
