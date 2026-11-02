import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

output_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_2_Project_Plan\Diagrams"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = ['Segoe UI', 'DejaVu Sans', 'sans-serif']
plt.rcParams['font.size'] = 9

# Activities data from cpm_engine
activities = {
    "ACT-01": {"name": "Stakeholder Surveys", "wbs": "1.1.1", "dur": 3, "cost": 14000, "preds": [], "es": 0, "ef": 3, "ls": 0, "lf": 3, "tf": 0, "crit": True},
    "ACT-02": {"name": "SRS & Req Matrix", "wbs": "1.1.2", "dur": 4, "cost": 16000, "preds": ["ACT-01"], "es": 3, "ef": 7, "ls": 3, "lf": 7, "tf": 0, "crit": True},
    "ACT-03": {"name": "DPDP Compliance", "wbs": "1.1.3", "dur": 3, "cost": 12000, "preds": ["ACT-02"], "es": 7, "ef": 10, "ls": 7, "lf": 10, "tf": 0, "crit": True},
    "ACT-04": {"name": "Multi-Tenant Data Model", "wbs": "1.2.1", "dur": 4, "cost": 20000, "preds": ["ACT-02", "ACT-03"], "es": 10, "ef": 14, "ls": 10, "lf": 14, "tf": 0, "crit": True},
    "ACT-05": {"name": "REST API Specs", "wbs": "1.2.2", "dur": 4, "cost": 18000, "preds": ["ACT-04"], "es": 14, "ef": 18, "ls": 14, "lf": 18, "tf": 0, "crit": True},
    "ACT-06": {"name": "Bilingual UI/UX", "wbs": "1.2.3", "dur": 5, "cost": 22000, "preds": ["ACT-02"], "es": 7, "ef": 12, "ls": 18, "lf": 23, "tf": 11, "crit": False},
    "ACT-07": {"name": "AWS Cloud Blueprint", "wbs": "1.2.4", "dur": 4, "cost": 18000, "preds": ["ACT-04", "ACT-05"], "es": 18, "ef": 22, "ls": 28, "lf": 32, "tf": 10, "crit": False},
    "ACT-08": {"name": "RBAC & JWT Security", "wbs": "1.3.1", "dur": 5, "cost": 22000, "preds": ["ACT-05"], "es": 18, "ef": 23, "ls": 18, "lf": 23, "tf": 0, "crit": True},
    "ACT-09": {"name": "Attendance Engine", "wbs": "1.3.2", "dur": 7, "cost": 32000, "preds": ["ACT-06", "ACT-08"], "es": 23, "ef": 30, "ls": 23, "lf": 30, "tf": 0, "crit": True},
    "ACT-10": {"name": "BEO Monthly Export", "wbs": "1.3.3", "dur": 5, "cost": 24000, "preds": ["ACT-09"], "es": 30, "ef": 35, "ls": 30, "lf": 35, "tf": 0, "crit": True},
    "ACT-11": {"name": "GR Circular Repo", "wbs": "1.3.4", "dur": 4, "cost": 18000, "preds": ["ACT-08"], "es": 23, "ef": 27, "ls": 40, "lf": 44, "tf": 17, "crit": False},
    "ACT-12": {"name": "Meeting Scheduler", "wbs": "1.3.5", "dur": 3, "cost": 16000, "preds": ["ACT-08"], "es": 23, "ef": 26, "ls": 41, "lf": 44, "tf": 18, "crit": False},
    "ACT-13": {"name": "Events & Galleries", "wbs": "1.3.6", "dur": 4, "cost": 20000, "preds": ["ACT-06", "ACT-08"], "es": 23, "ef": 27, "ls": 40, "lf": 44, "tf": 17, "crit": False},
    "ACT-14": {"name": "Dynamic Form Engine", "wbs": "1.3.7", "dur": 6, "cost": 26000, "preds": ["ACT-08", "ACT-10"], "es": 35, "ef": 41, "ls": 35, "lf": 41, "tf": 0, "crit": True},
    "ACT-15": {"name": "Public Portal", "wbs": "1.3.8", "dur": 4, "cost": 18000, "preds": ["ACT-05", "ACT-06"], "es": 18, "ef": 22, "ls": 40, "lf": 44, "tf": 22, "crit": False},
    "ACT-16": {"name": "Terraform AWS IaC", "wbs": "1.4.1", "dur": 5, "cost": 28000, "preds": ["ACT-07"], "es": 22, "ef": 27, "ls": 32, "lf": 37, "tf": 10, "crit": False},
    "ACT-17": {"name": "GitHub CI/CD Pipeline", "wbs": "1.4.2", "dur": 4, "cost": 22000, "preds": ["ACT-16"], "es": 27, "ef": 31, "ls": 37, "lf": 41, "tf": 10, "crit": False},
    "ACT-18": {"name": "Performance & Audit", "wbs": "1.4.3", "dur": 3, "cost": 18000, "preds": ["ACT-09", "ACT-10", "ACT-14", "ACT-17"], "es": 41, "ef": 44, "ls": 41, "lf": 44, "tf": 0, "crit": True},
    "ACT-19": {"name": "Automated Testing", "wbs": "1.5.1", "dur": 4, "cost": 20000, "preds": ["ACT-11", "ACT-12", "ACT-13", "ACT-15", "ACT-18"], "es": 44, "ef": 48, "ls": 44, "lf": 48, "tf": 0, "crit": True},
    "ACT-20": {"name": "Field Pilot & UAT", "wbs": "1.5.2", "dur": 3, "cost": 14000, "preds": ["ACT-19"], "es": 48, "ef": 51, "ls": 48, "lf": 51, "tf": 0, "crit": True},
    "ACT-21": {"name": "Docs & Handover", "wbs": "1.5.3", "dur": 3, "cost": 12000, "preds": ["ACT-20"], "es": 51, "ef": 54, "ls": 51, "lf": 54, "tf": 0, "crit": True}
}

# -------------------------------------------------------------
# 1. ACTIVITY-ON-NODE (AON) NETWORK DIAGRAM
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
ax.axis('off')

# Position nodes logically in topological tiers
node_positions = {
    "START": (0.5, 4.5),
    "ACT-01": (1.8, 4.5),
    "ACT-02": (3.2, 4.5),
    "ACT-03": (4.6, 5.8),
    "ACT-06": (4.6, 3.2),
    "ACT-04": (6.0, 5.8),
    "ACT-05": (7.4, 5.8),
    "ACT-07": (8.8, 7.2),
    "ACT-08": (8.8, 5.0),
    "ACT-15": (8.8, 3.2),
    "ACT-16": (10.2, 7.2),
    "ACT-09": (10.2, 5.0),
    "ACT-11": (10.2, 3.6),
    "ACT-12": (10.2, 2.4),
    "ACT-13": (10.2, 1.2),
    "ACT-17": (11.6, 7.2),
    "ACT-10": (11.6, 5.0),
    "ACT-14": (13.0, 5.0),
    "ACT-18": (14.4, 5.8),
    "ACT-19": (15.8, 4.5),
    "ACT-20": (17.2, 4.5),
    "ACT-21": (18.6, 4.5),
    "FINISH": (19.8, 4.5)
}

# Draw START and FINISH nodes
def draw_terminal_node(x, y, text):
    box = patches.FancyBboxPatch((x-0.45, y-0.35), 0.9, 0.7, boxstyle="circle,pad=0.1", facecolor="#334155", edgecolor="#0f172a", linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, text, color="white", fontsize=8.5, fontweight="bold", ha="center", va="center")

draw_terminal_node(*node_positions["START"], "START\nDay 0")
draw_terminal_node(*node_positions["FINISH"], "FINISH\nDay 54")

# Draw Activity Nodes: 6-celled box [ES | Dur | EF] / [Act Name / ID] / [LS | TF | LF]
for act_id, pos in node_positions.items():
    if act_id in ["START", "FINISH"]:
        continue
    x, y = pos
    data = activities[act_id]
    is_crit = data["crit"]
    bg_color = "#fee2e2" if is_crit else "#f1f5f9"
    border_color = "#dc2626" if is_crit else "#475569"
    border_width = 1.8 if is_crit else 1.0

    # Main box
    box = patches.FancyBboxPatch((x-0.62, y-0.48), 1.24, 0.96, boxstyle="round,pad=0.04", facecolor=bg_color, edgecolor=border_color, linewidth=border_width)
    ax.add_patch(box)

    # Content
    # Top row: ES | Dur | EF
    ax.text(x-0.4, y+0.28, f"{data['es']}", fontsize=7, color="#1e293b", ha="center")
    ax.text(x, y+0.28, f"d={data['dur']}", fontsize=7, fontweight="bold", color="#1e3a8a", ha="center")
    ax.text(x+0.4, y+0.28, f"{data['ef']}", fontsize=7, color="#1e293b", ha="center")
    ax.plot([x-0.58, x+0.58], [y+0.18, y+0.18], color="#94a3b8", lw=0.6)

    # Middle row: ID & Name
    ax.text(x, y+0.02, act_id, fontsize=7.5, fontweight="bold", color="#dc2626" if is_crit else "#0f172a", ha="center")
    ax.text(x, y-0.16, data['name'][:14], fontsize=6.2, color="#334155", ha="center")
    ax.plot([x-0.58, x+0.58], [y-0.24, y-0.24], color="#94a3b8", lw=0.6)

    # Bottom row: LS | TF | LF
    ax.text(x-0.4, y-0.38, f"{data['ls']}", fontsize=7, color="#64748b", ha="center")
    ax.text(x, y-0.38, f"TF={data['tf']}", fontsize=6.5, fontweight="bold", color="#dc2626" if is_crit else "#64748b", ha="center")
    ax.text(x+0.4, y-0.38, f"{data['lf']}", fontsize=7, color="#64748b", ha="center")

# Connect with arrows
edges = []
# Start edge
edges.append(("START", "ACT-01", True))
# Activity edges
for act_id, data in activities.items():
    for pred in data["preds"]:
        is_crit_edge = activities[pred]["crit"] and data["crit"] and (data["es"] == activities[pred]["ef"])
        edges.append((pred, act_id, is_crit_edge))
# Finish edge
edges.append(("ACT-21", "FINISH", True))

for u, v, crit in edges:
    ux, uy = node_positions[u]
    vx, vy = node_positions[v]
    dx = vx - ux
    dy = vy - uy
    # Shorten ends
    color = "#dc2626" if crit else "#94a3b8"
    lw = 2.0 if crit else 0.9
    zord = 4 if crit else 2
    ax.annotate(
        "", xy=(vx-0.62 if v not in ["START","FINISH"] else vx-0.45, vy),
        xytext=(ux+0.62 if u not in ["START","FINISH"] else ux+0.45, uy),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=10),
        zorder=zord
    )

ax.set_xlim(-0.2, 20.8)
ax.set_ylim(0.2, 8.5)
ax.set_title("ShalaConnect — Activity-on-Node (AON) Network Diagram with Critical Path (54 Working Days)", fontsize=13, fontweight='bold', pad=12, color='#1e3a8a')

# Legend
leg_box = patches.FancyBboxPatch((0.5, 0.4), 8.5, 0.7, boxstyle="round,pad=0.08", facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1.0)
ax.add_patch(leg_box)
ax.plot([0.8, 1.4], [0.75, 0.75], color="#dc2626", lw=2.2)
ax.text(1.5, 0.75, "Critical Path (TF = 0) [13 Activities, 54 Days]", fontsize=8, fontweight="bold", color="#dc2626", va="center")
ax.plot([4.8, 5.4], [0.75, 0.75], color="#94a3b8", lw=1.0)
ax.text(5.5, 0.75, "Non-Critical Path (Float > 0)", fontsize=8, color="#475569", va="center")

plt.tight_layout()
aon_path = os.path.join(output_dir, "aon_network_diagram.png")
plt.savefig(aon_path, dpi=300)
plt.close()
print("Saved aon_network_diagram.png")

# -------------------------------------------------------------
# 2. GANTT CHART
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 9), dpi=300)

act_keys = sorted(activities.keys(), reverse=True)
y_pos = np.arange(len(act_keys))

for idx, act_id in enumerate(act_keys):
    d = activities[act_id]
    is_crit = d["crit"]
    bar_color = "#ef4444" if is_crit else "#3b82f6"
    # Main bar
    ax.barh(idx, d["dur"], left=d["es"], height=0.55, align='center', color=bar_color, edgecolor="#0f172a", linewidth=0.8, zorder=3)
    # Float bar if any
    if d["tf"] > 0:
        ax.barh(idx, d["tf"], left=d["ef"], height=0.35, align='center', color="#cbd5e1", edgecolor="#94a3b8", linestyle="--", linewidth=0.8, hatch="//", zorder=2)
    # Text annotation
    tf_str = " (Critical)" if is_crit else f" (Float={d['tf']}d)"
    ax.text(d["ef"] + (d["tf"] if d["tf"]>0 else 0) + 0.5, idx, f"{d['dur']}d{tf_str}", va='center', fontsize=7.5, color="#334155", fontweight='bold' if is_crit else 'normal')

# Milestone lines
milestones = [
    (10, "M1: Req Approval (Day 10)", "#059669"),
    (22, "M2: Arch Freeze (Day 22)", "#0284c7"),
    (41, "M3: Core Dev (Day 41)", "#d97706"),
    (44, "M4: Cloud & Audit (Day 44)", "#7c3aed"),
    (54, "M5/M6: UAT & Handover (Day 54)", "#dc2626")
]
for x_m, m_label, m_col in milestones:
    ax.axvline(x_m, color=m_col, linestyle=":", linewidth=1.5, zorder=1)
    ax.text(x_m, len(act_keys)-0.2, m_label, color=m_col, fontsize=7.5, fontweight="bold", rotation=90, va="bottom", ha="right")

ax.set_yticks(y_pos)
ax.set_yticklabels([f"{k}: {activities[k]['name']} (WBS {activities[k]['wbs']})" for k in act_keys], fontsize=8.2)
ax.set_xlabel("PROJECT TIMELINE (WORKING DAYS → DAY 1 TO DAY 54)", fontsize=10, fontweight='bold', labelpad=10, color='#1e293b')
ax.set_xlim(-1, 62)
ax.set_title("ShalaConnect — Comprehensive Project Schedule Gantt Chart with Critical Activities & Float", fontsize=12.5, fontweight='bold', pad=14, color='#1e3a8a')
ax.grid(axis='x', linestyle='--', alpha=0.6, zorder=0)

# Custom legend
leg_crit = patches.Patch(color='#ef4444', label='Critical Activity (Zero Float)')
leg_non_crit = patches.Patch(color='#3b82f6', label='Non-Critical Activity (Has Float)')
leg_float = patches.Patch(facecolor='#cbd5e1', hatch='//', edgecolor='#94a3b8', label='Total Float Window')
ax.legend(handles=[leg_crit, leg_non_crit, leg_float], loc='lower right', framealpha=0.95, fontsize=8.5)

plt.tight_layout()
gantt_path = os.path.join(output_dir, "gantt_chart.png")
plt.savefig(gantt_path, dpi=300)
plt.close()
print("Saved gantt_chart.png")

# -------------------------------------------------------------
# 3. TIME-PHASED CUMULATIVE COST S-CURVE
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

# Calculate daily Planned Value (PV)
# Assume linear spend per working day for each activity
daily_pv = np.zeros(55) # index 0 to 54
for act_id, d in activities.items():
    daily_rate = d["cost"] / d["dur"]
    start_d = d["es"] + 1
    end_d = d["ef"]
    for day in range(start_d, end_d + 1):
        daily_pv[day] += daily_rate

cumulative_pv = np.cumsum(daily_pv)
days = np.arange(0, 55)

# Plot S-curve
ax.plot(days, cumulative_pv, color="#1e3a8a", linewidth=2.8, label="Planned Value (PV) — Cumulative Baseline Spend", zorder=4)
ax.fill_between(days, cumulative_pv, color="#dbeafe", alpha=0.5, zorder=2)

# Horizontal Baselines
ax.axhline(410000, color="#b45309", linestyle="--", linewidth=1.5, label="Cost Baseline (Aggregated WP Subtotal: ₹4,10,000)", zorder=3)
ax.axhline(451000, color="#d97706", linestyle=":", linewidth=1.2, label="+ Contingency Reserve (10%: ₹41,000 → ₹4,51,000)", zorder=3)
ax.axhline(485000, color="#dc2626", linestyle="-.", linewidth=1.5, label="Total Project Budget (+ Management Reserve ₹34,000 → ₹4,85,000)", zorder=3)

# Annotate Milestones on S-Curve
ms_points = [
    (10, cumulative_pv[10], "M1: Req Approval\n₹42,000"),
    (22, cumulative_pv[22], "M2: Design Freeze\n₹1,20,000"),
    (41, cumulative_pv[41], "M3: Core Dev Finish\n₹3,16,000"),
    (44, cumulative_pv[44], "M4: Cloud & Audit\n₹3,64,000"),
    (54, cumulative_pv[54], "M5: UAT & Baseline Handover\n₹4,10,000")
]
for x_pt, y_pt, label in ms_points:
    ax.scatter(x_pt, y_pt, color="#dc2626", s=60, zorder=5)
    ax.annotate(
        label, (x_pt, y_pt),
        xytext=(0, 14), textcoords='offset points',
        ha='center', fontsize=7.5, fontweight='bold', color='#0f172a',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#dc2626', alpha=0.9, lw=0.8),
        arrowprops=dict(arrowstyle="->", color='#dc2626', lw=0.8)
    )

ax.set_xlim(0, 56)
ax.set_ylim(0, 530000)
ax.set_xlabel("PROJECT TIMELINE (WORKING DAYS → DAY 1 TO DAY 54)", fontsize=10, fontweight='bold', labelpad=10, color='#1e293b')
ax.set_ylabel("CUMULATIVE PLANNED EXPENDITURE (INR ₹)", fontsize=10, fontweight='bold', labelpad=10, color='#1e293b')
ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('₹{x:,.0f}'))
ax.set_title("ShalaConnect — Cumulative Cost S-Curve & Time-Phased Budget Baseline (PMBOK 7th Ed.)", fontsize=12.5, fontweight='bold', pad=14, color='#1e3a8a')
ax.grid(True, linestyle='--', alpha=0.5, zorder=1)
ax.legend(loc="upper left", framealpha=0.95, fontsize=8.5)

plt.tight_layout()
scurve_path = os.path.join(output_dir, "scurve_chart.png")
plt.savefig(scurve_path, dpi=300)
plt.close()
print("Saved scurve_chart.png")
