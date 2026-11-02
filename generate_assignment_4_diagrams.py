import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

output_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_4_Risk_Management\Diagrams"
os.makedirs(output_dir, exist_ok=True)

plt.rcParams['font.family'] = ['Calibri', 'Arial', 'Segoe UI', 'DejaVu Sans']
plt.rcParams['font.size'] = 9

# -------------------------------------------------------------
# 1. RISK BREAKDOWN STRUCTURE (RBS) HIERARCHICAL DIAGRAM
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
ax.axis('off')

# Root Node
root_box = patches.FancyBboxPatch((5.0, 7.2), 4.0, 0.75, boxstyle="round,pad=0.15", facecolor="#1e3a8a", edgecolor="#0f172a", linewidth=2)
ax.add_patch(root_box)
ax.text(7.0, 7.57, "RBS Level 0: ShalaConnect Project Risks\n(School Cluster Education Platform)", color="white", fontsize=10.5, fontweight="bold", ha="center", va="center")

# Categories (Level 1)
categories = [
    (1.2, 5.4, "1.0 Technical\nRisks", "#2563eb"),
    (3.5, 5.4, "2.0 Cost &\nInfrastructure", "#2563eb"),
    (5.8, 5.4, "3.0 Operational &\nAdoption", "#2563eb"),
    (8.2, 5.4, "4.0 Security &\nCompliance", "#2563eb"),
    (10.5, 5.4, "5.0 Schedule &\nResource", "#2563eb"),
    (12.8, 5.4, "6.0 External &\nOpportunities", "#059669")
]

for x, y, title, col in categories:
    c_box = patches.FancyBboxPatch((x-1.0, y-0.45), 2.0, 0.9, boxstyle="round,pad=0.1", facecolor=col, edgecolor="#1e293b", linewidth=1.5)
    ax.add_patch(c_box)
    ax.text(x, y, title, color="white", fontsize=9, fontweight="bold", ha="center", va="center")
    ax.plot([7.0, x], [7.2, 5.85], color="#64748b", lw=1.5, zorder=1)

# Specific Risk Items (Level 2)
sub_items = {
    1.2: [
        ("RSK-01 Offline Sync Conflict", 4.3),
        ("RSK-03 Dynamic JSON Schema", 3.4),
        ("RSK-04 Apache POI Heap Leak", 2.5),
        ("RSK-15 DB Pool Exhaustion", 1.6)
    ],
    3.5: [
        ("RSK-02 AWS Cost Overrun", 4.3),
        ("RSK-07 S3 Photo Storage Spike", 3.4),
        ("RSK-19 AWS Academic Credits", 2.5) # Opportunity
    ],
    5.8: [
        ("RSK-08 Meeting Acknowledge Lag", 4.3),
        ("RSK-09 Mobile UI Overflow", 3.4),
        ("RSK-16 Corrupted PDF Circular", 2.5),
        ("RSK-18 PM-SHRI Govt Adoption", 1.6) # Opportunity
    ],
    8.2: [
        ("RSK-05 Tenant Data Leakage", 4.3),
        ("RSK-10 DPDP Act Compliance", 3.4),
        ("RSK-14 Brute-Force Auth Attack", 2.5)
    ],
    10.5: [
        ("RSK-06 CI/CD Deploy Breakage", 4.3),
        ("RSK-11 Key Developer SPoF", 3.4),
        ("RSK-12 Semester Exam Delay", 2.5)
    ],
    12.8: [
        ("RSK-13 Rural Telecom Blackout", 4.3),
        ("RSK-17 PWA Zero-Data Caching", 3.4), # Opportunity
        ("RSK-20 Open Source Community", 2.5)  # Opportunity
    ]
}

for px, items in sub_items.items():
    for label, y in items:
        is_opp = "Opportunity" in str(label) or "Credit" in label or "Adopt" in label or "Caching" in label or "Community" in label
        bg_col = "#ecfdf5" if is_opp else "#f8fafc"
        edge_col = "#059669" if is_opp else "#475569"
        w_box = patches.FancyBboxPatch((px-1.05, y-0.3), 2.1, 0.6, boxstyle="round,pad=0.06", facecolor=bg_col, edgecolor=edge_col, linewidth=1.0)
        ax.add_patch(w_box)
        ax.text(px, y, label, color="#0f172a", fontsize=7.5, fontweight="bold" if is_opp else "normal", ha="center", va="center")
        ax.plot([px, px], [4.95, y+0.3], color="#94a3b8", lw=1.0, zorder=1)

ax.set_xlim(0, 14.0)
ax.set_ylim(0.8, 8.2)
ax.set_title("ShalaConnect - Hierarchical Risk Breakdown Structure (RBS) (PMBOK Guide 7th Edition)", fontsize=12.5, fontweight='bold', pad=14, color='#1e3a8a')

plt.tight_layout()
rbs_path = os.path.join(output_dir, "risk_breakdown_structure.png")
plt.savefig(rbs_path, dpi=300)
plt.close()
print("Saved risk_breakdown_structure.png")

# -------------------------------------------------------------
# 2. PROBABILITY-IMPACT (5x5) HEATMAP MATRIX
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)

# Matrix grid: 5 rows (P = 5 down to 1), 5 cols (I = 1 to 5)
matrix_colors = [
    # I=1       I=2       I=3       I=4       I=5
    ['#fef08a', '#fdba74', '#f87171', '#ef4444', '#b91c1c'], # P=5
    ['#fef08a', '#fed7aa', '#fb923c', '#f87171', '#ef4444'], # P=4
    ['#bbf7d0', '#fef08a', '#fed7aa', '#fb923c', '#f87171'], # P=3
    ['#86efac', '#bbf7d0', '#fef08a', '#fed7aa', '#fb923c'], # P=2
    ['#4ade80', '#86efac', '#bbf7d0', '#fef08a', '#fef08a'], # P=1
]

for row_idx, r_colors in enumerate(matrix_colors):
    p_level = 5 - row_idx
    for col_idx, bg in enumerate(r_colors):
        i_level = col_idx + 1
        score = p_level * i_level
        rect = patches.Rectangle((col_idx, 4 - row_idx), 1, 1, facecolor=bg, edgecolor='#ffffff', lw=2)
        ax.add_patch(rect)
        ax.text(col_idx + 0.12, 4 - row_idx + 0.82, f"{score}", fontsize=8, color='#64748b', fontweight='bold')

# Map of risks: (Risk ID, Probability, Impact, Short Label)
risk_points = [
    ("RSK-01", 4, 4, "Sync Conflict"),      # P=4, I=4 -> Score 16 (Red)
    ("RSK-05", 3, 5, "Tenant Leak"),        # P=3, I=5 -> Score 15 (Red)
    ("RSK-10", 3, 5, "DPDP Legal"),         # P=3, I=5 -> Score 15 (Red)
    ("RSK-02", 4, 3, "AWS Overrun"),        # P=4, I=3 -> Score 12 (Orange)
    ("RSK-04", 3, 4, "POI Heap Leak"),      # P=3, I=4 -> Score 12 (Orange)
    ("RSK-11", 3, 4, "Dev SPoF"),           # P=3, I=4 -> Score 12 (Orange)
    ("RSK-15", 3, 4, "DB Pool Rush"),       # P=3, I=4 -> Score 12 (Orange)
    ("RSK-03", 3, 3, "Dynamic Schema"),     # P=3, I=3 -> Score 9 (Yellow)
    ("RSK-06", 3, 3, "CI/CD Break"),        # P=3, I=3 -> Score 9 (Yellow)
    ("RSK-07", 3, 3, "S3 Photo Spike"),     # P=3, I=3 -> Score 9 (Yellow)
    ("RSK-14", 3, 3, "Brute Force"),        # P=3, I=3 -> Score 9 (Yellow)
    ("RSK-12", 4, 2, "Exam Schedule"),      # P=4, I=2 -> Score 8 (Yellow)
    ("RSK-08", 3, 2, "Meeting Acknowledge"),# P=3, I=2 -> Score 6 (Yellow)
    ("RSK-09", 3, 2, "Mobile UI Overflow"), # P=3, I=2 -> Score 6 (Yellow)
    ("RSK-13", 2, 3, "Telecom Blackout"),   # P=2, I=3 -> Score 6 (Yellow)
    ("RSK-16", 2, 3, "Corrupt PDF"),        # P=2, I=3 -> Score 6 (Yellow)
    ("OPP-17", 4, 3, "PWA Caching"),        # P=4, I=3 (Opportunity)
    ("OPP-18", 3, 4, "PM-SHRI Adopt"),      # P=3, I=4 (Opportunity)
    ("OPP-19", 4, 4, "AWS Grant"),          # P=4, I=4 (Opportunity)
    ("OPP-20", 3, 3, "OpenSource")          # P=3, I=3 (Opportunity)
]

# Plot Risk Pins with offset dispersal
cell_counts = {}
for rid, p, i, lbl in risk_points:
    cell_key = (p, i)
    idx_in_cell = cell_counts.get(cell_key, 0)
    cell_counts[cell_key] = idx_in_cell + 1
    
    # Coordinates in 5x5 grid
    cx = (i - 1) + 0.35 + (idx_in_cell % 2) * 0.35
    cy = (p - 1) + 0.30 + (idx_in_cell // 2) * 0.30
    
    is_opp = "OPP" in rid
    node_col = "#059669" if is_opp else ("#991b1b" if p*i >= 15 else ("#c2410c" if p*i >= 10 else "#854d0e"))
    
    ax.scatter(cx, cy, color=node_col, s=120, edgecolors='white', lw=1.2, zorder=5)
    ax.text(cx, cy - 0.16, f"{rid}\n{lbl}", fontsize=6.2, fontweight='bold', ha='center', va='top', color='#0f172a', zorder=6)

# Axes settings
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)
ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5])
ax.set_xticklabels(["1: Negligible", "2: Minor", "3: Moderate", "4: Major", "5: Critical"], fontsize=9, fontweight='bold', color='#1e293b')
ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5])
ax.set_yticklabels(["1: Rare (<10%)", "2: Unlikely (10-30%)", "3: Moderate (30-50%)", "4: Likely (50-70%)", "5: Highly Likely (>70%)"], fontsize=9, fontweight='bold', color='#1e293b')

ax.set_xlabel("IMPACT SEVERITY (FINANCIAL, SCHEDULE, QUALITY, LEGAL) →", fontsize=10, fontweight='bold', labelpad=10, color='#1e293b')
ax.set_ylabel("PROBABILITY OF OCCURRENCE →", fontsize=10, fontweight='bold', labelpad=10, color='#1e293b')
ax.set_title("ShalaConnect - 5x5 Probability-Impact (P-I) Risk Heatmap Matrix (16 Threats + 4 Opportunities)", fontsize=12.5, fontweight='bold', pad=14, color='#1e3a8a')

# Legend
leg_items = [
    ("Critical (15-25): Immediate Mitigation", "#b91c1c"),
    ("High (10-14): Active Risk Plan", "#ea580c"),
    ("Medium (5-9): Monitor & Review", "#ca8a04"),
    ("Low (1-4): Routine Acceptance", "#16a34a"),
    ("Opportunity (Green Pin)", "#059669")
]
for idx, (label, col) in enumerate(leg_items):
    lx = 0.1 + idx * 1.0
    ax.plot([lx, lx + 0.15], [-0.55, -0.55], color=col, lw=6, solid_capstyle='round')
    ax.text(lx + 0.2, -0.55, label, fontsize=6.8, color='#334155', va='center')

plt.tight_layout()
pi_path = os.path.join(output_dir, "probability_impact_matrix.png")
plt.savefig(pi_path, dpi=300)
plt.close()
print("Saved probability_impact_matrix.png")

# -------------------------------------------------------------
# 3. RISK RESPONSE & RESIDUAL SCORE REDUCTION DASHBOARD
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)

# Top 8 Priority Risks comparing Inherent vs Residual Score
top_risks = [
    ("RSK-01: Sync Conflict", 16, 4, "Mitigate: HMAC Unique Constraint"),
    ("RSK-05: Tenant Data Leak", 15, 3, "Avoid: Strict JWT Tenancy Checks"),
    ("RSK-10: DPDP Statutory", 15, 3, "Avoid: Sovereign AWS Mumbai Hosting"),
    ("RSK-02: AWS Cost Overrun", 12, 4, "Mitigate: Serverless Fargate & Alerts"),
    ("RSK-04: POI Memory Leak", 12, 3, "Mitigate: Streaming SXSSF Workbook"),
    ("RSK-11: Developer SPoF", 12, 4, "Mitigate: Comprehensive Code Docs"),
    ("RSK-15: DB Connection Rush", 12, 3, "Mitigate: HikariCP Max Pool Tuning"),
    ("RSK-03: Dynamic Schema JSON", 9, 2, "Mitigate: Semantic Versioned Schema")
]

labels = [r[0] for r in reversed(top_risks)]
inherent = [r[1] for r in reversed(top_risks)]
residual = [r[2] for r in reversed(top_risks)]
strategies = [r[3] for r in reversed(top_risks)]

y_pos = np.arange(len(labels))
h = 0.35

ax.barh(y_pos + h/2, inherent, height=h, color="#ef4444", label="Inherent Risk Score (Pre-Mitigation)", edgecolor="#991b1b")
ax.barh(y_pos - h/2, residual, height=h, color="#10b981", label="Residual Risk Score (Post-Mitigation)", edgecolor="#065f46")

for idx, (inh, res, strat) in enumerate(zip(inherent, residual, strategies)):
    reduction_pct = round(((inh - res) / inh) * 100)
    ax.text(inh + 0.3, idx + h/2, f"{inh} (Critical/High)", va='center', fontsize=7.5, color='#991b1b', fontweight='bold')
    ax.text(res + 0.3, idx - h/2, f"{res} (Low) [-{reduction_pct}%] | {strat}", va='center', fontsize=7.2, color='#047857')

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=8.5, fontweight='bold', color='#1e293b')
ax.set_xlabel("RISK SEVERITY SCORE (PROBABILITY x IMPACT → 1 TO 25)", fontsize=10, fontweight='bold', labelpad=10, color='#1e293b')
ax.set_xlim(0, 24)
ax.set_title("ShalaConnect - Risk Response Playbook & Residual Score Reduction Analysis (Top Priority Risks)", fontsize=12, fontweight='bold', pad=14, color='#1e3a8a')
ax.grid(axis='x', linestyle='--', alpha=0.5)
ax.legend(loc='lower right', framealpha=0.95, fontsize=8.5)

plt.tight_layout()
resp_path = os.path.join(output_dir, "risk_response_dashboard.png")
plt.savefig(resp_path, dpi=300)
plt.close()
print("Saved risk_response_dashboard.png")
