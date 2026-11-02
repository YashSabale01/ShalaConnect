import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_1_WBS"
os.makedirs(base_dir, exist_ok=True)
docx_path = os.path.join(base_dir, "Assignment_1_Editable.docx")
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

PRIMARY = RGBColor(27, 54, 93)       # Deep Navy (#1B365D)
SECONDARY = RGBColor(180, 83, 9)     # Deep Amber (#B45309)
DARK_TEXT = RGBColor(30, 41, 59)     # Slate 800 (#1E293B)
MUTED_TEXT = RGBColor(100, 116, 139) # Slate 500 (#64748B)

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
r_asg = p_asg.add_run("COURSE ASSIGNMENT SUBMISSION: ASSIGNMENT 1")
r_asg.font.name = "Calibri"
r_asg.font.size = Pt(12)
r_asg.font.bold = True
r_asg.font.color.rgb = SECONDARY

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(8)
r_title = p_title.add_run("PROJECT CHARTER, WORK BREAKDOWN STRUCTURE (WBS) & WBS DICTIONARY")
r_title.font.name = "Calibri"
r_title.font.size = Pt(18)
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
    ("Target Organization Domain", "Cluster Resource Centers (CRC), Maharashtra State Education Dept"),
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
    ("1. Comprehensive Project Charter (PMBOK Guide 7th Edition Standards)", "3"),
    ("   1.1 Project Identification and Overview", "3"),
    ("   1.2 Background and Business Justification", "3"),
    ("   1.3 Problem Statement & Current Operational Inefficiencies", "4"),
    ("   1.4 Business Need & Strategic Alignment (NEP 2020 / PM-SHRI)", "4"),
    ("   1.5 SMART Project Objectives", "5"),
    ("   1.6 Project Scope: In-Scope vs. Explicit Out-of-Scope Exclusions", "5"),
    ("   1.7 Major Project Deliverables", "6"),
    ("   1.8 Acceptance Criteria & Quality Gates", "6"),
    ("   1.9 High-Level Project Milestones & Target Schedule", "7"),
    ("   1.10 Stakeholder Identification & Comprehensive Stakeholder Register", "7"),
    ("   1.11 Stakeholder Power-Interest Matrix Analysis", "9"),
    ("   1.12 Enterprise Environmental Factors (EEF)", "9"),
    ("   1.13 Organizational Process Assets (OPA)", "10"),
    ("   1.14 Project Assumptions", "10"),
    ("   1.15 Project Constraints", "11"),
    ("   1.16 High-Level Project Risks & Initial Mitigation Strategies", "11"),
    ("   1.17 Project Manager's Authority, Decision Rights & Limitations", "12"),
    ("   1.18 Formal Sign-off and Authorization Protocol", "12"),
    ("2. Work Breakdown Structure (WBS) - Deliverable-Oriented Decomposition", "13"),
    ("   2.1 WBS Design Methodology & The 100% Rule Compliance", "13"),
    ("   2.2 Hierarchical WBS Coding Structure (Level 1 to Level 3)", "13"),
    ("   2.3 Traceability Matrix: Scope to WBS Work Packages", "15"),
    ("3. Detailed WBS Dictionary (21 Work Packages)", "16"),
    ("   3.1 Phase 1.1: Project Initiation & Requirements Engineering", "16"),
    ("   3.2 Phase 1.2: System Architecture & Technical Design", "18"),
    ("   3.3 Phase 1.3: Core Application Development & Implementation", "20"),
    ("   3.4 Phase 1.4: Cloud Infrastructure, DevOps & Security Hardening", "24"),
    ("   3.5 Phase 1.5: Quality Assurance, Pilot Rollout & Handover", "26"),
    ("4. Architectural Diagrams & Visual Artifacts", "28"),
    ("   4.1 Project Scope Hierarchy Diagram", "28"),
    ("   4.2 Hierarchical Work Breakdown Structure (WBS) Tree", "29"),
    ("   4.3 Stakeholder Power-Interest Grid", "30"),
    ("5. Conclusion & Academic Sign-off", "31"),
    ("6. References (IEEE Format)", "32")
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
# SECTION 1: PROJECT CHARTER (100% ENGLISH)
# -------------------------------------------------------------
add_heading_1("1. Comprehensive Project Charter")
add_p(
    "A Project Charter formally authorizes the existence of a project and provides the project manager with the "
    "authority to apply organizational resources to project activities (PMI PMBOK Guide 7th Edition). This document "
    "establishes the complete baseline for ShalaConnect, customized to the administrative context of rural and "
    "semi-urban public education clusters."
)

add_heading_2("1.1 Project Identification and Overview")
add_p(
    "ShalaConnect is an enterprise-grade cloud-native school cluster education administration and governance platform. "
    "The project digitizes and automates communication, compliance tracking, and administrative data flows between "
    "Cluster Resource Centers (CRC) and primary/secondary School Principals / Headmasters across public educational networks."
)
meta_p = add_p()
meta_p.add_run("- Project Title: ").bold = True
meta_p.add_run("ShalaConnect - School Education Cluster Administration & Governance Platform\n")
meta_p.add_run("- Project Code: ").bold = True
meta_p.add_run("MITAOE-PM-2026-SC01\n")
meta_p.add_run("- Sponsoring Body: ").bold = True
meta_p.add_run("School of Computer Engineering & Technology, MIT Academy of Engineering, Pune\n")
meta_p.add_run("- Target Deployment Domain: ").bold = True
meta_p.add_run("Cluster Resource Centers (CRC), Maharashtra State Department of School Education\n")
meta_p.add_run("- Project Lead / Manager: ").bold = True
meta_p.add_run("Yash Sabale (B.Tech Computer Engineering)\n")
meta_p.add_run("- Project Life Cycle: ").bold = True
meta_p.add_run("16 Calendar Weeks (4 Months / 80 Working Days / 112 Calendar Days)\n")
meta_p.add_run("- Financial Baseline: ").bold = True
meta_p.add_run("INR 4,85,000 (USD 5,850) approved project budget")

add_heading_2("1.2 Background and Business Justification")
add_p(
    "Under the decentralized educational administration of Maharashtra, government schools are grouped into administrative "
    "clusters known as Resource Clusters (Kendras), each headed by a Cluster Resource Center Head (Cluster Administrator). "
    "A single cluster typically oversees between 20 to 50 primary and upper-primary schools spread across multiple rural villages. "
    "Historically, this tier has relied almost entirely on manual paper registers, physical courier dispatches, and informal "
    "messaging channels for administrative compliance."
)
add_p(
    "The business justification for ShalaConnect rests on four core operational imperatives:\n"
    "1. Elimination of 30-Day Reporting Lag: Monthly compilation of student attendance and Mid-Day Meal (MDM) headcounts prevents timely interventions for chronically absent students.\n"
    "2. Elimination of Messaging Channel Compliance Gaps: Official circulars, Government Resolutions (GRs), and urgent data collection calls shared over informal messaging apps lack read-receipt verification and persistent audit trails.\n"
    "3. Drastic Reduction of Bureaucratic Workload: School Headmasters divert an estimated 25% of instructional time into manually preparing repetitive survey tables for Block Education Officers (BEO).\n"
    "4. Public Accountability and Transparency: Parents and local village panchayats lack access to verified school infrastructure, student achievements, and attendance metrics."
)

add_heading_2("1.3 Problem Statement & Current Operational Inefficiencies")
add_p(
    "Rural educational administration suffers from three compounding bottlenecks:\n"
    "- Infrastructure Bottlenecks: Rural schools frequently operate under intermittent 2G/3G mobile connectivity. Standard cloud applications fail to function offline, leading to total operational abandonment.\n"
    "- Auditability Deficits: When BEO inspections occur, historical records of attendance and celebration proofs are either missing or inconsistent across multiple disparate paper files.\n"
    "- High Cost of Manual Consolidation: Aggregating survey responses across 40 schools requires manual spreadsheet data entry by CRC personnel, taking an average of 4 business days per survey."
)

add_heading_2("1.4 Business Need & Strategic Alignment (NEP 2020 / PM-SHRI)")
add_p(
    "ShalaConnect directly operationalizes Section 3 and Section 7 of the National Education Policy (NEP 2020), which mandate "
    "the establishment of school complexes/clusters for resource sharing, governance transparency, and data-driven administrative "
    "efficiency. The platform satisfies the standards set forth by PM-SHRI (Prime Minister Schools for Rising India) and the "
    "Ministry of Education's Unified District Information System for Education Plus (UDISE+) framework by providing real-time "
    "compliance tracking, automated Excel report card generation for BEOs, and standardized accessible interfaces."
)

add_heading_2("1.5 SMART Project Objectives")
smart_table_data = [
    ("Specific (S)", "Digitize daily student/teacher attendance across 100% of cluster schools and replace informal circulars with an audit-backed policy circular dissemination repository."),
    ("Measurable (M)", "Achieve >= 98% daily attendance submission compliance before 11:00 AM; reduce BEO monthly report generation time from 4 days to < 5 seconds via one-click Excel compilation."),
    ("Achievable (A)", "Deliver an offline-first progressive SPA built on React 18, Spring Boot 21, and PostgreSQL 16 capable of running reliably on low-end 2G/3G rural mobile devices."),
    ("Relevant (R)", "Directly eliminate bureaucratic workload for rural headmasters while empowering CRC Administrators with real-time cluster compliance dashboards."),
    ("Time-bound (T)", "Complete baseline architecture, development, AWS cloud infrastructure provisioning, and end-to-end validation within a 16-week project execution timeline.")
]
tbl_s = doc.add_table(rows=len(smart_table_data)+1, cols=2)
tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_s = tbl_s.rows[0]
hdr_s.cells[0].width, hdr_s.cells[1].width = Inches(1.8), Inches(4.7)
set_cell_shading(hdr_s.cells[0], "1E3A8A")
set_cell_shading(hdr_s.cells[1], "1E3A8A")
hdr_s.cells[0].paragraphs[0].add_run("SMART Criterion").font.bold = True
hdr_s.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
hdr_s.cells[1].paragraphs[0].add_run("Project Implementation Commitment").font.bold = True
hdr_s.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

for idx, (crit, desc) in enumerate(smart_table_data):
    row = tbl_s.rows[idx+1]
    c0, c1 = row.cells[0], row.cells[1]
    c0.width, c1.width = Inches(1.8), Inches(4.7)
    set_cell_shading(c0, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
    set_cell_shading(c1, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
    set_cell_margins(c0, 50, 50, 80, 80)
    set_cell_margins(c1, 50, 50, 80, 80)
    p0 = c0.paragraphs[0]
    p0.add_run(crit).font.bold = True
    p1 = c1.paragraphs[0]
    p1.add_run(desc)

add_p()

add_heading_2("1.6 Project Scope: In-Scope vs. Out-of-Scope Items")
scope_tbl_data = [
    ("In-Scope Capabilities", "- Multi-tenant Role-Based Access Control (RBAC) with strict school tenancy validation.\n- Daily student & teacher attendance tracking with offline caching and automatic sync.\n- Automated BEO monthly attendance report card export (.xlsx) with compliance status.\n- Government Resolutions (GR) repository with PDF uploads (<= 20MB) and read receipts.\n- Cluster review meeting coordination with offline/online venues and RSVP logging.\n- School celebration event tracking with multi-photo upload and public photo galleries.\n- Dynamic survey form builder supporting TEXT, NUMBER, SELECT, DATE with tabular Excel export.\n- Public school directory search by UDISE code, village, and facility inspection.\n- 100% Terraform AWS infrastructure (ECS Fargate, ALB, RDS, CloudFront, S3, Route 53).\n- Automated GitHub Actions CI/CD pipeline for zero-downtime rolling deployments."),
    ("Out-of-Scope Exclusions", "- Direct payroll processing and teacher salary disbursal (governed by State Treasury portal).\n- Student fee collection or commercial payment gateway integration (free public education).\n- Direct SMS gateway carrier subscriptions (push notifications used to eliminate carrier costs).\n- Native iOS/Android app store publication (replaced by mobile-optimized PWA architecture).\n- Real-time video conferencing server hosting (external Google Meet/Zoom URLs integrated).\n- Legacy physical paper scanning or historical archive OCR conversion beyond current academic year.")
]
tbl_sc = doc.add_table(rows=3, cols=2)
tbl_sc.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_sc = tbl_sc.rows[0]
hdr_sc.cells[0].width, hdr_sc.cells[1].width = Inches(2.2), Inches(4.3)
set_cell_shading(hdr_sc.cells[0], "1E3A8A")
set_cell_shading(hdr_sc.cells[1], "1E3A8A")
hdr_sc.cells[0].paragraphs[0].add_run("Scope Classification").font.bold = True
hdr_sc.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
hdr_sc.cells[1].paragraphs[0].add_run("Detailed Functional Boundaries").font.bold = True
hdr_sc.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

for idx, (cat, desc) in enumerate(scope_tbl_data):
    row = tbl_sc.rows[idx+1]
    c0, c1 = row.cells[0], row.cells[1]
    c0.width, c1.width = Inches(2.2), Inches(4.3)
    set_cell_shading(c0, "F1F5F9" if idx==0 else "FEE2E2")
    set_cell_shading(c1, "FFFFFF" if idx==0 else "FFF1F2")
    set_cell_margins(c0, 60, 60, 80, 80)
    set_cell_margins(c1, 60, 60, 80, 80)
    p0 = c0.paragraphs[0]
    p0.add_run(cat).font.bold = True
    p1 = c1.paragraphs[0]
    p1.add_run(desc)

add_p()

add_heading_2("1.7 Major Deliverables & Acceptance Criteria")
add_p(
    "Major deliverables encompass: (1) Production Cloud Web App (Spring Boot 21 + React 18 SPA), (2) Modular Terraform AWS suite, "
    "(3) Apache POI Excel BEO export engine, (4) Automated GitHub Actions CI/CD pipeline, (5) Comprehensive QA test suites (>80% coverage), "
    "and (6) Professional Academic Project Documentation and User Manuals. Acceptance requires zero tenancy leakage, p95 latency < 120ms, "
    "and UAT sign-off from Cluster Administrators."
)

add_heading_2("1.8 High-Level Milestones")
ms_data = [
    ("M1: Project Charter & Baseline Approval", "Week 2 (Day 10)", "Project Charter, WBS, Initial Traceability Matrix approved by Guide"),
    ("M2: System Architecture & Design Freeze", "Week 4 (Day 20)", "ERD, OpenAPI specs, responsive Figma prototypes, and AWS blueprint signed off"),
    ("M3: Core Platform Development Sprint", "Week 10 (Day 50)", "Attendance, GR, Meetings, Forms, and BEO reporting modules functionally complete"),
    ("M4: AWS Cloud Infrastructure & CI/CD", "Week 12 (Day 60)", "Terraform scripts applied; ECS Fargate & CloudFront live; GitHub Actions automated"),
    ("M5: Field Pilot UAT & QA Verification", "Week 15 (Day 75)", "5-school pilot executed; Cluster Administrator UAT sign-off; security audit passed"),
    ("M6: Final Academic Defense & Handover", "Week 16 (Day 80)", "All 4 assignments submitted; Viva presentation completed; repository archived")
]
tbl_m = doc.add_table(rows=len(ms_data)+1, cols=3)
tbl_m.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_m = tbl_m.rows[0]
hdr_m.cells[0].width, hdr_m.cells[1].width, hdr_m.cells[2].width = Inches(2.2), Inches(1.5), Inches(2.8)
set_cell_shading(hdr_m.cells[0], "1E3A8A")
set_cell_shading(hdr_m.cells[1], "1E3A8A")
set_cell_shading(hdr_m.cells[2], "1E3A8A")
for idx, title in enumerate(["Milestone Description", "Target Timeline", "Acceptance Deliverable / Criteria"]):
    c = hdr_m.cells[idx]
    p = c.paragraphs[0]
    p.add_run(title).font.bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

for idx, (m_name, m_time, m_crit) in enumerate(ms_data):
    row = tbl_m.rows[idx+1]
    for c_i, val in enumerate([m_name, m_time, m_crit]):
        c = row.cells[c_i]
        c.width = [Inches(2.2), Inches(1.5), Inches(2.8)][c_i]
        set_cell_shading(c, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
        set_cell_margins(c, 50, 50, 70, 70)
        p = c.paragraphs[0]
        r = p.add_run(val)
        if c_i == 0:
            r.font.bold = True
        r.font.size = Pt(8.5)

add_p()

add_heading_2("1.9 Stakeholder Register & Power-Interest Analysis")
sh_reg_data = [
    ("SH-01", "Cluster Resource Center Head", "CRC Head / Cluster Admin", "High", "High", "Manage Closely", "Needs real-time cluster attendance, meeting coordination, defaulter tracking, and BEO export.", "Weekly status meetings, demo walkthroughs, and direct feedback channel.", "Weekly review"),
    ("SH-02", "School Principals & Headmasters", "Primary & Secondary School Leads", "High", "High", "Manage Closely", "Require rapid attendance submission, offline sync, clean UI, and GR circular repository.", "Pre-deployment training workshops, user guides, and direct support helpline.", "Daily during pilot"),
    ("SH-03", "Block Education Officer (BEO)", "Sub-District Regulatory Authority", "High", "Low", "Keep Satisfied", "Requires audit-ready, standardized monthly cluster attendance compliance spreadsheets.", "Monthly summary reporting, demonstration of Apache POI compliance export accuracy.", "Monthly audit"),
    ("SH-04", "Students, Parents & Citizens", "Local Village Community", "Low", "Medium", "Keep Informed", "Desire public school directory, facility transparency, and celebration event gallery access.", "Public transparency portal, village education committee showcases.", "Bi-weekly updates"),
    ("SH-05", "Academic Guide & Evaluation Committee", "MITAOE Faculty Evaluators", "High", "High", "Manage Closely", "Mandate adherence to PMBOK standards, academic rigor, mathematical correctness, and viva defense.", "Bi-weekly sprint reviews, formal project documentation submissions, milestone check-ins.", "Fortnightly"),
    ("SH-06", "Cloud & Tool Vendors (AWS, GitHub)", "Infrastructure Providers", "Low", "Low", "Monitor", "Maintain high availability of hosting services, billing quotas, and API runtime.", "Automated CloudWatch billing alerts, terraform drift detection, and health check monitoring.", "Automated telemetry")
]
tbl_sr = doc.add_table(rows=len(sh_reg_data)+1, cols=6)
tbl_sr.alignment = WD_TABLE_ALIGNMENT.CENTER
sr_hdrs = ["ID", "Stakeholder Name", "Role / Context", "Power", "Interest", "Engagement Strategy & Communication Requirements"]
sr_widths = [Inches(0.6), Inches(1.5), Inches(1.2), Inches(0.6), Inches(0.6), Inches(2.0)]
hdr_sr = tbl_sr.rows[0]
for idx, h_t in enumerate(sr_hdrs):
    c = hdr_sr.cells[idx]
    c.width = sr_widths[idx]
    set_cell_shading(c, "1E3A8A")
    set_cell_margins(c, 50, 50, 50, 50)
    p = c.paragraphs[0]
    r = p.add_run(h_t)
    r.font.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

for idx, r_vals in enumerate(sh_reg_data):
    row = tbl_sr.rows[idx+1]
    row_vals = [r_vals[0], r_vals[1], r_vals[2], r_vals[3], r_vals[4], f"{r_vals[5]} Strategy: {r_vals[7]} ({r_vals[8]})."]
    for c_i, val in enumerate(row_vals):
        c = row.cells[c_i]
        c.width = sr_widths[c_i]
        set_cell_shading(c, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
        set_cell_margins(c, 40, 40, 50, 50)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(8)
        if c_i in [0, 1]:
            r.font.bold = True

add_p()

# Embed Diagram 1: Stakeholder Power-Interest Matrix
add_heading_2("1.10 Visual Stakeholder Power-Interest Matrix")
sh_img = os.path.join(diag_dir, "stakeholder_matrix.png")
if os.path.exists(sh_img):
    doc.add_picture(sh_img, width=Inches(5.8))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 1.1: Stakeholder Power-Interest Matrix (PMBOK Guide 7th Edition)")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = MUTED_TEXT

doc.add_page_break()

# -------------------------------------------------------------
# SECTION 2: WORK BREAKDOWN STRUCTURE (WBS)
# -------------------------------------------------------------
add_heading_1("2. Work Breakdown Structure (WBS) - 100% Rule Compliance")
add_p(
    "The WBS represents a deliverable-oriented hierarchical decomposition of the total scope of work to be carried out "
    "by the project team. The WBS encompasses 100% of the work defined by the project scope and captures all internal, "
    "external, and interim deliverables."
)

# Embed Diagram 2: Scope Hierarchy
add_heading_2("2.1 Project Scope Hierarchy Framework")
scope_img = os.path.join(diag_dir, "scope_hierarchy.png")
if os.path.exists(scope_img):
    doc.add_picture(scope_img, width=Inches(6.4))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 2.1: ShalaConnect Project Scope Hierarchy & Architecture Framework")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = MUTED_TEXT

# Embed Diagram 3: WBS Hierarchy
add_heading_2("2.2 Deliverable-Oriented Hierarchical WBS Tree")
wbs_img = os.path.join(diag_dir, "wbs_hierarchy.png")
if os.path.exists(wbs_img):
    doc.add_picture(wbs_img, width=Inches(6.4))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 2.2: Deliverable-Oriented Hierarchical Work Breakdown Structure (100% Rule)")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = MUTED_TEXT

doc.add_page_break()

# -------------------------------------------------------------
# SECTION 3: WBS DICTIONARY SUMMARY
# -------------------------------------------------------------
add_heading_1("3. Detailed WBS Dictionary (21 Work Packages)")
add_p(
    "The WBS Dictionary provides detailed deliverable, activity, and technical scheduling information about each work package "
    "in the WBS. All 21 lowest-level work packages are summarized below (with full granular breakdown available in WBS_Dictionary.xlsx)."
)

# Detailed table of all 21 WPs
wbs_data_21 = [
    ("1.1.1", "Stakeholder Needs Surveys", "3 d", "Project Manager / Analyst", "INR 14,000", "Field survey report with verified operational pain points."),
    ("1.1.2", "SRS Specification & Traceability", "4 d", "Systems Analyst / Tech Lead", "INR 16,000", "Approved IEEE 830-compliant SRS Document v1.0."),
    ("1.1.3", "DPDP Act Compliance Assessment", "3 d", "Security Specialist", "INR 12,000", "DPDP 2023 compliance matrix & privacy policy."),
    ("1.2.1", "Multi-Tenant Data Modeling (PG16)", "4 d", "Database Architect", "INR 20,000", "ER diagram, DDL init.sql, and JPA entity mappings."),
    ("1.2.2", "REST API Specs (OpenAPI 3.0)", "4 d", "Backend Lead Developer", "INR 18,000", "OpenAPI 3.0 specs and Postman API test collection."),
    ("1.2.3", "Responsive UI/UX & Wireframes", "5 d", "UI/UX Designer", "INR 22,000", "Figma interactive prototypes and design system."),
    ("1.2.4", "AWS Cloud Blueprint", "4 d", "Cloud Architect", "INR 18,000", "Cloud architecture topology and Terraform blueprint."),
    ("1.3.1", "Multi-Tenant RBAC & Security", "5 d", "Backend Security Engineer", "INR 22,000", "Spring Security filter chain with HMAC-SHA256 JWT."),
    ("1.3.2", "Attendance Engine & Offline Sync", "7 d", "Full-Stack Developer", "INR 32,000", "Daily attendance module with local caching and auto-sync."),
    ("1.3.3", "BEO Monthly Excel Report Engine", "5 d", "Backend Developer", "INR 24,000", "Server-side Apache POI formatted Excel generator."),
    ("1.3.4", "Circulars Repository & Receipts", "4 d", "Full-Stack Developer", "INR 18,000", "PDF circular upload vault with audit read receipts."),
    ("1.3.5", "Cluster Review Meeting Scheduler", "3 d", "Full-Stack Developer", "INR 16,000", "Meeting scheduling coordinator with RSVP tracking."),
    ("1.3.6", "Events & Multi-Photo Gallery", "4 d", "Full-Stack Developer", "INR 20,000", "Event implementation submission and photo showcase."),
    ("1.3.7", "Dynamic Form Builder & Engine", "6 d", "Senior Developer", "INR 26,000", "Schema-driven dynamic survey builder & export."),
    ("1.3.8", "Public Transparency Portal", "4 d", "Frontend Developer", "INR 18,000", "Unauthenticated UDISE school search directory."),
    ("1.4.1", "Modular AWS Terraform IaC", "5 d", "DevOps Engineer", "INR 28,000", "Terraform modules for VPC, ALB, ECS, RDS, S3, CDN."),
    ("1.4.2", "GitHub Actions CI/CD Automation", "4 d", "DevOps Engineer", "INR 22,000", "Automated GitHub Actions deploy.yml workflow."),
    ("1.4.3", "Performance Tuning & Audit", "3 d", "Security Auditor / Lead", "INR 18,000", "Database composite indexes and OWASP security audit."),
    ("1.5.1", "Automated Test Suite (JUnit)", "4 d", "QA Automation Engineer", "INR 20,000", "Unit, integration, and tenancy boundary test suites."),
    ("1.5.2", "Field Pilot Rollout & UAT", "3 d", "Project Manager / Lead", "INR 14,000", "5-school pilot trial with signed UAT acceptance."),
    ("1.5.3", "Documentation & Handover", "3 d", "Technical Writer / PM", "INR 12,000", "Final academic reports, manuals, and viva pack.")
]

tbl_w_21 = doc.add_table(rows=len(wbs_data_21)+1, cols=6)
tbl_w_21.alignment = WD_TABLE_ALIGNMENT.CENTER
w_hdrs = ["WBS ID", "Work Package Name", "Dur", "Responsible Role", "Cost (INR)", "Primary Deliverable"]
w_w = [Inches(0.7), Inches(2.1), Inches(0.5), Inches(1.4), Inches(0.9), Inches(1.6)]
hdr_w = tbl_w_21.rows[0]
for idx, h_t in enumerate(w_hdrs):
    c = hdr_w.cells[idx]
    c.width = w_w[idx]
    set_cell_shading(c, "1E3A8A")
    set_cell_margins(c, 40, 40, 40, 40)
    p = c.paragraphs[0]
    r = p.add_run(h_t)
    r.font.bold = True
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(255, 255, 255)

for idx, r_val in enumerate(wbs_data_21):
    row = tbl_w_21.rows[idx+1]
    for c_i, val in enumerate(r_val):
        c = row.cells[c_i]
        c.width = w_w[c_i]
        set_cell_shading(c, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
        set_cell_margins(c, 30, 30, 40, 40)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.size = Pt(7.5)
        if c_i == 0:
            r.font.bold = True

add_p()

# Summary statement
add_heading_1("4. Conclusion & Academic Sign-off")
add_p(
    "Assignment 1 establishes the verified project management foundation for ShalaConnect. By formalizing the Project Charter, "
    "decomposing scope under the 100% Rule, and defining all 21 lowest-level work packages with realistic costs and schedules, "
    "this submission creates an unambiguous baseline for Assignment 2 (Activity Network, CPM, Gantt, and Budget S-Curve), "
    "Assignment 3 (Kanban Execution & EVM Control), and Assignment 4 (Risk Management Framework)."
)
add_p(
    "Academic Declaration: I declare that this assignment represents authentic engineering project management work "
    "developed for the B.Tech Computer Engineering program at MITAOE Pune, strictly conforming to PMI PMBOK Guide 7th Edition standards.",
    bold_prefix="Academic Declaration: "
)

add_heading_1("5. Key References (IEEE Format)")
references = [
    "[1] Project Management Institute, A Guide to the Project Management Body of Knowledge (PMBOK Guide), 7th ed. Newtown Square, PA: PMI, 2021.",
    "[2] Project Management Institute, Process Groups: A Practice Guide. Newtown Square, PA: PMI, 2022.",
    "[3] International Organization for Standardization, Guidance on Project Management, ISO Standard 21500:2021, 2021.",
    "[4] Ministry of Human Resource Development, Government of India, National Education Policy 2020 (NEP 2020), New Delhi, 2020.",
    "[5] Ministry of Law and Justice, Government of India, The Digital Personal Data Protection Act, 2023, The Gazette of India, Aug. 2023.",
    "[6] IEEE Computer Society, IEEE Recommended Practice for Software Requirements Specifications, IEEE Std 830-1998, 1998."
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
print(f"Generated 100% English Assignment_1_Editable.docx successfully at {docx_path}!")
