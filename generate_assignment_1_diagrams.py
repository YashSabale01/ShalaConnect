import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

output_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_1_WBS\Diagrams"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = ['Calibri', 'Arial', 'Segoe UI', 'DejaVu Sans']
plt.rcParams['font.size'] = 10

# -------------------------------------------------------------
# 1. STAKEHOLDER POWER-INTEREST MATRIX (100% PURE ENGLISH)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

# Draw quadrants
ax.axhline(0.5, color='#94a3b8', linestyle='--', linewidth=1.5)
ax.axvline(0.5, color='#94a3b8', linestyle='--', linewidth=1.5)

# Quadrant backgrounds
ax.add_patch(patches.Rectangle((0, 0.5), 0.5, 0.5, facecolor='#fef3c7', alpha=0.4))
ax.add_patch(patches.Rectangle((0.5, 0.5), 0.5, 0.5, facecolor='#fee2e2', alpha=0.4))
ax.add_patch(patches.Rectangle((0, 0), 0.5, 0.5, facecolor='#f1f5f9', alpha=0.4))
ax.add_patch(patches.Rectangle((0.5, 0), 0.5, 0.5, facecolor='#e0f2fe', alpha=0.4))

# Quadrant Strategy Labels
ax.text(0.04, 0.94, "KEEP SATISFIED\n(High Power, Low/Medium Interest)", fontsize=11, fontweight='bold', color='#92400e', va='top')
ax.text(0.54, 0.94, "MANAGE CLOSELY / KEY PLAYERS\n(High Power, High Interest)", fontsize=11, fontweight='bold', color='#991b1b', va='top')
ax.text(0.04, 0.46, "MONITOR / MINIMUM EFFORT\n(Low Power, Low Interest)", fontsize=11, fontweight='bold', color='#475569', va='top')
ax.text(0.54, 0.46, "KEEP INFORMED / REGULAR ENGAGEMENT\n(Low Power, High Interest)", fontsize=11, fontweight='bold', color='#075985', va='top')

# Stakeholder nodes (100% English)
stakeholders = [
    ("Cluster Resource Center Head\n(CRC Administrator / Cluster Lead)", 0.88, 0.85, '#dc2626'),
    ("School Principals & Headmasters\n(Primary & Secondary School Leads)", 0.72, 0.88, '#ea580c'),
    ("Block Education Officer (BEO)\n(Sub-District Regulatory Authority)", 0.82, 0.28, '#d97706'),
    ("Academic Committee & Guide\n(MITAOE Evaluation Panel)", 0.92, 0.65, '#b91c1c'),
    ("Students, Parents & Citizens\n(Public School Community)", 0.22, 0.78, '#0284c7'),
    ("Cloud & Infrastructure Providers\n(AWS & Domain Registrars)", 0.25, 0.18, '#64748b'),
]

for label, pwr, intr, color in stakeholders:
    ax.scatter(intr, pwr, color=color, s=250, zorder=5, edgecolors='#0f172a', linewidth=1.5)
    ax.annotate(
        label, (intr, pwr),
        xytext=(0, 14), textcoords='offset points',
        ha='center', va='bottom',
        fontsize=9, fontweight='bold', color='#0f172a',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor=color, alpha=0.95, linewidth=1.2),
        zorder=6
    )

ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.0)
ax.set_xlabel("STAKEHOLDER INTEREST IN PROJECT OUTCOMES →", fontsize=11, fontweight='bold', labelpad=12, color='#1e293b')
ax.set_ylabel("STAKEHOLDER POWER / AUTHORITY LEVEL →", fontsize=11, fontweight='bold', labelpad=12, color='#1e293b')
ax.set_title("ShalaConnect - Stakeholder Power-Interest Matrix (PMBOK Guide 7th Edition)", fontsize=13, fontweight='bold', pad=16, color='#1e3a8a')

ax.set_xticks([0.25, 0.75])
ax.set_xticklabels(["Low / Medium Interest", "High / Critical Interest"], fontweight='bold', color='#334155')
ax.set_yticks([0.25, 0.75])
ax.set_yticklabels(["Low / Operational Power", "High / Decision-Making Power"], fontweight='bold', color='#334155')

plt.tight_layout()
stakeholder_path = os.path.join(output_dir, "stakeholder_matrix.png")
plt.savefig(stakeholder_path, dpi=300)
plt.close()
print("Saved 100% English stakeholder_matrix.png")

# -------------------------------------------------------------
# 2. HIERARCHICAL WBS DIAGRAM (100% PURE ENGLISH)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
ax.axis('off')

# Root Node (Level 1)
root_box = patches.FancyBboxPatch((4.5, 8.0), 5.0, 0.75, boxstyle="round,pad=0.2", facecolor="#1e3a8a", edgecolor="#0f172a", linewidth=2)
ax.add_patch(root_box)
ax.text(7.0, 8.37, "1.0 ShalaConnect Platform\n(School Cluster Education Governance)", color="white", fontsize=11, fontweight="bold", ha="center", va="center")

# Phases (Level 2)
phases = [
    (1.4, 6.2, "1.1 Initiation &\nRequirements", "#2563eb"),
    (4.2, 6.2, "1.2 System\nArchitecture", "#2563eb"),
    (7.0, 6.2, "1.3 Core Application\nDevelopment", "#2563eb"),
    (9.8, 6.2, "1.4 Cloud DevOps\n& Hardening", "#2563eb"),
    (12.6, 6.2, "1.5 QA, Pilot &\nHandover", "#2563eb")
]

for x, y, title, col in phases:
    box = patches.FancyBboxPatch((x-1.1, y-0.45), 2.2, 0.9, boxstyle="round,pad=0.15", facecolor=col, edgecolor="#1e293b", linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, title, color="white", fontsize=9.5, fontweight="bold", ha="center", va="center")
    ax.plot([7.0, x], [8.0, 6.65], color="#64748b", linewidth=1.8, zorder=1)

# Work Packages (Level 3)
wp_data = {
    1.4: [
        ("1.1.1 Stakeholder Surveys", 5.0),
        ("1.1.2 SRS Specification", 4.1),
        ("1.1.3 DPDP Compliance", 3.2)
    ],
    4.2: [
        ("1.2.1 Data Modeling (PG16)", 5.0),
        ("1.2.2 REST API Spec", 4.1),
        ("1.2.3 Responsive UI/UX", 3.2),
        ("1.2.4 Cloud Blueprint", 2.3)
    ],
    7.0: [
        ("1.3.1 RBAC & Security", 5.2),
        ("1.3.2 Attendance & Sync", 4.5),
        ("1.3.3 BEO Report Engine", 3.8),
        ("1.3.4 Circulars Repository", 3.1),
        ("1.3.5 Meeting Coord.", 2.4),
        ("1.3.6 Events & Photos", 1.7),
        ("1.3.7 Dynamic Forms", 1.0),
        ("1.3.8 Public Portal", 0.3)
    ],
    9.8: [
        ("1.4.1 Terraform IaC", 5.0),
        ("1.4.2 GitHub CI/CD", 4.1),
        ("1.4.3 Security & Tuning", 3.2)
    ],
    12.6: [
        ("1.5.1 Automated Testing", 5.0),
        ("1.5.2 Cluster Pilot UAT", 4.1),
        ("1.5.3 Docs & Submission", 3.2)
    ]
}

for px, items in wp_data.items():
    for label, y in items:
        wp_box = patches.FancyBboxPatch((px-1.15, y-0.28), 2.3, 0.56, boxstyle="round,pad=0.1", facecolor="#f8fafc", edgecolor="#475569", linewidth=1.2)
        ax.add_patch(wp_box)
        ax.text(px, y, label, color="#0f172a", fontsize=8, fontweight="bold", ha="center", va="center")
        ax.plot([px, px], [5.75, y+0.28], color="#94a3b8", linewidth=1.2, zorder=1)

ax.set_xlim(0, 14)
ax.set_ylim(-0.2, 9.2)
ax.set_title("ShalaConnect - Deliverable-Oriented Hierarchical Work Breakdown Structure (100% Rule)", fontsize=13, fontweight='bold', pad=16, color='#1e3a8a')

plt.tight_layout()
wbs_path = os.path.join(output_dir, "wbs_hierarchy.png")
plt.savefig(wbs_path, dpi=300)
plt.close()
print("Saved 100% English wbs_hierarchy.png")

# -------------------------------------------------------------
# 3. PROJECT SCOPE HIERARCHY DIAGRAM (100% PURE ENGLISH)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
ax.axis('off')

# Layer 1: Strategic Need
b1 = patches.FancyBboxPatch((0.5, 6.0), 11.0, 1.0, boxstyle="round,pad=0.15", facecolor="#1e3a8a", edgecolor="#0f172a", linewidth=1.5)
ax.add_patch(b1)
ax.text(6.0, 6.65, "STRATEGIC GOAL & BUSINESS NEED (NEP 2020 & Public School Governance Standards)", color="white", fontsize=10.5, fontweight="bold", ha="center")
ax.text(6.0, 6.25, "Eliminate attendance data lag, paper circular loss, and bureaucratic reporting burden across school clusters", color="#cbd5e1", fontsize=9, ha="center")

# Layer 2: Scope Boundaries
b2 = patches.FancyBboxPatch((0.5, 4.3), 5.3, 1.3, boxstyle="round,pad=0.15", facecolor="#065f46", edgecolor="#047857", linewidth=1.5)
ax.add_patch(b2)
ax.text(3.15, 5.25, "CORE IN-SCOPE CAPABILITIES", color="white", fontsize=10, fontweight="bold", ha="center")
ax.text(3.15, 4.65, "- Multi-tenant Daily Attendance with Offline Sync\n- BEO Monthly Excel Export & Defaulter Tracking\n- Circulars Repository with Read Receipts & Audit Logs\n- Dynamic Form Builder & Photo Gallery System", color="#ecfdf5", fontsize=8.5, ha="center")

b3 = patches.FancyBboxPatch((6.2, 4.3), 5.3, 1.3, boxstyle="round,pad=0.15", facecolor="#991b1b", edgecolor="#b91c1c", linewidth=1.5)
ax.add_patch(b3)
ax.text(8.85, 5.25, "EXPLICIT OUT-OF-SCOPE BOUNDARIES", color="white", fontsize=10, fontweight="bold", ha="center")
ax.text(8.85, 4.65, "- Teacher Payroll & State Treasury Finance Disbursal\n- Student Fee Collection & Commercial Pay Gateways\n- Native Android/iOS Store Apps (Responsive PWA used)\n- Third-Party Carrier SMS Gateway Subscriptions", color="#fef2f2", fontsize=8.5, ha="center")

# Layer 3: Architectural Pillars
pillars = [
    (0.5, 1.5, 2.6, 2.3, "Pillar 1: Data & API\nSpring Boot 21 & PostgreSQL 16\n\n- Multi-Tenant Isolation\n- Hibernate JPA 3.2\n- Apache POI Excel Engine\n- RESTful JWT Bearer Auth", "#1e40af"),
    (3.3, 1.5, 2.6, 2.3, "Pillar 2: Client Experience\nReact 18 & Vite SPA\n\n- Clean English Typography\n- Offline Cache Auto-Sync\n- Recharts Trend Visuals\n- Tailwind CSS Responsive", "#0284c7"),
    (6.1, 1.5, 2.6, 2.3, "Pillar 3: Cloud & Security\nAWS Cloud-Native Suite\n\n- ECS Fargate Serverless\n- RDS Postgres Multi-AZ\n- CloudFront CDN Edge\n- S3 Document Vault", "#0d9488"),
    (8.9, 1.5, 2.6, 2.3, "Pillar 4: Automation\nDevOps & CI/CD Pipeline\n\n- 100% Terraform IaC\n- GitHub Actions CI/CD\n- Zero Manual Deployments\n- Docker Containerization", "#7c3aed")
]

for x, y, w, h, text, col in pillars:
    b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor="#f8fafc", edgecolor=col, linewidth=2)
    ax.add_patch(b)
    bh = patches.FancyBboxPatch((x, y+h-0.75), w, 0.75, boxstyle="round,pad=0.1", facecolor=col, edgecolor=col)
    ax.add_patch(bh)
    lines = text.split("\n\n")
    ax.text(x + w/2, y + h - 0.38, lines[0], color="white", fontsize=9, fontweight="bold", ha="center", va="center")
    ax.text(x + 0.15, y + (h - 0.8)/2, lines[1], color="#1e293b", fontsize=8.2, va="center")

# Layer 4: Foundation
b_found = patches.FancyBboxPatch((0.5, 0.2), 11.0, 0.9, boxstyle="round,pad=0.15", facecolor="#334155", edgecolor="#0f172a", linewidth=1.5)
ax.add_patch(b_found)
ax.text(6.0, 0.75, "PROJECT GOVERNANCE & QUALITY FOUNDATION", color="white", fontsize=9.5, fontweight="bold", ha="center")
ax.text(6.0, 0.45, "PMBOK 7th Edition Standards - IEEE Citation Style - 16-Week Lifecycle - INR 4,85,000 Budget Baseline", color="#cbd5e1", fontsize=8.5, ha="center")

# Connectors
ax.annotate('', xy=(6.0, 5.7), xytext=(6.0, 6.0), arrowprops=dict(facecolor='#475569', arrowstyle="->", lw=2))
ax.annotate('', xy=(6.0, 3.9), xytext=(6.0, 4.3), arrowprops=dict(facecolor='#475569', arrowstyle="->", lw=2))
ax.annotate('', xy=(6.0, 1.2), xytext=(6.0, 1.5), arrowprops=dict(facecolor='#475569', arrowstyle="->", lw=2))

ax.set_xlim(0, 12)
ax.set_ylim(0, 7.5)
ax.set_title("ShalaConnect - Comprehensive Project Scope Hierarchy & Architectural Framework", fontsize=12.5, fontweight='bold', pad=14, color='#1e3a8a')

plt.tight_layout()
scope_path = os.path.join(output_dir, "scope_hierarchy.png")
plt.savefig(scope_path, dpi=300)
plt.close()
print("Saved 100% English scope_hierarchy.png")
