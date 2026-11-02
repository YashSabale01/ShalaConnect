import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\00_Project_Baseline"
os.makedirs(base_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. GENERATE PROJECT_BASELINE.DOCX (100% ENGLISH)
# -------------------------------------------------------------
doc = docx.Document()

for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)

PRIMARY = RGBColor(27, 54, 93)     # Deep Navy
SECONDARY = RGBColor(180, 83, 9)   # Amber / Gold
DARK_TEXT = RGBColor(30, 41, 59)   # Slate 800
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

def add_header(title, subtitle):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("MIT ACADEMY OF ENGINEERING, PUNE")
    run.font.name = "Calibri"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = PRIMARY
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(4)
    run2 = p2.add_run("School of Computer Engineering & Technology | Academic Year 2026-27\nDepartment Project Management Framework & Central Baseline")
    run2.font.name = "Calibri"
    run2.font.size = Pt(10)
    run2.font.color.rgb = MUTED_TEXT
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p3 = doc.add_paragraph()
    p3.paragraph_format.space_before = Pt(12)
    p3.paragraph_format.space_after = Pt(4)
    run3 = p3.add_run(title)
    run3.font.name = "Calibri"
    run3.font.size = Pt(18)
    run3.font.bold = True
    run3.font.color.rgb = PRIMARY
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p4 = doc.add_paragraph()
    p4.paragraph_format.space_before = Pt(0)
    p4.paragraph_format.space_after = Pt(18)
    run4 = p4.add_run(subtitle)
    run4.font.name = "Calibri"
    run4.font.size = Pt(11)
    run4.font.italic = True
    run4.font.color.rgb = SECONDARY
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER

add_header(
    "PROJECT BASELINE DOCUMENTATION",
    "ShalaConnect - School Education Cluster Administration & Governance Platform"
)

# Metadata Table
meta_tbl = doc.add_table(rows=6, cols=2)
meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Project Title", "ShalaConnect - School Education Cluster Administration & Governance Platform"),
    ("Target Organization Domain", "Cluster Resource Centers (CRC), Maharashtra State Education Dept & District Councils"),
    ("Candidate / Lead Developer", "Yash Sabale (B.Tech Computer Engineering, MITAOE Pune)"),
    ("Academic Term / Course", "2026-27 | Final Year Project Management (PM-401)"),
    ("Baseline Status & Version", "Approved Central Project Baseline v2.0 (Foundation for Assignments 1, 2, 3 & 4)"),
    ("Date of Formal Approval", "October 31, 2026")
]
for i, (k, v) in enumerate(meta_data):
    row = meta_tbl.rows[i]
    cell_k, cell_v = row.cells[0], row.cells[1]
    cell_k.width = Inches(2.3)
    cell_v.width = Inches(4.2)
    set_cell_shading(cell_k, "F1F5F9")
    set_cell_shading(cell_v, "FFFFFF")
    set_cell_margins(cell_k, top=60, bottom=60, left=100, right=100)
    set_cell_margins(cell_v, top=60, bottom=60, left=100, right=100)
    
    pk = cell_k.paragraphs[0]
    pk.paragraph_format.space_before = Pt(2)
    pk.paragraph_format.space_after = Pt(2)
    rk = pk.add_run(k)
    rk.font.name = "Calibri"
    rk.font.size = Pt(9.5)
    rk.font.bold = True
    rk.font.color.rgb = DARK_TEXT

    pv = cell_v.paragraphs[0]
    pv.paragraph_format.space_before = Pt(2)
    pv.paragraph_format.space_after = Pt(2)
    rv = pv.add_run(v)
    rv.font.name = "Calibri"
    rv.font.size = Pt(9.5)
    rv.font.color.rgb = DARK_TEXT

doc.add_paragraph().paragraph_format.space_after = Pt(12)

def add_heading_1(text):
    h = doc.add_heading(text, level=1)
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = PRIMARY
    return h

def add_heading_2(text):
    h = doc.add_heading(text, level=2)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    for r in h.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = SECONDARY
    return h

def add_body_p(text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Calibri"
        rb.font.size = Pt(9.5)
        rb.font.bold = True
        rb.font.color.rgb = DARK_TEXT
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.color.rgb = DARK_TEXT
    return p

# 1. EXECUTIVE SUMMARY & PROJECT DESCRIPTION
add_heading_1("1. Executive Summary & Project Description")
add_body_p(
    "ShalaConnect is an enterprise-grade cloud-native governance and administrative automation platform "
    "specifically designed for primary and secondary education governance across Maharashtra, India. The system bridges the "
    "operational gap between rural School Principals / Headmasters, Cluster Resource Center (CRC) Heads / Cluster Administrators, "
    "Block Education Officers (BEO), and local citizen-parent communities across public school networks."
)
add_body_p(
    "Operating in Maharashtra's decentralized school cluster framework, ShalaConnect digitizes end-to-end CRC operations: "
    "daily multi-tenant student and teacher attendance, automated Government Resolution (GR) policy circular dissemination "
    "with verified read-receipts, monthly BEO compliance reporting in official Excel formats, dynamic survey data collection, "
    "cluster review meetings, school event celebration proof tracking, and a public portal showcasing UDISE-verified school infrastructure."
)

# 2. BUSINESS JUSTIFICATION & STRATEGIC ALIGNMENT
add_heading_1("2. Business Justification & Strategic Alignment")
add_body_p(
    "The Maharashtra State School Education Department administers over 65,000 rural and semi-urban government schools across "
    "thousands of educational clusters. At present, cluster administration suffers from critical structural inefficiencies:",
    "Problem Context: "
)
add_body_p(
    "- Delayed Paper Registers & Data Lag: Attendance and Mid-Day Meal (MDM) headcounts are physically entered into registers and collated manually once a month, causing a 30-day reporting delay and preventing early dropout interventions.\n"
    "- Messaging Group Information Dissipation: Important policy circulars, GRs, and meeting agendas are distributed across informal messaging groups, resulting in loss of compliance traceability, zero audit trails, and missed deadlines.\n"
    "- Rural Connectivity Bottlenecks: Rural schools frequently experience 2G/3G network blackouts, rendering standard web applications unusable and frustrating field headmasters.\n"
    "- Ad-Hoc Data Requests: Emergency data inquiries from District Institutes of Education and Training (DIET) or BEO require headmasters to fill unstandardized forms repeatedly, diverting instructional time into bureaucratic overhead."
)
add_body_p(
    "ShalaConnect aligns directly with the National Education Policy (NEP 2020) and PM-SHRI school modernization standards by establishing "
    "a single-source-of-truth governance portal featuring offline-first local synchronization, automated compliance aggregation, and standardized English-language accessibility.",
    "Strategic Alignment: "
)

# 3. SMART PROJECT OBJECTIVES
add_heading_1("3. SMART Project Objectives")
smart_table_data = [
    ("Specific (S)", "Digitize daily student/teacher attendance across 100% of cluster schools and replace informal messaging circulars with an audit-backed policy circular repository."),
    ("Measurable (M)", "Achieve >= 98% daily attendance submission compliance before 11:00 AM; reduce BEO monthly report generation time from 4 days to < 5 seconds via one-click Excel compilation."),
    ("Achievable (A)", "Deliver an offline-first progressive SPA built on React 18, Spring Boot 21, and PostgreSQL 16 capable of running reliably on low-end 2G/3G rural mobile devices."),
    ("Relevant (R)", "Directly eliminate bureaucratic workload for rural headmasters while empowering CRC Cluster Administrators with real-time cluster compliance dashboards."),
    ("Time-bound (T)", "Complete baseline architecture, development, AWS cloud infrastructure provisioning, and end-to-end validation within a 16-week project execution timeline.")
]
tbl_smart = doc.add_table(rows=len(smart_table_data), cols=2)
tbl_smart.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx, (crit, desc) in enumerate(smart_table_data):
    row = tbl_smart.rows[idx]
    c0, c1 = row.cells[0], row.cells[1]
    c0.width, c1.width = Inches(1.8), Inches(4.7)
    set_cell_shading(c0, "F8FAFC")
    set_cell_shading(c1, "FFFFFF")
    set_cell_margins(c0, 50, 50, 80, 80)
    set_cell_margins(c1, 50, 50, 80, 80)
    p0 = c0.paragraphs[0]
    p0.add_run(crit).font.bold = True
    p1 = c1.paragraphs[0]
    p1.add_run(desc)

# 4. SCOPE & BOUNDARIES
add_heading_1("4. Scope Baseline & Boundaries")
add_heading_2("4.1 In-Scope Deliverables & Capabilities")
add_body_p(
    "1. Multi-Tenant Role-Based Access Control (RBAC): Strict isolation between Cluster Administrator, School Headmasters, and unauthenticated Public citizens.\n"
    "2. Daily Attendance Module: Student and teacher attendance recording, multi-day editing window, offline local caching with auto-sync, and 30-day visual trend analytics.\n"
    "3. BEO Compliance Reporting: Automated Apache POI engine generating formatted .xlsx spreadsheets computing school compliance categorization (Regular, Partial, Defaulter).\n"
    "4. Government Resolutions (GR) Portal: Multi-file PDF uploads up to 20MB, searchable catalog, and persistent headmaster read-receipt tracking.\n"
    "5. Cluster Meeting Coordinator: Hybrid (offline venue / online video conference) scheduling with one-click attendance acknowledgment.\n"
    "6. Event & Celebration Proof Tracker: Cluster-wide celebration announcements, school implementation submissions, and multi-photo cloud storage with gallery previews.\n"
    "7. Dynamic Form Builder & Aggregator: Administrative schema designer (TEXT, NUMBER, SELECT, DATE, CHECKBOX) with multi-row spreadsheet entry and instant Excel aggregation.\n"
    "8. Public School Transparency Portal: UDISE-indexed directory search, school facility cards, and student achievement showcases.\n"
    "9. Production Cloud Infrastructure: 100% Terraform-managed AWS architecture (ECS Fargate, ALB, CloudFront CDN, RDS PostgreSQL Multi-AZ, S3, Route 53) with GitHub Actions CI/CD."
)
add_heading_2("4.2 Out-of-Scope Items (Project Exclusions)")
add_body_p(
    "- Direct financial payroll processing and salary disbursal for school teachers (handled exclusively by State Treasury portals).\n"
    "- Online student fee collection or payment gateway integration (government schools provide free education under RTE Act 2009).\n"
    "- Direct SMS gateway integration (incurring recurring telecom carrier costs; replaced by in-app push/bell notifications).\n"
    "- Native iOS/Android app store publication (replaced by responsive, mobile-first PWA architecture to minimize maintenance overhead)."
)

# 5. STAKEHOLDER MATRIX & TEAM STRUCTURE
add_heading_1("5. Key Stakeholders & Governance Structure")
sh_data = [
    ("Cluster Resource Center Head / Admin", "Internal / Primary", "High", "High", "Primary user; requires cluster dashboard, defaulter tracking, meeting scheduling, and report export."),
    ("School Headmasters / Principals", "Internal / Primary", "High", "High", "Field users; require rapid attendance logging, offline support, clean UI, and GR circular access."),
    ("Block Education Officer (BEO)", "External / Governance", "High", "Medium", "Regulatory consumer; requires punctual, audit-ready monthly cluster attendance compliance exports."),
    ("Students, Parents & Citizens", "External / Public", "Low", "Medium", "Public transparency consumers; access school profiles, UDISE stats, and event photo galleries."),
    ("Academic Evaluation Committee (MITAOE)", "Academic / Evaluator", "High", "High", "Evaluates project management rigor, PMBOK standards, architecture, and live defense."),
    ("Project Engineering Team", "Internal / Execution", "High", "High", "Responsible for end-to-end full-stack development, cloud deployment, and quality assurance.")
]
tbl_sh = doc.add_table(rows=len(sh_data)+1, cols=5)
tbl_sh.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Stakeholder Role", "Classification", "Power", "Interest", "Core Expectation / Strategy"]
widths = [Inches(1.8), Inches(1.1), Inches(0.7), Inches(0.7), Inches(2.2)]

hdr_row = tbl_sh.rows[0]
for idx, h_text in enumerate(headers):
    c = hdr_row.cells[idx]
    c.width = widths[idx]
    set_cell_shading(c, "1E3A8A")
    set_cell_margins(c, 60, 60, 60, 60)
    p = c.paragraphs[0]
    r = p.add_run(h_text)
    r.font.name = "Calibri"
    r.font.size = Pt(9)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

for idx, (role, cls, pwr, intr, strat) in enumerate(sh_data):
    row = tbl_sh.rows[idx+1]
    for c_idx, val in enumerate([role, cls, pwr, intr, strat]):
        c = row.cells[c_idx]
        c.width = widths[c_idx]
        set_cell_shading(c, "F8FAFC" if idx % 2 == 1 else "FFFFFF")
        set_cell_margins(c, 50, 50, 60, 60)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        if c_idx == 0:
            r.font.bold = True

# 6. TECHNOLOGIES & INFRASTRUCTURE
add_heading_1("6. Technology Stack & Resource Baseline")
add_body_p(
    "- Application Backend: Java 21 LTS, Spring Boot 3.2.3 (Spring Security, Spring Data JPA, Apache POI 5.2.5, JJWT 0.12.3, Lombok).\n"
    "- Frontend Client: React 18.2, Vite 5.1, Tailwind CSS 3.4, Lucide React, Recharts 2.12, Axios 1.6.\n"
    "- Database Layer: PostgreSQL 16 Relational Engine with UUID and Pgcrypto extensions, indexed on school tenancy and date ranges.\n"
    "- Cloud Infrastructure (AWS): ECS Fargate (Serverless Containers), Application Load Balancer (ALB), CloudFront CDN (TLS 1.3), S3 (Static Assets & Documents), Amazon RDS PostgreSQL (Multi-AZ Private Subnet), Route 53 DNS.\n"
    "- DevOps & IaC: Terraform >= 1.5.0 (Declarative Modular Infrastructure), Docker multi-stage builds, GitHub Actions automated CI/CD pipeline."
)

# 7. PROJECT SCHEDULE & BUDGET BASELINE SUMMARY
add_heading_1("7. Schedule & Budget Baseline Summary")
add_body_p(
    "- Planned Duration: 16 Weeks (4 Calendar Months / 112 Days / 80 Working Days), spanning Requirements Analysis, Architecture, Core Development, AWS Cloud Infrastructure Provisioning, QA Testing, and Academic Submission.\n"
    "- Total Cost Baseline: INR 4,10,000 (USD 4,940), structured through bottom-up work package estimation.\n"
    "- Total Approved Project Budget: INR 4,85,000 (USD 5,850), including Contingency Reserve (INR 41,000) and Management Reserve (INR 34,000).",
    "Project Parameters: "
)

budget_summary_data = [
    ("Direct Personnel & Development Costs", "INR 3,40,000", "70.1%", "Full-Stack Development, Architecture, UI/UX Design & Testing"),
    ("Cloud Infrastructure & Hosting (AWS)", "INR 42,000", "8.7%", "ECS Fargate, RDS PostgreSQL, CloudFront CDN, S3, ALB, Route 53"),
    ("Software Tools, Licenses & Security Audits", "INR 28,000", "5.8%", "Domain Registration, SSL Certificates, SonarQube, GitHub Actions"),
    ("Cost Baseline (Aggregated Work Packages)", "INR 4,10,000", "84.5%", "Sum of all planned direct and operational expenditures"),
    ("Contingency Reserve (Identified Risks - 10%)", "INR 41,000", "8.5%", "Allocated to mitigate technical, network and integration risks"),
    ("Management Reserve (Unforeseen Changes - 8.3%)", "INR 34,000", "7.0%", "Reserved under PM/Sponsor authority for unexpected regulatory scope"),
    ("Total Project Budget", "INR 4,85,000", "100.0%", "Total approved financial baseline for ShalaConnect")
]
tbl_bgt = doc.add_table(rows=len(budget_summary_data)+1, cols=4)
tbl_bgt.alignment = WD_TABLE_ALIGNMENT.CENTER
bgt_headers = ["Budget Category", "Amount (INR)", "Share (%)", "Description & Allocation Basis"]
bgt_widths = [Inches(2.5), Inches(1.1), Inches(0.9), Inches(2.0)]

hdr_bgt = tbl_bgt.rows[0]
for idx, h_text in enumerate(bgt_headers):
    c = hdr_bgt.cells[idx]
    c.width = bgt_widths[idx]
    set_cell_shading(c, "1E3A8A")
    set_cell_margins(c, 60, 60, 60, 60)
    p = c.paragraphs[0]
    r = p.add_run(h_text)
    r.font.name = "Calibri"
    r.font.size = Pt(9)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

for idx, (cat, amt, pct, dsc) in enumerate(budget_summary_data):
    row = tbl_bgt.rows[idx+1]
    is_summary = "Baseline" in cat or "Total" in cat
    bg_col = "FEF3C7" if "Total" in cat else ("F1F5F9" if is_summary else ("FFFFFF" if idx%2==0 else "F8FAFC"))
    for c_idx, val in enumerate([cat, amt, pct, dsc]):
        c = row.cells[c_idx]
        c.width = bgt_widths[c_idx]
        set_cell_shading(c, bg_col)
        set_cell_margins(c, 50, 50, 60, 60)
        p = c.paragraphs[0]
        r = p.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        if is_summary:
            r.font.bold = True

doc.save(os.path.join(base_dir, "Project_Baseline.docx"))
print("Generated 100% English Project_Baseline.docx successfully!")

# -------------------------------------------------------------
# 2. GENERATE PROJECT_ASSUMPTIONS.XLSX (100% ENGLISH)
# -------------------------------------------------------------
wb_assumptions = openpyxl.Workbook()
ws_assump = wb_assumptions.active
ws_assump.title = "Assumptions & Constraints"

font_hdr = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
fill_hdr = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
border_thin = Border(left=Side(style='thin', color='CBD5E1'),
                     right=Side(style='thin', color='CBD5E1'),
                     top=Side(style='thin', color='CBD5E1'),
                     bottom=Side(style='thin', color='CBD5E1'))

assump_headers = ["ID", "Category", "Type", "Statement", "Impact on Schedule / Cost / Quality", "Owner / Validation Strategy"]
ws_assump.append(assump_headers)
for col_idx in range(1, len(assump_headers) + 1):
    cell = ws_assump.cell(row=1, column=col_idx)
    cell.font = font_hdr
    cell.fill = fill_hdr
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

assumptions_rows = [
    ("A-01", "Technical", "Assumption", "Target rural headmasters operate standard Android smartphones with modern Chromium-based browsers.", "Ensures React PWA functions smoothly without requiring legacy Polyfills.", "Full-Stack Lead"),
    ("A-02", "Infrastructure", "Assumption", "AWS cloud services (Fargate, RDS, CloudFront, S3) will maintain standard >= 99.9% uptime SLA.", "Zero architecture re-engineering required for redundant secondary cloud provider.", "DevOps Engineer"),
    ("A-03", "Connectivity", "Assumption", "Network dead-zones in remote villages are intermittent; devices reconnect to internet at least once in 24 hours.", "Validates offline local storage attendance queuing and flush-on-reconnect logic.", "QA Specialist"),
    ("A-04", "User Experience", "Assumption", "Headmasters possess basic digital smartphone literacy and familiarity with digital messaging apps.", "Justifies intuitive UI layout, high-contrast visual cues, and responsive icon design.", "UI/UX Designer"),
    ("A-05", "Data Source", "Assumption", "Cluster Resource Center provides authentic school UDISE codes and registered teacher tallies during initial seeding.", "Eliminates need for manual field surveys to verify baseline school data.", "Project Manager"),
    ("C-01", "Financial", "Constraint", "Total project expenditure cannot exceed the approved cap of INR 4,85,000.", "Requires strict weekly cost monitoring and serverless AWS resource auto-pausing.", "Project Manager"),
    ("C-02", "Schedule", "Constraint", "System must achieve full operational production readiness within the hard 16-week academic window.", "Critical path activities must strictly adhere to zero negative float.", "Project Manager"),
    ("C-03", "Regulatory", "Constraint", "All student and school data must comply with Indian Digital Personal Data Protection (DPDP) Act 2023.", "Requires data residency within AWS Asia Pacific (Mumbai) ap-south-1 region.", "Lead Architect"),
    ("C-04", "Security", "Constraint", "Multi-tenant attendance updates must enforce strict cryptographic JWT token tenancy checks.", "Zero horizontal privilege escalation permitted between schools.", "Security Lead"),
    ("C-05", "Data Integrity", "Constraint", "Platform must enforce relational foreign key cascading and deterministic unique constraints on (school_id, attendance_date).", "Prevents duplicate attendance submissions and ensures reliable audit logs.", "Database Architect")
]

for row_idx, r_data in enumerate(assumptions_rows, start=2):
    ws_assump.append(r_data)
    fill_row = PatternFill(start_color="F8FAFC" if row_idx % 2 == 1 else "FFFFFF", fill_type="solid")
    for col_idx in range(1, len(r_data) + 1):
        cell = ws_assump.cell(row=row_idx, column=col_idx)
        cell.font = Font(name="Calibri", size=10)
        cell.fill = fill_row
        cell.border = border_thin
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if col_idx in [1, 2, 3]:
            cell.alignment = Alignment(horizontal="center", vertical="center")

col_widths = [8, 14, 12, 45, 38, 20]
for idx, w in enumerate(col_widths, start=1):
    ws_assump.column_dimensions[get_column_letter(idx)].width = w

wb_assumptions.save(os.path.join(base_dir, "Project_Assumptions.xlsx"))
print("Generated 100% English Project_Assumptions.xlsx successfully!")

# -------------------------------------------------------------
# 3. GENERATE TRACEABILITY_MATRIX.XLSX (100% ENGLISH)
# -------------------------------------------------------------
wb_trace = openpyxl.Workbook()
ws_trace = wb_trace.active
ws_trace.title = "Scope Traceability Matrix"

trace_headers = [
    "Requirement ID", "Business Objective", "Scope Component / Feature", 
    "Assignment 1 (WBS Package)", "Assignment 2 (Activity ID)", 
    "Assignment 3 (Kanban Module & RACI)", "Assignment 4 (Risk Identifier)", 
    "Verification / Acceptance Criteria"
]
ws_trace.append(trace_headers)
for col_idx in range(1, len(trace_headers) + 1):
    cell = ws_trace.cell(row=1, column=col_idx)
    cell.font = font_hdr
    cell.fill = fill_hdr
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

trace_data = [
    ("REQ-01", "OBJ-1 (Attendance)", "Daily Attendance & Tenancy Validation", "WBS 1.3.2: Attendance Engine", "ACT-09", "Task KB-04 (Headmaster - R, Admin - A)", "RSK-01 (Offline Sync Conflict)", "Verified HMAC JWT token rejects foreign school submissions; offline queue flushes upon connection."),
    ("REQ-02", "OBJ-2 (Compliance)", "BEO Monthly Excel Cluster Report Export", "WBS 1.3.3: Analytics & Reporting", "ACT-10", "Task KB-06 (Full-Stack - R, PM - A)", "RSK-04 (Apache POI Memory Leak)", "Generates standardized .xlsx for 50+ schools in < 5 seconds with zero server memory degradation."),
    ("REQ-03", "OBJ-1 (Circulars)", "Circular Repository & Read-Receipts", "WBS 1.3.4: Policy & GR Center", "ACT-11", "Task KB-08 (Backend - R, Admin - A)", "RSK-05 (PDF S3 Upload Exhaustion)", "20MB PDF upload, SHA-256 validation, and persistent seen timestamp recorded for every headmaster."),
    ("REQ-04", "OBJ-3 (Meetings)", "Cluster Review Meeting Coordination", "WBS 1.3.5: Meeting Management", "ACT-12", "Task KB-09 (Frontend - R, Admin - A)", "RSK-08 (Meeting Reschedule Lag)", "Real-time acknowledgment tally and instant calendar sync across headmaster dashboard."),
    ("REQ-05", "OBJ-3 (Events)", "Event Celebration Proof Tracker", "WBS 1.3.6: Events & Galleries", "ACT-13", "Task KB-11 (Full-Stack - R, Guide - I)", "RSK-07 (Image Storage Spike)", "Multi-photo upload with thumbnail generation and public photo gallery inspection."),
    ("REQ-06", "OBJ-4 (Surveys)", "Dynamic Schema Form Builder", "WBS 1.3.7: Dynamic Form Engine", "ACT-14", "Task KB-12 (Backend - R, Admin - A)", "RSK-03 (JSON Schema Incompatibility)", "Support for TEXT, NUMBER, SELECT, DATE; multi-row entry and aggregated tabular Excel download."),
    ("REQ-07", "OBJ-5 (Cloud & IaC)", "Terraform Modular AWS Provisioning", "WBS 1.4.1: Cloud Infrastructure", "ACT-16", "Task KB-15 (DevOps - R, PM - A)", "RSK-02 (AWS Cost Overrun)", "Terraform plan/apply executes cleanly, provisioning VPC, ALB, ECS Fargate, RDS, and CloudFront."),
    ("REQ-08", "OBJ-5 (CI/CD)", "Automated GitHub Actions Pipeline", "WBS 1.4.2: CI/CD Pipeline", "ACT-17", "Task KB-16 (DevOps - R, PM - A)", "RSK-06 (Deployment Pipeline Breakage)", "Git push to main builds Spring Boot ECR container and Vite SPA, syncing S3 & ECS in < 6 minutes."),
    ("REQ-09", "OBJ-4 (UI/UX)", "Responsive Web UI & Dashboard", "WBS 1.2.3: UI/UX & Wireframes", "ACT-06", "Task KB-03 (UI Lead - R, PM - A)", "RSK-09 (Design Usability Defect)", "100% UI elements seamlessly render across desktop and mobile devices without horizontal overflow.")
]

for row_idx, r_data in enumerate(trace_data, start=2):
    ws_trace.append(r_data)
    fill_row = PatternFill(start_color="F8FAFC" if row_idx % 2 == 1 else "FFFFFF", fill_type="solid")
    for col_idx in range(1, len(r_data) + 1):
        cell = ws_trace.cell(row=row_idx, column=col_idx)
        cell.font = Font(name="Calibri", size=9.5)
        cell.fill = fill_row
        cell.border = border_thin
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if col_idx in [1, 2, 4, 5, 7]:
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

trace_col_widths = [14, 18, 28, 24, 20, 26, 22, 38]
for idx, w in enumerate(trace_col_widths, start=1):
    ws_trace.column_dimensions[get_column_letter(idx)].width = w

wb_trace.save(os.path.join(base_dir, "Traceability_Matrix.xlsx"))
print("Generated 100% English Traceability_Matrix.xlsx successfully!")
