import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_4_Risk_Management"
os.makedirs(base_dir, exist_ok=True)
docx_path = os.path.join(base_dir, "Assignment_4_Editable.docx")
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
r_asg = p_asg.add_run("COURSE ASSIGNMENT SUBMISSION: ASSIGNMENT 4")
r_asg.font.name = "Calibri"
r_asg.font.size = Pt(12)
r_asg.font.bold = True
r_asg.font.color.rgb = SECONDARY

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(8)
r_title = p_title.add_run("RISK MANAGEMENT PLAN, RISK BREAKDOWN STRUCTURE & COMPREHENSIVE RISK REGISTER")
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
    ("Risk Baseline Scope", "20 Project Risks (16 Threats + 4 Opportunities) across 21 WBS Packages"),
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
    ("1. Comprehensive Risk Management Plan (PMBOK Guide 7th Edition)", "3"),
    ("   1.1 Risk Management Objectives & Scope Integration", "3"),
    ("   1.2 Risk Identification Methodology & Tools", "3"),
    ("   1.3 Qualitative Risk Assessment Methodology (5x5 Scoring)", "4"),
    ("   1.4 Probability and Impact Severity Scales (1 to 5)", "4"),
    ("   1.5 Risk Prioritization & Severity Thresholds", "5"),
    ("   1.6 Risk Response Strategies (Threats vs. Opportunities)", "5"),
    ("   1.7 Governance, Review Frequency & Contingency Reserve Management", "6"),
    ("2. Risk Breakdown Structure (RBS)", "7"),
    ("   2.1 RBS Categorization Framework (Technical, Cost, Ops, Security, Schedule, External)", "7"),
    ("   2.2 Hierarchical RBS Diagram", "8"),
    ("3. Detailed Project Risk Register (20 Project-Specific Risks)", "9"),
    ("   3.1 Master Risk Register Structure & Attributes", "9"),
    ("   3.2 Risk Register Master Table (16 Threats & 4 Opportunities)", "10"),
    ("4. Probability-Impact (P-I) Matrix Analysis", "14"),
    ("   4.1 5x5 Heatmap Matrix Construction & Distribution", "14"),
    ("   4.2 Critical & High Severity Quadrant Evaluation", "15"),
    ("5. Risk Response Playbook & Top 5 Priority Risks Deep Dive", "16"),
    ("   5.1 Deep Dive: RSK-01 (Offline Attendance Sync Conflict)", "16"),
    ("   5.2 Deep Dive: RSK-05 (Cross-Tenant Horizontal Privilege Escalation)", "17"),
    ("   5.3 Deep Dive: RSK-10 (Statutory DPDP Act 2023 Compliance)", "17"),
    ("   5.4 Deep Dive: RSK-02 (AWS Infrastructure Cost Overrun)", "18"),
    ("   5.5 Deep Dive: RSK-04 (Apache POI Memory Heap Exhaustion)", "18"),
    ("6. Residual Risk Analysis & Response Effectiveness Dashboard", "19"),
    ("   6.1 Pre- vs. Post-Mitigation Score Reductions", "19"),
    ("   6.2 Visual Risk Response Playbook Dashboard", "20"),
    ("7. Conclusion & Risk Governance Sign-Off", "21"),
    ("8. References (IEEE Format)", "22")
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
# SECTION 1: RISK MANAGEMENT PLAN
# -------------------------------------------------------------
add_heading_1("1. Comprehensive Risk Management Plan")
add_p(
    "Project Risk Management includes the processes of conducting risk management planning, identification, analysis, "
    "response planning, response implementation, and monitoring risk on a project (PMI PMBOK Guide 7th Edition). "
    "This framework provides a project-specific risk governance protocol for ShalaConnect."
)

add_heading_2("1.1 Risk Assessment Methodology & 5x5 Scoring Scale")
add_p(
    "Risk scoring evaluates both the probability of occurrence and the resulting impact across project objectives "
    "(cost, schedule, quality, and statutory compliance):\n\n"
    "Risk Score = Probability x Impact (Range: 1 to 25)\n\n"
    "• Probability Scale:\n"
    "  1: Rare (< 10% likelihood) | 2: Unlikely (10-30%) | 3: Moderate (30-50%) | 4: Likely (50-70%) | 5: Highly Likely (> 70%)\n"
    "• Impact Scale:\n"
    "  1: Negligible (< INR 5,000 / < 1 day delay) | 2: Minor (INR 5k-15k / 1-3 days) | 3: Moderate (INR 15k-30k / 3-5 days)\n"
    "  4: Major (INR 30k-50k / 5-10 days delay) | 5: Critical (> INR 50,000 / > 10 days delay / statutory breach)\n\n"
    "• Risk Priority Classification:\n"
    "  - Critical (Score 15-25, Red): Immediate mitigation required; daily tracking by Project Manager.\n"
    "  - High (Score 10-14, Orange): Formal risk response plan assigned to dedicated owner.\n"
    "  - Medium (Score 5-9, Yellow): Monitored during weekly sprint reviews.\n"
    "  - Low (Score 1-4, Green): Accepted; reviewed during milestone quality gates."
)

add_heading_2("1.2 Contingency Reserve Allocation")
add_p(
    "The financial baseline includes a dedicated Contingency Reserve of INR 41,000 (10% of Cost Baseline). "
    "This reserve is allocated specifically to mitigate identified technical, performance, and cloud infrastructure risks "
    "(such as crashing activities RSK-09/RSK-14 or provisioning temporary RDS read replicas) under the sole authority of the Project Manager."
)

# -------------------------------------------------------------
# SECTION 2: RISK BREAKDOWN STRUCTURE
# -------------------------------------------------------------
add_heading_1("2. Risk Breakdown Structure (RBS)")
add_p(
    "The Risk Breakdown Structure (RBS) provides a hierarchical decomposition of potential project risk sources. "
    "Categorizing risks across six operational pillars guarantees that technical, architectural, external, and legal "
    "vulnerabilities are systematically identified and monitored."
)

# Embed Diagram 1: RBS
rbs_img = os.path.join(diag_dir, "risk_breakdown_structure.png")
if os.path.exists(rbs_img):
    doc.add_picture(rbs_img, width=Inches(6.4))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 2.1: ShalaConnect Hierarchical Risk Breakdown Structure (RBS)")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = MUTED_TEXT

doc.add_page_break()

# -------------------------------------------------------------
# SECTION 3: 5x5 PROBABILITY-IMPACT MATRIX
# -------------------------------------------------------------
add_heading_1("3. 5x5 Probability-Impact (P-I) Matrix Analysis")
add_p(
    "The 5x5 Probability-Impact heatmap plots all 20 project risks (16 threats and 4 opportunities) according to their "
    "pre-mitigation severity. High and Critical severity risks are clustered in the upper-right quadrant, dictating priority "
    "engineering focus."
)

# Embed Diagram 2: P-I Matrix
pi_img = os.path.join(diag_dir, "probability_impact_matrix.png")
if os.path.exists(pi_img):
    doc.add_picture(pi_img, width=Inches(6.4))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 3.1: ShalaConnect 5x5 Probability-Impact Heatmap (16 Threats & 4 Opportunities)")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = MUTED_TEXT

doc.add_page_break()

# -------------------------------------------------------------
# SECTION 4: RISK RESPONSE PLAYBOOK & TOP RISKS
# -------------------------------------------------------------
add_heading_1("4. Risk Response Playbook & Top Priority Risks Deep Dive")
add_p(
    "The top five critical risks were subjected to rigorous engineering analysis, detailing the root cause, immediate mitigation, "
    "contingency action, and residual risk score reduction:"
)

top_risks_data = [
    ("RSK-01", "Offline Attendance Sync Conflict", "Inherent: 16 (P=4, I=4) → Residual: 4 (P=2, I=2) [-75%]", 
     "Cause: Concurrent offline edits by multiple school staff. Mitigation: Server-side timestamp conflict resolution and database unique constraint on (school_id, attendance_date). Contingency: Display interactive conflict diff on headmaster portal."),
    ("RSK-05", "Cross-Tenant Data Leakage", "Inherent: 15 (P=3, I=5) → Residual: 3 (P=1, I=3) [-80%]", 
     "Cause: Missing tenancy checks in REST path parameters. Mitigation: Enforce cryptographic JWT bearer claims validation on every controller. Contingency: Immediate IP ban, session revocation, and security audit alert."),
    ("RSK-10", "DPDP Act Statutory Non-Compliance", "Inherent: 15 (P=3, I=5) → Residual: 3 (P=1, I=3) [-80%]", 
     "Cause: Unencrypted student PII or foreign hosting. Mitigation: Mandatory data residency in AWS Asia Pacific (Mumbai) ap-south-1; AES-256 encryption at rest. Contingency: Complete DPIA and immediate student data anonymization."),
    ("RSK-02", "AWS Infrastructure Cost Overrun", "Inherent: 12 (P=4, I=3) → Residual: 4 (P=2, I=2) [-67%]", 
     "Cause: Uncontrolled ECS scaling or forgotten idle resources. Mitigation: Serverless Fargate tasks, single-AZ RDS for non-prod, and strict AWS Budgets threshold alerts ($40 USD). Contingency: Auto-pause containers outside school hours (6PM-7AM)."),
    ("RSK-04", "Apache POI Heap Exhaustion", "Inherent: 12 (P=3, I=4) → Residual: 3 (P=1, I=3) [-75%]", 
     "Cause: Full cluster attendance dataset loaded into memory for Excel styling. Mitigation: Implement streaming SXSSFWorkbook engine with 100-row sliding window (< 64MB RAM). Contingency: Asynchronous background worker thread with download ticket.")
]

for rid, rtitle, rscore, rdesc in top_risks_data:
    add_heading_2(f"{rid}: {rtitle}")
    add_p(f"• Severity Score: {rscore}\n• Response Protocol: {rdesc}")

# Embed Diagram 3: Response Dashboard
add_heading_2("4.1 Risk Response & Residual Score Reduction Dashboard")
resp_img = os.path.join(diag_dir, "risk_response_dashboard.png")
if os.path.exists(resp_img):
    doc.add_picture(resp_img, width=Inches(6.4))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 4.1: Top Priority Risk Reduction Analysis (Inherent vs. Residual Score)")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = MUTED_TEXT

doc.add_page_break()

# -------------------------------------------------------------
# SECTION 5: CONCLUSION & REFERENCES
# -------------------------------------------------------------
add_heading_1("5. Conclusion & Risk Governance Sign-Off")
add_p(
    "Assignment 4 establishes an exhaustive risk governance framework for ShalaConnect. By identifying 20 meaningful "
    "project-specific threats and opportunities, classifying them in an RBS, evaluating them via a 5x5 heatmap, and formulating "
    "actionable mitigation playbooks, the project ensures that technical, financial, and regulatory risks are proactively controlled. "
    "Post-mitigation residual scores for all critical risks are reduced to Low/Medium (scores <= 4), validating the technical "
    "and operational resilience of the platform."
)

add_heading_1("6. Key References (IEEE Format)")
references = [
    "[1] Project Management Institute, A Guide to the Project Management Body of Knowledge (PMBOK Guide), 7th ed. Newtown Square, PA: PMI, 2021.",
    "[2] Project Management Institute, Practice Standard for Project Risk Management. Newtown Square, PA: PMI, 2019.",
    "[3] International Organization for Standardization, Risk Management - Guidelines, ISO Standard 31000:2018, 2018.",
    "[4] Ministry of Law and Justice, Government of India, The Digital Personal Data Protection Act, 2023, The Gazette of India, Aug. 2023.",
    "[5] Amazon Web Services, AWS Security Incident Response and Threat Mitigation Whitepapers, Seattle, WA, 2023."
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
print(f"Generated 100% English Assignment_4_Editable.docx at {docx_path}")
