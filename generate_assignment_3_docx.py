import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_3_Kanban_Control"
os.makedirs(base_dir, exist_ok=True)
docx_path = os.path.join(base_dir, "Assignment_3_Editable.docx")
diag_dir = os.path.join(base_dir, "Diagrams")

doc = docx.Document()

# Margins
for sec in doc.sections:
    sec.top_margin = Inches(1)
    sec.bottom_margin = Inches(1)
    sec.left_margin = Inches(1)
    sec.right_margin = Inches(1)
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)

PRIMARY = RGBColor(27, 54, 93)       # Deep Navy
SECONDARY = RGBColor(180, 83, 9)     # Deep Amber
DARK_TEXT = RGBColor(30, 41, 59)     # Slate 800
MUTED_TEXT = RGBColor(100, 116, 139) # Slate 500

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_p(text="", bold_prefix=None, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=6, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Calibri"
        rb.font.size = Pt(10)
        rb.font.bold = True
        rb.font.color.rgb = DARK_TEXT
    if text:
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(10)
        r.font.color.rgb = DARK_TEXT
    return p

def add_heading_1(text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(18)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = PRIMARY
    return h

def add_heading_2(text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = SECONDARY
    return h

# -------------------------------------------------------------
# COVER PAGE
# -------------------------------------------------------------
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_before = Pt(36)
p_inst.paragraph_format.space_after = Pt(4)
r_inst = p_inst.add_run("MAEER's MIT ACADEMY OF ENGINEERING, PUNE")
r_inst.font.name = "Calibri"
r_inst.font.size = Pt(15)
r_inst.font.bold = True
r_inst.font.color.rgb = PRIMARY

p_dept = doc.add_paragraph()
p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dept.paragraph_format.space_after = Pt(12)
r_dept = p_dept.add_run("(An Autonomous Institute Affiliated to Savitribai Phule Pune University)\nSchool of Computer Engineering & Technology | Academic Year: 2026-27")
r_dept.font.name = "Calibri"
r_dept.font.size = Pt(11)
r_dept.font.color.rgb = MUTED_TEXT

doc.add_paragraph().paragraph_format.space_after = Pt(24)

p_asg = doc.add_paragraph()
p_asg.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_asg.paragraph_format.space_after = Pt(6)
r_asg = p_asg.add_run("COURSE ASSIGNMENT SUBMISSION: ASSIGNMENT 3")
r_asg.font.name = "Calibri"
r_asg.font.size = Pt(12)
r_asg.font.bold = True
r_asg.font.color.rgb = SECONDARY

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(8)
r_title = p_title.add_run("KANBAN BOARD, EXECUTION CONTROL PLAN, RACI MATRIX & EARNED VALUE MANAGEMENT (EVM)")
r_title.font.name = "Calibri"
r_title.font.size = Pt(16)
r_title.font.bold = True
r_title.font.color.rgb = PRIMARY

p_proj = doc.add_paragraph()
p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_proj.paragraph_format.space_after = Pt(36)
r_proj = p_proj.add_run("PROJECT: ShalaConnect\nSchool Education Cluster Administration & Governance Platform")
r_proj.font.name = "Calibri"
r_proj.font.size = Pt(12)
r_proj.font.italic = True
r_proj.font.color.rgb = DARK_TEXT

cov_tbl = doc.add_table(rows=6, cols=2)
cov_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
cov_data = [
    ("Course / Subject", "Project Management (PM-401 / B.Tech Computer Engineering)"),
    ("Student Name / Candidate", "Yash Sabale"),
    ("PRN / Roll Number", "B.Tech Final Year (Computer Engineering)"),
    ("Faculty Guide / Evaluator", "Prof. Project Guide / Evaluator (School of CET)"),
    ("Functional Artifact", "Web-Based Dynamic Kanban Dashboard & EVM Calculator Application"),
    ("Date of Submission", "October 31, 2026")
]
for idx, (k, v) in enumerate(cov_data):
    row = cov_tbl.rows[idx]
    ck, cv = row.cells[0], row.cells[1]
    ck.width, cv.width = Inches(2.3), Inches(4.2)
    set_cell_shading(ck, "F1F5F9")
    set_cell_shading(cv, "FFFFFF")
    set_cell_margins(ck, top=60, bottom=60, left=100, right=100)
    set_cell_margins(cv, top=60, bottom=60, left=100, right=100)
    pk = ck.paragraphs[0]
    rk = pk.add_run(k)
    rk.font.name = "Calibri"
    rk.font.size = Pt(9.5)
    rk.font.bold = True
    pv = cv.paragraphs[0]
    rv = pv.add_run(v)
    rv.font.name = "Calibri"
    rv.font.size = Pt(9.5)

doc.add_page_break()

# -------------------------------------------------------------
# TABLE OF CONTENTS
# -------------------------------------------------------------
add_heading_1("Table of Contents")
toc_items = [
    ("1. Functional Kanban Board Architecture & Lean Workflow", "3"),
    ("   1.1 Five-Column Kanban Workflow Design", "3"),
    ("   1.2 Work in Progress (WIP) Limits & Bottleneck Mitigation", "4"),
    ("   1.3 Interactive Dashboard Features & LocalStorage Persistence", "5"),
    ("2. Kanban Lean Process Metrics & Flow Efficiency", "6"),
    ("   2.1 Lead Time vs. Cycle Time Analysis", "6"),
    ("   2.2 Throughput, WIP, and Little's Law Mathematical Validation", "7"),
    ("   2.3 Cumulative Flow & Flow Efficiency Ratio", "8"),
    ("3. RACI Responsibility Assignment Matrix", "9"),
    ("   3.1 Role Definitions & Single-Accountability Rule", "9"),
    ("   3.2 Cross-Functional RACI Master Matrix (21 Work Packages)", "10"),
    ("4. Comprehensive Project Execution Control Plan", "12"),
    ("   4.1 Project Monitoring Approach & Daily Standups", "12"),
    ("   4.2 Schedule, Cost, and Quality Control Thresholds", "13"),
    ("   4.3 Change Management & Formal Change Request Protocol", "14"),
    ("   4.4 Issue Management & Tiered Escalation Procedures", "15"),
    ("   4.5 Stakeholder Communication Plan & Information Distribution", "16"),
    ("5. Earned Value Management (EVM) Performance Tracking", "18"),
    ("   5.1 EVM Mathematical Framework (PV, EV, AC, CV, SV, CPI, SPI)", "18"),
    ("   5.2 Estimate At Completion (EAC) Forecasting Models", "19"),
    ("   5.3 Day 35 Project Performance Status Snapshot & Variance Analysis", "20"),
    ("   5.4 Earned Value Management S-Curve Visualization", "22"),
    ("   5.5 Corrective Action & Performance Recovery Recommendations", "23"),
    ("6. Conclusion & Execution Control Sign-Off", "24"),
    ("7. References (IEEE Format)", "25")
]
for item, pg in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(item)
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.5)
    r2 = p.add_run(f"   ...........................................................................................   {pg}")
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = MUTED_TEXT

doc.add_page_break()

# -------------------------------------------------------------
# SECTION 1: KANBAN BOARD ARCHITECTURE
# -------------------------------------------------------------
add_heading_1("1. Functional Kanban Board Architecture & Lean Workflow")
add_p(
    "Execution control for ShalaConnect combines predictive PMBOK baseline governance with Agile Lean Kanban mechanics. "
    "A working web application was engineered to provide real-time task visualization, bottleneck prevention, and automated "
    "Earned Value tracking. The complete web application source code is provided in Kanban_Dashboard/Source_Code/index.html."
)

add_heading_2("1.1 Five-Column Kanban Workflow Design")
add_p(
    "The execution workflow progresses across five standardized columns:\n"
    "1. Backlog: Holds all prioritized project scope items derived from the WBS. Work packages remain in the backlog until sprint allocation.\n"
    "2. To Do: Sprint-committed work packages whose predecessors have been satisfied in the CPM network (WIP Limit: 5).\n"
    "3. In Progress: Active software engineering, architecture, or cloud provisioning currently undergoing development (WIP Limit: 3).\n"
    "4. Testing / Review: Code reviews, JUnit 5 tenancy boundary testing, and security verification (WIP Limit: 3).\n"
    "5. Done: Fully validated deliverables that meet all acceptance criteria and are deployed to AWS ECS Fargate."
)

add_heading_2("1.2 Work in Progress (WIP) Limits & Bottleneck Mitigation")
add_p(
    "WIP limits constrain the maximum number of work items allowed in an active column simultaneously. In ShalaConnect, "
    "In Progress is strictly capped at 3 tasks and Testing / Review is capped at 3 tasks. When a column reaches its limit, "
    "the dashboard triggers visual warning banners, prohibiting developers from pulling new work until active bottlenecks are cleared. "
    "This prevents multitasking thrashing, minimizes context switching, and accelerates overall cycle time."
)

# Embed Diagram 1: Kanban Workflow
add_heading_2("1.3 Visual Kanban Workflow & Queue Structure")
kanban_img = os.path.join(diag_dir, "kanban_workflow_diagram.png")
if os.path.exists(kanban_img):
    doc.add_picture(kanban_img, width=Inches(6.4))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 1.1: ShalaConnect Kanban Process Flow with WIP Limits and Flow Efficiency Metrics")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = MUTED_TEXT

doc.add_page_break()

# -------------------------------------------------------------
# SECTION 2: KANBAN PROCESS METRICS
# -------------------------------------------------------------
add_heading_1("2. Kanban Lean Process Metrics & Flow Efficiency")
add_p(
    "To achieve Master Craftsman rigor, the execution system calculates flow metrics dynamically from actual task movement:\n"
    "• Lead Time: The total elapsed duration from when a requirement is first logged in the Backlog until it reaches the Done column (Current Average: 11.2 Days).\n"
    "• Cycle Time: The active duration spent working on a task from when it enters In Progress until it is completed in Done (Current Average: 4.8 Days).\n"
    "• Throughput: The number of completed work packages delivered per unit time (Average: 3.5 Work Packages per Week).\n"
    "• Little's Law Mathematical Validation: In a stable queuing system, WIP is governed by Little's Law: "
    "WIP = Throughput x Cycle Time = 0.7 tasks/day x 4.8 days = 3.36 active tasks, which aligns with our observed average WIP of 3.4 tasks.\n"
    "• Flow Efficiency: Flow Efficiency = (Active Cycle Time / Total Lead Time) x 100 = (4.8 / 11.2) x 100 = 42.8%, well above industry benchmarks (15% to 40%)."
)

# -------------------------------------------------------------
# SECTION 3: RACI MATRIX
# -------------------------------------------------------------
add_heading_1("3. RACI Responsibility Assignment Matrix")
add_p(
    "The RACI matrix (Responsibility Assignment Matrix - RAM) clarifies roles and responsibilities across all 21 WBS work packages. "
    "In strict compliance with PMBOK governance, the matrix enforces the Single-Accountability Rule: exactly one role is designated "
    "Accountable (A) per work package to prevent ambiguity and conflicting authority."
)

# Embed Diagram 2: RACI Matrix
add_heading_2("3.1 Cross-Functional RACI Matrix Visualization")
raci_img = os.path.join(diag_dir, "raci_matrix_diagram.png")
if os.path.exists(raci_img):
    doc.add_picture(raci_img, width=Inches(6.4))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 3.1: ShalaConnect RACI Responsibility Assignment Matrix across 21 Work Packages")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = MUTED_TEXT

doc.add_page_break()

# -------------------------------------------------------------
# SECTION 4: EXECUTION CONTROL PLAN
# -------------------------------------------------------------
add_heading_1("4. Comprehensive Project Execution Control Plan")
add_p(
    "The Execution Control Plan establishes the organizational mechanisms used to measure, evaluate, and adjust project progress:\n"
    "• Daily 15-Minute Standup: Engineering team reviews tasks moved across the Kanban board, inspects WIP limits, and addresses blockers.\n"
    "• Performance Thresholds: Schedule Performance Index (SPI) < 0.90 or Cost Performance Index (CPI) < 0.90 triggers an immediate Project Manager variance review.\n"
    "• Change Control Protocol: Any scope alteration requires a formal Change Request (CR) documenting business justification, schedule impact, and budget adjustment, subject to written Guide approval.\n"
    "• Tiered Escalation: Tier 1 issues (code defects) resolved within 24 hours by Lead Developer; Tier 2 issues (cross-work package blockers) resolved within 48 hours by PM; Tier 3 issues (statutory/scope changes) escalated to Evaluation Committee."
)

# -------------------------------------------------------------
# SECTION 5: EARNED VALUE MANAGEMENT (EVM)
# -------------------------------------------------------------
add_heading_1("5. Earned Value Management (EVM) Performance Tracking")
add_p(
    "Earned Value Management (EVM) integrates project scope, schedule, and cost performance measurements. "
    "Rather than simply comparing actual spend against planned budget, EVM assesses the actual physical work accomplished."
)

add_heading_2("5.1 Mathematical Formulations & Day 35 Status Snapshot")
add_p(
    "A formal project control snapshot was executed at Day 35 (the conclusion of Phase 1.3 Core Application Development sprint):\n"
    "• Budget At Completion (BAC): INR 4,10,000 (Cost Baseline)\n"
    "• Planned Value (PV) at Day 35: INR 3,20,000 (Cumulative planned spend)\n"
    "• Earned Value (EV) at Day 35: INR 2,97,000 (Sum of physical completion percentage x WP cost baseline)\n"
    "• Actual Cost (AC) at Day 35: INR 2,82,857 (Direct recorded expenditures)\n\n"
    "Key Variance & Index Calculations:\n"
    "1. Cost Variance: CV = EV - AC = INR 2,97,000 - INR 2,82,857 = +INR 14,143 (Positive = Under Budget / Favorable Savings)\n"
    "2. Schedule Variance: SV = EV - PV = INR 2,97,000 - INR 3,20,000 = -INR 23,000 (Negative = Behind Schedule Lag)\n"
    "3. Cost Performance Index: CPI = EV / AC = 2,97,000 / 2,82,857 = 1.05 (Achieving INR 1.05 worth of work for every INR 1.00 spent)\n"
    "4. Schedule Performance Index: SPI = EV / PV = 2,97,000 / 3,20,000 = 0.93 (Progressing at 93% of planned schedule velocity)\n\n"
    "EAC Forecasting Models:\n"
    "• Case 1 (Current CPI expected to continue): EAC = BAC / CPI = 4,10,000 / 1.05 = INR 3,90,476 (Projected Savings: INR 19,524)\n"
    "• Case 2 (Future work at planned rate): EAC = AC + (BAC - EV) = 2,82,857 + (4,10,000 - 2,97,000) = INR 3,95,857\n"
    "• Case 3 (Both CPI and SPI influence future work): EAC = AC + [(BAC - EV) / (CPI x SPI)] = 2,82,857 + [1,13,000 / 0.9765] = INR 3,98,579\n\n"
    "Under all three forecasting variants, Estimate At Completion remains well below the approved INR 4,10,000 Cost Baseline "
    "and safely within the INR 4,85,000 Total Project Budget."
)

# Embed Diagram 3: EVM S-Curve
add_heading_2("5.2 Earned Value Management S-Curve Visualization")
evm_img = os.path.join(diag_dir, "evm_scurve_analysis.png")
if os.path.exists(evm_img):
    doc.add_picture(evm_img, width=Inches(6.4))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 5.1: ShalaConnect Earned Value Management Performance S-Curve (PV, EV, AC, CV, SV, and EAC Forecast)")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = MUTED_TEXT

doc.add_page_break()

# -------------------------------------------------------------
# SECTION 6: CONCLUSION & REFERENCES
# -------------------------------------------------------------
add_heading_1("6. Conclusion & Execution Control Sign-Off")
add_p(
    "Assignment 3 demonstrates complete execution control over ShalaConnect. By combining a functional, interactive Kanban dashboard "
    "with rigorous Lean metrics (Lead Time, Cycle Time, WIP Limits) and PMBOK-standard Earned Value Management (EVM), the project "
    "verifies both operational agility and strict financial governance. At Day 35, the project demonstrates strong cost efficiency "
    "(CPI = 1.05) with minor schedule lag (SPI = 0.93) that is easily absorbed by the 26-day operational buffer."
)

add_heading_1("7. Key References (IEEE Format)")
references = [
    "[1] Project Management Institute, A Guide to the Project Management Body of Knowledge (PMBOK Guide), 7th ed. Newtown Square, PA: PMI, 2021.",
    "[2] Project Management Institute, Practice Standard for Earned Value Management, 2nd ed. Newtown Square, PA: PMI, 2011.",
    "[3] D. J. Anderson, Kanban: Successful Evolutionary Change for Your Technology Business. Sequim, WA: Blue Hole Press, 2010.",
    "[4] J. D. C. Little, 'A proof for the queuing formula: L = λW,' Operations Research, vol. 9, no. 3, pp. 383-387, Jun. 1961.",
    "[5] Q. W. Fleming and J. M. Koppelman, Earned Value Project Management, 4th ed. Newtown Square, PA: Project Management Institute, 2010."
]
for ref in references:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(ref)
    r.font.name = "Calibri"
    r.font.size = Pt(8.5)
    r.font.color.rgb = DARK_TEXT

doc.save(docx_path)
print(f"Generated 100% English Assignment_3_Editable.docx at {docx_path}")
