import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

os.makedirs("Project_Management_Submissions/Assignment_4_Risk_Management/Diagrams", exist_ok=True)
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

def draw_rbs():
    fig, ax = plt.subplots(figsize=(18, 10), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 9.1), 17.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(9.0, 9.45, "SHALACONNECT - HIERARCHICAL RISK BREAKDOWN STRUCTURE (RBS) TAXONOMY",
            color=WHITE, fontsize=13, fontweight='bold', ha='center', va='center')

    # Level 0 Root
    ax.add_patch(FancyBboxPatch((6.5, 8.0), 5.0, 0.75, boxstyle="round,pad=0.08", fc=SLATE, ec=NAVY, lw=2))
    ax.text(9.0, 8.42, "ShalaConnect Project Risks", color=WHITE, fontsize=11, fontweight='bold', ha='center')
    ax.text(9.0, 8.15, "16 Threats + 4 Opportunities (PMBOK 7th Ed)", color='#FEFCBF', fontsize=8, ha='center')

    # 4 Level-1 Categories
    cats = [
        ("1.0 TECHNICAL RISKS", "Architecture, Security, Data, Mobile", 2.0, '#2B6CB0'),
        ("2.0 EXTERNAL RISKS", "Cloud Cost, SMS Gateway, Govt APIs", 6.6, '#C05621'),
        ("3.0 ORGANIZATIONAL RISKS", "User Adoption, Pilot UAT Sign-Off", 11.2, '#6B46C1'),
        ("4.0 PROJECT MGMT RISKS", "Staffing Leave, Scope Creep, QA Flakes", 15.8, '#2F855A')
    ]

    for title, sub, x, color in cats:
        # Category Box
        ax.add_patch(FancyBboxPatch((x - 1.8, 6.7), 3.6, 0.8, boxstyle="round,pad=0.06", fc=color, ec=NAVY, lw=1.5))
        ax.text(x, 7.15, title, color=WHITE, fontsize=8.5, fontweight='bold', ha='center')
        ax.text(x, 6.85, sub, color='#E2E8F0', fontsize=6.8, ha='center')
        # Connector from Root
        ax.annotate("", xy=(x, 7.5), xytext=(9.0, 8.0), arrowprops=dict(arrowstyle="->", lw=1.5, color=SLATE))

    # Level 2 & Specific Risks Listed Under Each Category
    cat_risks = [
        # Technical
        [("RSK-01: Rural Network Deficit (PWA Sync)", "Pre: 4x4=16 (HIGH) -> Post: 2x2=4 (LOW)"),
         ("RSK-03: UDISE+ Schema Mismatches", "Pre: 4x4=16 (HIGH) -> Post: 2x2=4 (LOW)"),
         ("RSK-06: Tesseract OCR Degradation", "Pre: 3x4=12 (MED)  -> Post: 2x2=4 (LOW)"),
         ("RSK-08: DB Connection Starvation", "Pre: 3x4=12 (MED)  -> Post: 1x2=2 (LOW)"),
         ("RSK-11: Geofencing Location Spoofing", "Pre: 3x3=9 (MED)   -> Post: 1x1=1 (LOW)"),
         ("RSK-13: JVM 21 Heap Spikes / Leaks", "Pre: 2x4=8 (MED)   -> Post: 1x2=2 (LOW)"),
         ("RSK-15: Playwright Integration Flakes", "Pre: 3x2=6 (LOW)   -> Post: 1x1=1 (LOW)"),
         ("OPP-01: GraalVM AOT Native Image", "Opportunity: 50% RAM Savings / Cold Start"),
         ("OPP-03: Student Dropout ML Prediction", "Opportunity: Scikit-learn Risk Alerting")],
        # External
        [("RSK-02: AWS Cloud Cost Overruns", "Pre: 4x3=12 (MED)  -> Post: 2x2=4 (LOW)"),
         ("RSK-09: Regulatory API Spec Changes", "Pre: 3x3=9 (MED)   -> Post: 1x2=2 (LOW)"),
         ("RSK-12: SMS Gateway Delivery Throttle", "Pre: 3x3=9 (MED)   -> Post: 1x2=2 (LOW)"),
         ("RSK-16: School PC Browser Incompatibility", "Pre: 3x3=9 (MED)   -> Post: 1x2=2 (LOW)"),
         ("OPP-02: Adjacent ZP Replication", "Opportunity: Multi-Tenant District Expansion")],
        # Organizational
        [("RSK-04: DPDPA 2023 Compliance Deficit", "Pre: 3x5=15 (HIGH) -> Post: 1x3=3 (LOW)"),
         ("RSK-05: Headmaster Digital Resistance", "Pre: 4x3=12 (MED)  -> Post: 2x2=4 (LOW)"),
         ("RSK-10: Pilot District Sign-off Delay", "Pre: 3x4=12 (MED)  -> Post: 1x2=2 (LOW)"),
         ("OPP-04: State Hackathon Award / Paper", "Opportunity: University Research Publication")],
        # Project Management
        [("RSK-07: Critical Path Developer Leave", "Pre: 3x4=12 (MED)  -> Post: 1x3=3 (LOW)"),
         ("RSK-14: Uncontrolled Scope Creep", "Pre: 3x3=9 (MED)   -> Post: 1x2=2 (LOW)")]
    ]

    for c_idx, r_list in enumerate(cat_risks):
        x = cats[c_idx][2]
        y_start = 6.4
        box_h = 0.52
        spacing = 0.60

        for idx, (rtitle, rdesc) in enumerate(r_list):
            y = y_start - ((idx + 1) * spacing)
            is_opp = "OPP" in rtitle
            is_high = "(HIGH)" in rdesc
            ec_col = GREEN if is_opp else (RED if is_high else BORDER_GRAY)
            bg_col = '#F0FFF4' if is_opp else ('#FFF5F5' if is_high else WHITE)

            ax.add_patch(FancyBboxPatch((x - 1.8, y), 3.6, box_h, boxstyle="round,pad=0.04", fc=bg_col, ec=ec_col, lw=1.2))
            ax.text(x - 1.7, y + box_h * 0.65, rtitle, color=NAVY, fontsize=6.8, fontweight='bold', ha='left')
            ax.text(x - 1.7, y + box_h * 0.22, rdesc, color=RED if is_high else (GREEN if is_opp else TEXT_MUTED), fontsize=6.0, ha='left')
            # Connector
            ax.plot([x, x], [y_start, y + box_h], color=BORDER_GRAY, lw=0.6)

    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10.2)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_4_Risk_Management/Diagrams/risk_breakdown_structure.png", dpi=300)
    plt.close()
    print("Risk Breakdown Structure diagram generated successfully!")

def draw_probability_impact_matrix():
    fig, ax = plt.subplots(figsize=(15, 11), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 10.1), 14.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(7.5, 10.45, "SHALACONNECT - 5x5 PROBABILITY-IMPACT HEATMAP WITH ALL 20 RISKS PLOTTED",
            color=WHITE, fontsize=12, fontweight='bold', ha='center', va='center')

    # Grid Box: 5 rows (P=5 down to P=1), 5 columns (I=1 to I=5)
    # Cell size 2.2 wide x 1.4 high
    grid_x0 = 2.0
    grid_y0 = 1.2
    cw = 2.4
    ch = 1.5

    # Color zones
    def get_color(p, i):
        score = p * i
        if score >= 15: return '#FED7D7', '#E53E3E' # High Red
        if score >= 8: return '#FEEBC8', '#DD6B20'  # Med Amber
        return '#C6F6D5', '#38A169'                 # Low Green

    # Risks Pre-Mitigation Plotted Data: (id, P, I, is_opp)
    risk_plot = [
        ("RSK-01", 4, 4, False),
        ("RSK-02", 4, 3, False),
        ("RSK-03", 4, 4, False),
        ("RSK-04", 3, 5, False),
        ("RSK-05", 4, 3, False),
        ("RSK-06", 3, 4, False),
        ("RSK-07", 3, 4, False),
        ("RSK-08", 3, 4, False),
        ("RSK-09", 3, 3, False),
        ("RSK-10", 3, 4, False),
        ("RSK-11", 3, 3, False),
        ("RSK-12", 3, 3, False),
        ("RSK-13", 2, 4, False),
        ("RSK-14", 3, 3, False),
        ("RSK-15", 3, 2, False),
        ("RSK-16", 3, 3, False),
        ("OPP-01", 4, 4, True),
        ("OPP-02", 3, 5, True),
        ("OPP-03", 3, 4, True),
        ("OPP-04", 4, 4, True),
    ]

    # Draw Cells
    for p in range(1, 6):
        for i in range(1, 6):
            x = grid_x0 + ((i - 1) * cw)
            y = grid_y0 + ((p - 1) * ch)
            bg_c, border_c = get_color(p, i)

            ax.add_patch(FancyBboxPatch((x, y), cw - 0.1, ch - 0.1, boxstyle="round,pad=0.03", fc=bg_c, ec=border_c, lw=1.5))
            score = p * i
            ax.text(x + 0.15, y + ch - 0.30, f"{score}", color=NAVY, fontsize=8, fontweight='bold')
            ax.text(x + cw - 0.25, y + ch - 0.30, f"P{p}xI{i}", color=TEXT_MUTED, fontsize=6.5, ha='right')

            # Find matching risks in this cell
            in_cell = [r for r in risk_plot if r[1] == p and r[2] == i]
            # Print badges
            for b_idx, (rid, _, _, is_opp) in enumerate(in_cell):
                bx = x + 0.2 + ((b_idx % 2) * 1.1)
                by = y + ch - 0.65 - ((b_idx // 2) * 0.36)
                badge_bg = '#805AD5' if is_opp else (RED if score >= 15 else (AMBER if score >= 8 else GREEN))
                ax.add_patch(FancyBboxPatch((bx, by), 0.95, 0.28, boxstyle="round,pad=0.02", fc=badge_bg, ec=badge_bg))
                ax.text(bx + 0.475, by + 0.07, rid, color=WHITE, fontsize=6.5, fontweight='bold', ha='center')

    # Y Axis (Probability)
    p_labels = ["1 - Very Low (<10%)", "2 - Low (10-30%)", "3 - Medium (30-50%)", "4 - High (50-70%)", "5 - Very High (>70%)"]
    for idx, pl in enumerate(p_labels):
        y = grid_y0 + (idx * ch) + (ch / 2)
        ax.text(grid_x0 - 0.2, y, pl, color=NAVY, fontsize=7.5, fontweight='bold', ha='right', va='center')

    # X Axis (Impact)
    i_labels = ["1 - Negligible", "2 - Minor", "3 - Moderate", "4 - Significant", "5 - Catastrophic"]
    for idx, il in enumerate(i_labels):
        x = grid_x0 + (idx * cw) + (cw / 2)
        ax.text(x, grid_y0 - 0.35, il, color=NAVY, fontsize=7.5, fontweight='bold', ha='center', va='top')

    ax.text(grid_x0 + (cw * 2.5), grid_y0 - 0.75, "IMPACT SEVERITY RATING →", color=NAVY, fontsize=10, fontweight='bold', ha='center')
    ax.text(grid_x0 - 1.8, grid_y0 + (ch * 2.5), "PROBABILITY RATING →", color=NAVY, fontsize=10, fontweight='bold', va='center', rotation=90)

    # Legend at Bottom
    ax.add_patch(FancyBboxPatch((2.0, 8.9), 11.9, 0.75, boxstyle="round,pad=0.06", fc=WHITE, ec=BORDER_GRAY))
    ax.text(2.2, 9.35, "SEVERITY TIERS:", color=NAVY, fontsize=8, fontweight='bold')
    ax.add_patch(Rectangle((3.6, 9.25), 0.3, 0.25, fc='#FED7D7', ec=RED))
    ax.text(4.0, 9.35, "High (15-25): Immediate Mitigation", color=RED, fontsize=7.5, fontweight='bold', va='center')
    ax.add_patch(Rectangle((7.5, 9.25), 0.3, 0.25, fc='#FEEBC8', ec=AMBER))
    ax.text(7.9, 9.35, "Medium (8-14): Active Controls", color=AMBER, fontsize=7.5, fontweight='bold', va='center')
    ax.add_patch(Rectangle((11.0, 9.25), 0.3, 0.25, fc='#C6F6D5', ec=GREEN))
    ax.text(11.4, 9.35, "Low (1-7): Routine Monitoring", color=GREEN, fontsize=7.5, fontweight='bold', va='center')

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 11)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_4_Risk_Management/Diagrams/probability_impact_matrix.png", dpi=300)
    plt.close()
    print("Probability-Impact matrix diagram generated successfully!")

def draw_risk_response_workflow():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 7.6), 14.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(7.5, 7.95, "SHALACONNECT - 5-STAGE RISK MANAGEMENT LIFECYCLE WORKFLOW",
            color=WHITE, fontsize=12, fontweight='bold', ha='center', va='center')

    stages = [
        ("1. IDENTIFY", "Technical checklists\nStakeholder interviews\nUDISE+ audit logs", 1.8, 5.2, '#2B6CB0'),
        ("2. ANALYZE", "5x5 Qualitative scoring\nExpected monetary value\nRoot-cause evaluation", 5.2, 5.2, '#2C7A7B'),
        ("3. PLAN RESPONSE", "Threat: Mitigate, Avoid\nOpp: Exploit, Enhance\nContingency reserves", 8.6, 5.2, AMBER),
        ("4. EXECUTE", "Engineering playbooks\nOffline PWA & AES-256\nHeadmaster workshops", 12.0, 5.2, GREEN),
        ("5. RESIDUAL AUDIT", "Re-score residual PxI\nReserve drawdown log\nPost-mortem updates", 6.9, 2.2, '#6B46C1')
    ]

    for title, desc, x, y, col in stages:
        ax.add_patch(FancyBboxPatch((x - 1.4, y - 0.7), 2.8, 1.4, boxstyle="round,pad=0.08", fc=WHITE, ec=col, lw=2))
        ax.add_patch(FancyBboxPatch((x - 1.4, y + 0.35), 2.8, 0.35, boxstyle="round,pad=0.03", fc=col, ec=col))
        ax.text(x, y + 0.52, title, color=WHITE, fontsize=8.0, fontweight='bold', ha='center')
        ax.text(x, y - 0.15, desc, color=TEXT_DARK, fontsize=7.2, ha='center', va='center')

    # Arrows 1 -> 2 -> 3 -> 4
    ax.annotate("", xy=(3.6, 5.2), xytext=(3.2, 5.2), arrowprops=dict(arrowstyle="->", lw=2, color=SLATE))
    ax.annotate("", xy=(7.0, 5.2), xytext=(6.6, 5.2), arrowprops=dict(arrowstyle="->", lw=2, color=SLATE))
    ax.annotate("", xy=(10.4, 5.2), xytext=(10.0, 5.2), arrowprops=dict(arrowstyle="->", lw=2, color=SLATE))

    # Feedback loop 4 down to 5 and back to 1
    ax.annotate("Action Complete", xy=(12.0, 3.2), xytext=(12.0, 4.5),
                arrowprops=dict(arrowstyle="->", lw=2, color=GREEN), color=GREEN, fontsize=7.2, fontweight='bold')
    ax.plot([12.0, 8.3], [3.2, 3.2], color=GREEN, lw=2)
    ax.annotate("", xy=(8.3, 2.4), xytext=(8.3, 3.2), arrowprops=dict(arrowstyle="->", lw=2, color=GREEN))

    ax.annotate("Continuous Review Cycle", xy=(1.8, 4.5), xytext=(5.5, 2.2),
                arrowprops=dict(arrowstyle="->", lw=2, color=SLATE, ls='--'), color=SLATE, fontsize=7.5, fontweight='bold')

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_4_Risk_Management/Diagrams/risk_response_workflow.png", dpi=300)
    plt.close()
    print("Risk response workflow diagram generated successfully!")

def draw_risk_monitoring_escalation():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)
    ax.axis('off')

    # Title
    ax.add_patch(FancyBboxPatch((0.5, 7.6), 14.0, 0.7, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY))
    ax.text(7.5, 7.95, "SHALACONNECT - RISK MONITORING, TRIGGER DETECTION & ESCALATION LADDER",
            color=WHITE, fontsize=12, fontweight='bold', ha='center', va='center')

    # Escalation Steps
    levels = [
        ("Level 1: Operational Trigger", "Telemetry log / Developer alert\nTrigger condition detected", 1.8, 4.8, '#2B6CB0'),
        ("Level 2: Risk Owner Playbook", "Risk Owner activates response\nDeploy offline sync / cache fix", 5.4, 4.8, '#2C7A7B'),
        ("Level 3: PM Contingency Fund", "Drawdown from INR 41,000 reserve\nPM spending authority", 9.0, 4.8, AMBER),
        ("Level 4: Sponsor / CCB Escalation", "Management reserve needed (>10%)?\nFormal CCB review required", 12.6, 4.8, RED)
    ]

    for title, desc, x, y, col in levels:
        ax.add_patch(FancyBboxPatch((x - 1.6, y - 0.7), 3.2, 1.4, boxstyle="round,pad=0.08", fc=WHITE, ec=col, lw=2))
        ax.add_patch(FancyBboxPatch((x - 1.6, y + 0.35), 3.2, 0.35, boxstyle="round,pad=0.03", fc=col, ec=col))
        ax.text(x, y + 0.52, title, color=WHITE, fontsize=7.8, fontweight='bold', ha='center')
        ax.text(x, y - 0.15, desc, color=TEXT_DARK, fontsize=7.2, ha='center', va='center')

    # Escalation Arrows
    ax.annotate("", xy=(3.6, 4.8), xytext=(3.4, 4.8), arrowprops=dict(arrowstyle="->", lw=2, color=SLATE))
    ax.annotate("Exceeds Playbook", xy=(7.2, 4.8), xytext=(7.0, 4.8), arrowprops=dict(arrowstyle="->", lw=2, color=AMBER), color=AMBER, fontsize=7.0, fontweight='bold', ha='center', va='bottom')
    ax.annotate("Scope / Reserve > 10%", xy=(10.8, 4.8), xytext=(10.6, 4.8), arrowprops=dict(arrowstyle="->", lw=2, color=RED), color=RED, fontsize=7.0, fontweight='bold', ha='center', va='bottom')

    # Governance Thresholds Callout Box below
    ax.add_patch(FancyBboxPatch((0.8, 1.0), 13.4, 2.0, boxstyle="round,pad=0.08", fc=LIGHT_BLUE, ec='#90CDF4', lw=1.5))
    ax.text(7.5, 2.65, "GOVERNANCE THRESHOLDS & AUTHORITY PROTOCOLS", color=NAVY, fontsize=9.5, fontweight='bold', ha='center')
    ax.text(1.2, 2.1, "• Trigger Condition Detection: Automated CloudWatch alarms (>80% CPU/RAM) or daily standup blocker flag.", color=TEXT_DARK, fontsize=7.8)
    ax.text(1.2, 1.7, "• Contingency Reserve Drawdown: Project Manager can allocate up to INR 41,000 for verified Risk Register items without delay.", color=TEXT_DARK, fontsize=7.8)
    ax.text(1.2, 1.3, "• Management Reserve Access: Requires written justification, CCB review, and MITAOE Sponsor formal approval.", color=TEXT_DARK, fontsize=7.8)

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_4_Risk_Management/Diagrams/risk_monitoring_escalation.png", dpi=300)
    plt.close()
    print("Risk monitoring & escalation diagram generated successfully!")

def draw_risk_exposure_reduction():
    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
    ax.set_facecolor(GRAY_BG)
    fig.patch.set_facecolor(GRAY_BG)

    top_risks = ["RSK-01 (PWA)", "RSK-02 (AWS)", "RSK-03 (UDISE+)", "RSK-04 (DPDPA)", "RSK-05 (Adoption)", "RSK-06 (OCR)", "RSK-07 (Leave)", "RSK-08 (DB Pool)", "RSK-10 (UAT)"]
    pre_scores = [16, 12, 16, 15, 12, 12, 12, 12, 12]
    post_scores = [4, 4, 4, 3, 4, 4, 3, 2, 2]

    x = range(len(top_risks))
    width = 0.35

    rects1 = ax.bar([i - width/2 for i in x], pre_scores, width, label='Pre-Mitigation Risk Score (PxI)', color=RED, alpha=0.9, edgecolor=NAVY)
    rects2 = ax.bar([i + width/2 for i in x], post_scores, width, label='Post-Mitigation Residual Score (PxI)', color=GREEN, alpha=0.9, edgecolor=NAVY)

    # Threshold lines
    ax.axhline(15, color=RED, lw=1.5, ls='--', label='High Severity Threshold (Score >= 15)')
    ax.axhline(8, color=AMBER, lw=1.2, ls=':', label='Medium Severity Threshold (Score >= 8)')

    # Labels on bars
    for r in rects1:
        h = r.get_height()
        ax.text(r.get_x() + r.get_width()/2, h + 0.3, str(h), ha='center', fontsize=8.0, fontweight='bold', color=RED)
    for r in rects2:
        h = r.get_height()
        ax.text(r.get_x() + r.get_width()/2, h + 0.3, str(h), ha='center', fontsize=8.0, fontweight='bold', color=GREEN)

    ax.set_ylabel("Risk Score (Probability x Impact, Scale 1 to 25)", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_title("SHALACONNECT - PRE- VS. POST-MITIGATION RISK SCORE REDUCTION (TOP THREATS)", fontsize=13, fontweight='bold', color=NAVY, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(top_risks, rotation=15, ha='right', fontsize=8.5, fontweight='bold', color=NAVY)
    ax.set_ylim(0, 20)
    ax.grid(axis='y', color=BORDER_GRAY, ls=':', lw=0.8)
    ax.legend(loc='upper right', frameon=True, facecolor=WHITE, edgecolor=BORDER_GRAY, fontsize=9)

    plt.tight_layout()
    plt.savefig("Project_Management_Submissions/Assignment_4_Risk_Management/Diagrams/risk_response_dashboard.png", dpi=300)
    plt.close()
    print("Risk exposure reduction dashboard generated successfully!")

if __name__ == "__main__":
    draw_rbs()
    draw_probability_impact_matrix()
    draw_risk_response_workflow()
    draw_risk_monitoring_escalation()
    draw_risk_exposure_reduction()
    print("All Assignment 4 diagrams successfully generated!")
