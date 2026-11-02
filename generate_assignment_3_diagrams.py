import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

output_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_3_Kanban_Control\Diagrams"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = ['Calibri', 'Arial', 'Segoe UI', 'DejaVu Sans']
plt.rcParams['font.size'] = 9

# -------------------------------------------------------------
# 1. KANBAN WORKFLOW PROCESS DIAGRAM
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
ax.axis('off')

# Columns definition
cols = [
    (0.6, "1. Backlog", "All Prioritized Scope Items\n(21 WBS Work Packages)", "#64748b", "WIP: ∞"),
    (3.2, "2. To Do", "Ready for Sprint\nDependencies Cleared", "#3b82f6", "WIP Limit: 5"),
    (5.8, "3. In Progress", "Active Engineering\nDevelopment & Coding", "#f59e0b", "WIP Limit: 3"),
    (8.4, "4. Testing / Review", "Code Review, JUnit 5\nTenancy Verification", "#8b5cf6", "WIP Limit: 3"),
    (11.0, "5. Done", "Acceptance Verified\nDeployed to AWS ECS", "#10b981", "WIP: ∞")
]

for x, title, sub, col, wip in cols:
    # Outer column box
    c_box = patches.FancyBboxPatch((x, 1.2), 2.2, 5.0, boxstyle="round,pad=0.1", facecolor="#f8fafc", edgecolor=col, linewidth=1.8)
    ax.add_patch(c_box)
    # Header box
    h_box = patches.FancyBboxPatch((x, 5.4), 2.2, 0.8, boxstyle="round,pad=0.08", facecolor=col, edgecolor=col)
    ax.add_patch(h_box)
    ax.text(x + 1.1, 5.85, title, color="white", fontsize=10, fontweight="bold", ha="center")
    ax.text(x + 1.1, 5.52, wip, color="#fef3c7" if "Limit" in wip else "#e2e8f0", fontsize=8, fontweight="bold", ha="center")
    ax.text(x + 1.1, 5.05, sub, color="#475569", fontsize=7.2, ha="center")

# Sample Cards inside columns
def draw_card(cx, cy, task_id, title, owner, cost, bg="#ffffff", border="#cbd5e1"):
    card = patches.FancyBboxPatch((cx+0.12, cy), 1.96, 0.95, boxstyle="round,pad=0.04", facecolor=bg, edgecolor=border, linewidth=1.0)
    ax.add_patch(card)
    ax.text(cx + 0.22, cy + 0.72, task_id, fontsize=7.5, fontweight="bold", color="#1e3a8a")
    ax.text(cx + 1.95, cy + 0.72, cost, fontsize=7, color="#059669", ha="right")
    ax.text(cx + 0.22, cy + 0.42, title, fontsize=7, color="#1e293b")
    ax.text(cx + 0.22, cy + 0.16, f"Lead: {owner}", fontsize=6.5, color="#64748b")

# Backlog Cards
draw_card(0.6, 3.8, "KB-20", "Field Pilot Rollout", "Project Mgr", "INR 14k")
draw_card(0.6, 2.6, "KB-21", "Academic Handover", "Tech Writer", "INR 12k")
draw_card(0.6, 1.4, "KB-15", "Public Portal UI", "Frontend Dev", "INR 18k")

# To Do Cards
draw_card(3.2, 3.8, "KB-13", "Event Gallery Proof", "Full-Stack", "INR 20k")
draw_card(3.2, 2.6, "KB-12", "Meeting Scheduler", "Full-Stack", "INR 16k")

# In Progress Cards
draw_card(5.8, 3.8, "KB-09", "Daily Attendance Engine", "Full-Stack", "INR 32k", bg="#fef3c7", border="#f59e0b")
draw_card(5.8, 2.6, "KB-16", "Modular Terraform IaC", "DevOps Lead", "INR 28k", bg="#fef3c7", border="#f59e0b")

# Testing / Review Cards
draw_card(8.4, 3.8, "KB-08", "RBAC & JWT Security", "Backend Eng", "INR 22k", bg="#f5f3ff", border="#8b5cf6")
draw_card(8.4, 2.6, "KB-10", "BEO Excel Export Engine", "Backend Dev", "INR 24k", bg="#f5f3ff", border="#8b5cf6")

# Done Cards
draw_card(11.0, 3.8, "KB-01", "Stakeholder Surveys", "Project Mgr", "INR 14k", bg="#ecfdf5", border="#10b981")
draw_card(11.0, 2.6, "KB-02", "SRS & Requirements", "Sys Analyst", "INR 16k", bg="#ecfdf5", border="#10b981")
draw_card(11.0, 1.4, "KB-04", "Data Modeling (PG16)", "DB Architect", "INR 20k", bg="#ecfdf5", border="#10b981")

# Connectors and Metric Annotations
ax.annotate("", xy=(3.15, 3.7), xytext=(2.85, 3.7), arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=2))
ax.annotate("", xy=(5.75, 3.7), xytext=(5.45, 3.7), arrowprops=dict(arrowstyle="->", color="#f59e0b", lw=2))
ax.annotate("", xy=(8.35, 3.7), xytext=(8.05, 3.7), arrowprops=dict(arrowstyle="->", color="#8b5cf6", lw=2))
ax.annotate("", xy=(10.95, 3.7), xytext=(10.65, 3.7), arrowprops=dict(arrowstyle="->", color="#10b981", lw=2))

# Lead Time & Cycle Time brackets
ax.plot([0.6, 13.2], [0.8, 0.8], color="#1e3a8a", lw=1.5)
ax.text(6.9, 0.55, "LEAD TIME (Request Initiated in Backlog → Deployed to Done) [Avg: 11.2 Days]", ha="center", fontsize=8, fontweight="bold", color="#1e3a8a")

ax.plot([5.8, 13.2], [0.25, 0.25], color="#b45309", lw=1.5)
ax.text(9.5, 0.05, "CYCLE TIME (Work Commenced in Progress → Done) [Avg: 4.8 Days | Little's Law: WIP = Throughput x Cycle Time]", ha="center", fontsize=8, fontweight="bold", color="#b45309")

ax.set_xlim(0, 13.8)
ax.set_ylim(-0.2, 6.8)
ax.set_title("ShalaConnect - Interactive Kanban Execution Workflow & Lean Process Flow (WIP Limits & Flow Metrics)", fontsize=12.5, fontweight='bold', pad=14, color='#1e3a8a')

plt.tight_layout()
kanban_path = os.path.join(output_dir, "kanban_workflow_diagram.png")
plt.savefig(kanban_path, dpi=300)
plt.close()
print("Saved kanban_workflow_diagram.png")

# -------------------------------------------------------------
# 2. RACI RESPONSIBILITY ASSIGNMENT MATRIX DIAGRAM
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
ax.axis('off')

roles = ["Project Manager", "Lead Architect", "Backend Dev", "Frontend Dev", "DevOps Eng", "QA Engineer", "CRC Admin", "Headmaster"]
wbs_packages = [
    ("1.1.1 Stakeholder Surveys", ["A", "C", "I", "I", "I", "I", "R", "R"]),
    ("1.1.2 SRS Specification", ["A", "R", "C", "C", "I", "C", "C", "I"]),
    ("1.1.3 DPDP Compliance", ["A", "R", "C", "I", "C", "I", "I", "I"]),
    ("1.2.1 Data Modeling (PG16)", ["I", "A", "R", "I", "C", "I", "I", "I"]),
    ("1.2.2 REST API Specs", ["I", "A", "R", "C", "I", "C", "I", "I"]),
    ("1.2.3 Responsive UI/UX", ["I", "C", "C", "R", "I", "I", "A", "C"]),
    ("1.2.4 Cloud Blueprint", ["I", "A", "C", "I", "R", "I", "I", "I"]),
    ("1.3.1 RBAC & Security", ["I", "A", "R", "C", "C", "C", "I", "I"]),
    ("1.3.2 Attendance Engine", ["A", "C", "R", "R", "I", "C", "C", "C"]),
    ("1.3.3 BEO Excel Report Engine", ["A", "C", "R", "I", "I", "C", "C", "I"]),
    ("1.3.4 Circulars Repository", ["A", "I", "R", "C", "I", "I", "C", "C"]),
    ("1.3.5 Meeting Scheduler", ["A", "I", "R", "C", "I", "I", "C", "C"]),
    ("1.3.6 Events & Photo Gallery", ["A", "I", "R", "C", "I", "I", "C", "C"]),
    ("1.3.7 Dynamic Form Builder", ["A", "C", "R", "C", "I", "C", "C", "C"]),
    ("1.3.8 Public Transparency Portal", ["I", "I", "C", "R", "I", "C", "A", "I"]),
    ("1.4.1 Modular Terraform IaC", ["A", "C", "I", "I", "R", "I", "I", "I"]),
    ("1.4.2 GitHub Actions CI/CD", ["A", "C", "C", "C", "R", "C", "I", "I"]),
    ("1.4.3 Performance & Audit", ["A", "C", "C", "C", "C", "R", "I", "I"]),
    ("1.5.1 Automated Testing", ["A", "I", "C", "C", "I", "R", "I", "I"]),
    ("1.5.2 Field Pilot Rollout", ["A", "I", "C", "C", "I", "C", "R", "R"]),
    ("1.5.3 Academic Handover", ["A", "R", "C", "C", "C", "C", "I", "I"])
]

n_rows = len(wbs_packages)
n_cols = len(roles)

# Draw Table Grid
col_x = [3.2 + i * 1.2 for i in range(n_cols)]
row_y = [7.2 - j * 0.33 for j in range(n_rows)]

# Headers
for i, r_name in enumerate(roles):
    ax.text(col_x[i] + 0.55, 7.55, r_name, fontsize=8, fontweight='bold', color='#1e3a8a', ha='center', rotation=30)

raci_colors = {
    "R": ("#dcfce7", "#15803d"), # Green: Responsible
    "A": ("#fee2e2", "#b91c1c"), # Red: Accountable
    "C": ("#fef3c7", "#b45309"), # Yellow: Consulted
    "I": ("#e0f2fe", "#0369a1")  # Blue: Informed
}

for j, (wp_title, assignments) in enumerate(wbs_packages):
    y = row_y[j]
    ax.text(0.1, y + 0.1, wp_title, fontsize=7.5, color='#1e293b', va='center')
    for i, code in enumerate(assignments):
        x = col_x[i]
        bg, fg = raci_colors[code]
        box = patches.Rectangle((x, y - 0.05), 1.1, 0.3, facecolor=bg, edgecolor='#cbd5e1', lw=0.6)
        ax.add_patch(box)
        ax.text(x + 0.55, y + 0.1, code, fontsize=8, fontweight='bold', color=fg, ha='center', va='center')

# Legend
leg_items = [
    ("R", "Responsible (Does the work)", "#dcfce7", "#15803d"),
    ("A", "Accountable (Sole decision maker - exactly ONE per activity)", "#fee2e2", "#b91c1c"),
    ("C", "Consulted (Two-way input & review)", "#fef3c7", "#b45309"),
    ("I", "Informed (One-way status updates)", "#e0f2fe", "#0369a1")
]
for idx, (sym, dsc, bg, fg) in enumerate(leg_items):
    lx = 0.5 + idx * 3.1
    b = patches.Rectangle((lx, -0.4), 0.4, 0.25, facecolor=bg, edgecolor='#cbd5e1', lw=0.6)
    ax.add_patch(b)
    ax.text(lx + 0.2, -0.27, sym, fontsize=8, fontweight='bold', color=fg, ha='center', va='center')
    ax.text(lx + 0.5, -0.27, dsc, fontsize=6.8, color='#334155', va='center')

ax.set_xlim(0, 13.0)
ax.set_ylim(-0.6, 8.2)
ax.set_title("ShalaConnect - RACI Responsibility Assignment Matrix (Strict Single-Accountability Rule)", fontsize=12.5, fontweight='bold', pad=14, color='#1e3a8a')

plt.tight_layout()
raci_path = os.path.join(output_dir, "raci_matrix_diagram.png")
plt.savefig(raci_path, dpi=300)
plt.close()
print("Saved raci_matrix_diagram.png")

# -------------------------------------------------------------
# 3. EARNED VALUE MANAGEMENT (EVM) S-CURVE DIAGRAM
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

# Simulate 54-day project with snapshot taken at Day 35 (Status Date)
days = np.arange(0, 55)
# Planned Value: Cumulative from Baseline
pv_curve = 410000 * (1 / (1 + np.exp(-0.12 * (days - 25))))
pv_curve = pv_curve - pv_curve[0]
pv_curve = pv_curve * (410000 / pv_curve[-1])

# Earned Value (EV) up to Day 35: Slight schedule lag (SPI = 0.94)
ev_days = np.arange(0, 36)
ev_curve = pv_curve[:36] * 0.94

# Actual Cost (AC) up to Day 35: Cost efficient (CPI = 1.05)
ac_curve = ev_curve * (1 / 1.05)

# Plot PV (Full curve)
ax.plot(days, pv_curve, color="#1e3a8a", lw=2.5, label="Planned Value (PV) Baseline — BAC: INR 4,10,000", zorder=3)
# Plot EV (up to Day 35)
ax.plot(ev_days, ev_curve, color="#059669", lw=2.8, label="Earned Value (EV) — Status at Day 35: INR 2,97,000", zorder=4)
# Plot AC (up to Day 35)
ax.plot(ev_days, ac_curve, color="#dc2626", lw=2.8, linestyle="--", label="Actual Cost (AC) — Status at Day 35: INR 2,82,857", zorder=4)

# Status Date Line (Day 35)
ax.axvline(35, color="#64748b", linestyle=":", lw=1.8, zorder=2)
ax.text(35, 425000, "STATUS DATE\n(Day 35 / Week 7)", color="#0f172a", fontsize=8.5, fontweight="bold", ha="center")

# Annotate Variances at Day 35
pv_35 = pv_curve[35]
ev_35 = ev_curve[35]
ac_35 = ac_curve[35]

# Schedule Variance (SV = EV - PV)
ax.annotate("", xy=(35, ev_35), xytext=(35, pv_35), arrowprops=dict(arrowstyle="<->", color="#b45309", lw=1.8))
ax.text(35.8, (ev_35 + pv_35)/2, f"Schedule Variance (SV)\n= INR {ev_35 - pv_35:,.0f} (Lag)", fontsize=7.5, fontweight="bold", color="#b45309")

# Cost Variance (CV = EV - AC)
ax.annotate("", xy=(34.5, ev_35), xytext=(34.5, ac_35), arrowprops=dict(arrowstyle="<->", color="#059669", lw=1.8))
ax.text(26.5, (ev_35 + ac_35)/2, f"Cost Variance (CV)\n= +INR {ev_35 - ac_35:,.0f} (Savings)", fontsize=7.5, fontweight="bold", color="#059669")

# EAC Forecast Projection from Day 35 to Day 56
eac_days = np.arange(35, 57)
# Using EAC = BAC / CPI = 410,000 / 1.05 = INR 3,90,476
eac_val = 410000 / 1.05
eac_curve = np.linspace(ac_35, eac_val, len(eac_days))
ax.plot(eac_days, eac_curve, color="#dc2626", linestyle=":", lw=2.0, label=f"EAC Forecast Projection (EAC = INR {eac_val:,.0f})", zorder=3)

# Budget At Completion (BAC) Reference line
ax.axhline(410000, color="#b45309", linestyle="--", lw=1.2)

ax.set_xlim(0, 58)
ax.set_ylim(0, 460000)
ax.set_xlabel("PROJECT TIMELINE (WORKING DAYS → DAY 1 TO DAY 54)", fontsize=10, fontweight='bold', labelpad=10, color='#1e293b')
ax.set_ylabel("CUMULATIVE PERFORMANCE VALUE (INR)", fontsize=10, fontweight='bold', labelpad=10, color='#1e293b')
ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('INR {x:,.0f}'))
ax.set_title("ShalaConnect - Earned Value Management (EVM) Performance S-Curve Analysis (PV, EV, AC, CV, SV, EAC)", fontsize=12.5, fontweight='bold', pad=14, color='#1e3a8a')
ax.grid(True, linestyle='--', alpha=0.5, zorder=1)
ax.legend(loc="upper left", framealpha=0.95, fontsize=8.5)

plt.tight_layout()
evm_path = os.path.join(output_dir, "evm_scurve_analysis.png")
plt.savefig(evm_path, dpi=300)
plt.close()
print("Saved evm_scurve_analysis.png")
