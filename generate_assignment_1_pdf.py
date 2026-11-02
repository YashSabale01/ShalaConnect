import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.pdfgen import canvas

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_1_WBS"
pdf_path = os.path.join(base_dir, "Assignment_1_Report.pdf")
diag_dir = os.path.join(base_dir, "Diagrams")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on cover page
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header
        self.drawString(54, 842 - 36, "MIT Academy of Engineering, Pune | School of Computer Engineering & Technology")
        self.drawRightString(595 - 54, 842 - 36, "Project Management (PM-401) | Assignment 1")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 842 - 42, 595 - 54, 842 - 42)
        
        # Footer
        self.line(54, 46, 595 - 54, 46)
        self.drawString(54, 34, "ShalaConnect - Project Charter, WBS & WBS Dictionary Baseline")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(595 - 54, 34, page_str)
        self.restoreState()

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    leftMargin=54,
    rightMargin=54,
    topMargin=54,
    bottomMargin=54
)

styles = getSampleStyleSheet()

PRIMARY = colors.HexColor("#1E3A8A")
SECONDARY = colors.HexColor("#B45309")
DARK = colors.HexColor("#1E293B")
BORDER_COLOR = colors.HexColor("#CBD5E1")

title_style = ParagraphStyle(
    'CoverTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=17,
    leading=21,
    textColor=PRIMARY,
    alignment=1,
    spaceAfter=8
)

inst_style = ParagraphStyle(
    'CoverInst',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=16,
    textColor=PRIMARY,
    alignment=1,
    spaceAfter=4
)

sub_inst_style = ParagraphStyle(
    'CoverSubInst',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor("#475569"),
    alignment=1,
    spaceAfter=20
)

h1_style = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12.5,
    leading=16,
    textColor=PRIMARY,
    spaceBefore=14,
    spaceAfter=6,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10.5,
    leading=14,
    textColor=SECONDARY,
    spaceBefore=10,
    spaceAfter=4,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'Body_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=11.5,
    textColor=DARK,
    spaceBefore=2,
    spaceAfter=4
)

bullet_style = ParagraphStyle(
    'Bullet_Custom',
    parent=body_style,
    leftIndent=12,
    firstLineIndent=-8,
    spaceBefore=1,
    spaceAfter=2
)

tbl_cell = ParagraphStyle('TCell', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=DARK)
tbl_cell_bold = ParagraphStyle('TCellBold', parent=tbl_cell, fontName='Helvetica-Bold')
tbl_hdr = ParagraphStyle('THdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white, alignment=1)

story = []

# =============================================================
# 1. COVER PAGE
# =============================================================
story.append(Spacer(1, 20))
story.append(Paragraph("MAEER's MIT ACADEMY OF ENGINEERING, PUNE", inst_style))
story.append(Paragraph("(An Autonomous Institute Affiliated to Savitribai Phule Pune University)<br/>School of Computer Engineering & Technology | Academic Year: 2026-27", sub_inst_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=4, spaceAfter=20))

story.append(Paragraph("COURSE SUBMISSION: PROJECT MANAGEMENT (PM-401)", ParagraphStyle('SubSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=SECONDARY, alignment=1, spaceAfter=8)))
story.append(Paragraph("ASSIGNMENT 1: PROJECT CHARTER, WORK BREAKDOWN STRUCTURE (WBS) & WBS DICTIONARY", title_style))
story.append(Spacer(1, 10))
story.append(Paragraph("<b>Project: ShalaConnect</b><br/><i>School Education Cluster Administration & Governance Platform</i>", ParagraphStyle('ProjSub', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=DARK, alignment=1, spaceAfter=25)))

cov_rows = [
    [Paragraph("<b>Course / Curriculum</b>", tbl_cell_bold), Paragraph("Project Management (B.Tech Computer Engineering, Final Year)", tbl_cell)],
    [Paragraph("<b>Candidate Name / Lead</b>", tbl_cell_bold), Paragraph("Yash Sabale", tbl_cell)],
    [Paragraph("<b>Academic Year / Class</b>", tbl_cell_bold), Paragraph("2026-27 | B.Tech Computer Engineering", tbl_cell)],
    [Paragraph("<b>Institutional Department</b>", tbl_cell_bold), Paragraph("School of Computer Engineering & Technology, MITAOE Pune", tbl_cell)],
    [Paragraph("<b>Faculty Guide / Evaluator</b>", tbl_cell_bold), Paragraph("Prof. Project Guide / Evaluation Committee", tbl_cell)],
    [Paragraph("<b>Target Governance Sector</b>", tbl_cell_bold), Paragraph("Cluster Resource Centers (CRC), Maharashtra State Education Dept", tbl_cell)],
    [Paragraph("<b>Submission Date & Status</b>", tbl_cell_bold), Paragraph("October 31, 2026 | Master Baseline v2.0 (100% English Verified)", tbl_cell)]
]
cov_tbl = Table(cov_rows, colWidths=[150, 337])
cov_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F1F5F9")),
    ('BACKGROUND', (1,0), (1,-1), colors.white),
    ('GRID', (0,0), (-1,-1), 0.6, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(cov_tbl)
story.append(Spacer(1, 40))

summary_box = [
    [Paragraph("<b>Executive Summary & Academic Integrity Statement:</b><br/>"
               "This document represents the comprehensive Project Charter, hierarchical Work Breakdown Structure "
               "complying with the 100% Rule, and 21-work-package WBS Dictionary for ShalaConnect. "
               "All deliverables, timelines (16 weeks), budget estimates (INR 4,85,000), and resource assignments have been "
               "customized to the actual software architecture and formatted strictly in English for academic submission at MITAOE Pune.",
               ParagraphStyle('Box', parent=body_style, fontSize=8, leading=11, textColor=colors.HexColor("#334155")))]
]
b_tbl = Table(summary_box, colWidths=[487])
b_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D97706")),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
]))
story.append(b_tbl)

story.append(PageBreak())

# =============================================================
# 2. SECTION 1: PROJECT CHARTER
# =============================================================
story.append(Paragraph("1. Comprehensive Project Charter (PMBOK Guide 7th Edition)", h1_style))
story.append(Paragraph(
    "The Project Charter formally authorizes the existence of the ShalaConnect project and establishes the project manager's "
    "authority to utilize institutional and cloud resources. This section provides the exhaustive 18-point charter customized "
    "to the primary education cluster governance ecosystem.", body_style
))

story.append(Paragraph("1.1 Project Identification and Overview", h2_style))
story.append(Paragraph(
    "<b>Project Title:</b> ShalaConnect - School Education Cluster Administration & Governance Platform<br/>"
    "<b>Project Code:</b> MITAOE-PM-2026-SC01 | <b>Academic Term:</b> 2026-27 B.Tech Capstone<br/>"
    "<b>Project Manager:</b> Yash Sabale (Lead Developer & Consultant)<br/>"
    "<b>Baseline Life Cycle:</b> 16 Calendar Weeks (80 Working Days / 112 Calendar Days)<br/>"
    "<b>Approved Financial Baseline:</b> INR 4,85,000 (including contingency and management reserves)", body_style
))

story.append(Paragraph("1.2 Background and Business Justification", h2_style))
story.append(Paragraph(
    "In Maharashtra's decentralized primary education system, government schools are grouped into administrative clusters "
    "known as Resource Clusters, led by a Cluster Resource Center (CRC) Head / Administrator. A typical cluster oversees "
    "20 to 50 rural schools. Key business justifications for ShalaConnect include:", body_style
))
story.append(Paragraph("- <b>Elimination of 30-Day Reporting Lag:</b> Replaces physical paper attendance registers with real-time digital logging, enabling early dropout intervention.", bullet_style))
story.append(Paragraph("- <b>Replacement of Informal Messaging Channels:</b> Eliminates unverified circulars by establishing an audit-backed policy circular repository with read-receipts.", bullet_style))
story.append(Paragraph("- <b>Automated BEO Monthly Compliance:</b> Compresses 4-day manual survey compilation into sub-second Apache POI Excel report exports for Block Education Officers.", bullet_style))
story.append(Paragraph("- <b>Citizen & Parent Transparency:</b> Empowers local communities with a public portal displaying UDISE-verified school infrastructure and achievements.", bullet_style))

story.append(Paragraph("1.3 SMART Project Objectives", h2_style))
smart_rows = [
    [Paragraph("SMART Dimension", tbl_hdr), Paragraph("Project Objective Specification & Target", tbl_hdr)],
    [Paragraph("<b>Specific (S)</b>", tbl_cell_bold), Paragraph("Digitize daily student/teacher attendance across 100% of cluster schools; replace informal messaging circulars with an audit-backed repository.", tbl_cell)],
    [Paragraph("<b>Measurable (M)</b>", tbl_cell_bold), Paragraph("Achieve >= 98% daily attendance submission compliance before 11:00 AM; reduce BEO monthly report generation time to < 5 seconds.", tbl_cell)],
    [Paragraph("<b>Achievable (A)</b>", tbl_cell_bold), Paragraph("Deliver an offline-first progressive SPA built on React 18, Spring Boot 21, and PostgreSQL 16 capable of running on rural 2G/3G devices.", tbl_cell)],
    [Paragraph("<b>Relevant (R)</b>", tbl_cell_bold), Paragraph("Directly eliminate administrative burden for rural headmasters while empowering CRC Administrators with live compliance dashboards.", tbl_cell)],
    [Paragraph("<b>Time-bound (T)</b>", tbl_cell_bold), Paragraph("Complete baseline architecture, development, AWS cloud infrastructure provisioning, and end-to-end validation within 16 weeks.", tbl_cell)]
]
tbl_sm = Table(smart_rows, colWidths=[100, 387])
tbl_sm.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(tbl_sm)

story.append(Paragraph("1.4 Dynamic Stakeholder Register & Power-Interest Classification", h2_style))
sh_rows = [
    [Paragraph("ID", tbl_hdr), Paragraph("Stakeholder", tbl_hdr), Paragraph("Power", tbl_hdr), Paragraph("Interest", tbl_hdr), Paragraph("Strategy", tbl_hdr), Paragraph("Communication & Engagement Mode", tbl_hdr)],
    [Paragraph("SH-01", tbl_cell), Paragraph("<b>CRC Administrator</b>", tbl_cell), Paragraph("High", tbl_cell), Paragraph("High", tbl_cell), Paragraph("Manage Closely", tbl_cell), Paragraph("Weekly reviews, dashboard walkthroughs, direct mobile feedback channel.", tbl_cell)],
    [Paragraph("SH-02", tbl_cell), Paragraph("<b>School Headmasters</b>", tbl_cell), Paragraph("High", tbl_cell), Paragraph("High", tbl_cell), Paragraph("Manage Closely", tbl_cell), Paragraph("Pre-deployment workshops, standardized user guides, support helpline.", tbl_cell)],
    [Paragraph("SH-03", tbl_cell), Paragraph("<b>Block Edu Officer (BEO)</b>", tbl_cell), Paragraph("High", tbl_cell), Paragraph("Low", tbl_cell), Paragraph("Keep Satisfied", tbl_cell), Paragraph("Monthly audit-ready Excel reports, compliance accuracy demos.", tbl_cell)],
    [Paragraph("SH-04", tbl_cell), Paragraph("<b>Parents & Public</b>", tbl_cell), Paragraph("Low", tbl_cell), Paragraph("Med", tbl_cell), Paragraph("Keep Informed", tbl_cell), Paragraph("Public transparency portal, school achievements and photo galleries.", tbl_cell)],
    [Paragraph("SH-05", tbl_cell), Paragraph("<b>Academic Guide (MITAOE)</b>", tbl_cell), Paragraph("High", tbl_cell), Paragraph("High", tbl_cell), Paragraph("Manage Closely", tbl_cell), Paragraph("Bi-weekly sprint reviews, formal project documentation, milestone check-ins.", tbl_cell)],
    [Paragraph("SH-06", tbl_cell), Paragraph("<b>Cloud Vendors (AWS)</b>", tbl_cell), Paragraph("Low", tbl_cell), Paragraph("Low", tbl_cell), Paragraph("Monitor", tbl_cell), Paragraph("Automated CloudWatch billing alerts, Terraform drift monitoring.", tbl_cell)]
]
tbl_sh_pdf = Table(sh_rows, colWidths=[36, 110, 42, 42, 75, 182])
tbl_sh_pdf.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
]))
story.append(tbl_sh_pdf)

story.append(Spacer(1, 10))

# Embed Diagram: Stakeholder Matrix
sh_img = os.path.join(diag_dir, "stakeholder_matrix.png")
if os.path.exists(sh_img):
    story.append(Image(sh_img, width=6.2*inch, height=4.8*inch))
    story.append(Paragraph("<b>Figure 1.1:</b> Stakeholder Power-Interest Matrix (PMBOK Guide 7th Edition Standards)", ParagraphStyle('Cap1', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(PageBreak())

# =============================================================
# 3. SECTION 2: WBS & ARCHITECTURAL DIAGRAMS
# =============================================================
story.append(Paragraph("2. Work Breakdown Structure (WBS) & Scope Framework", h1_style))
story.append(Paragraph(
    "The ShalaConnect WBS is a deliverable-oriented hierarchical decomposition of the project scope adhering strictly to the "
    "<b>100% Rule</b> (PMBOK Guide 7th Edition). The sum of child work packages under each phase equals exactly 100% of the parent scope.", body_style
))

# Embed Scope Diagram
scope_img = os.path.join(diag_dir, "scope_hierarchy.png")
if os.path.exists(scope_img):
    story.append(Image(scope_img, width=6.6*inch, height=4.1*inch))
    story.append(Paragraph("<b>Figure 2.1:</b> ShalaConnect Project Scope Hierarchy & Architecture Framework", ParagraphStyle('Cap2', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(Spacer(1, 10))

# Embed WBS Hierarchy Diagram
wbs_img = os.path.join(diag_dir, "wbs_hierarchy.png")
if os.path.exists(wbs_img):
    story.append(Image(wbs_img, width=6.6*inch, height=4.1*inch))
    story.append(Paragraph("<b>Figure 2.2:</b> Deliverable-Oriented Hierarchical Work Breakdown Structure (100% Rule)", ParagraphStyle('Cap3', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(PageBreak())

# =============================================================
# 4. SECTION 3: WBS DICTIONARY MASTER TABLE
# =============================================================
story.append(Paragraph("3. Detailed WBS Dictionary (21 Work Packages Summary)", h1_style))
story.append(Paragraph(
    "The WBS Dictionary defines the definitive scope boundaries, duration, resource ownership, and cost baselines for all 21 work packages.", body_style
))

wbs_summary_rows = [
    [Paragraph("WBS", tbl_hdr), Paragraph("Work Package Name", tbl_hdr), Paragraph("Dur", tbl_hdr), Paragraph("Responsible Role", tbl_hdr), Paragraph("Cost (INR)", tbl_hdr), Paragraph("Primary Deliverable", tbl_hdr)],
    [Paragraph("1.1.1", tbl_cell_bold), Paragraph("Stakeholder Needs Surveys", tbl_cell), Paragraph("3 d", tbl_cell), Paragraph("Project Manager / Analyst", tbl_cell), Paragraph("INR 14,000", tbl_cell), Paragraph("Field survey report & pain points matrix.", tbl_cell)],
    [Paragraph("1.1.2", tbl_cell_bold), Paragraph("SRS & Requirements Matrix", tbl_cell), Paragraph("4 d", tbl_cell), Paragraph("Systems Analyst / Tech Lead", tbl_cell), Paragraph("INR 16,000", tbl_cell), Paragraph("IEEE 830-compliant SRS Document v1.0.", tbl_cell)],
    [Paragraph("1.1.3", tbl_cell_bold), Paragraph("DPDP Act Compliance", tbl_cell), Paragraph("3 d", tbl_cell), Paragraph("Security Specialist", tbl_cell), Paragraph("INR 12,000", tbl_cell), Paragraph("DPDP 2023 compliance & privacy matrix.", tbl_cell)],
    [Paragraph("1.2.1", tbl_cell_bold), Paragraph("Multi-Tenant Data Model (PG16)", tbl_cell), Paragraph("4 d", tbl_cell), Paragraph("Database Architect", tbl_cell), Paragraph("INR 20,000", tbl_cell), Paragraph("ERD, SQL DDL init.sql, and JPA entities.", tbl_cell)],
    [Paragraph("1.2.2", tbl_cell_bold), Paragraph("REST API Specs (OpenAPI 3.0)", tbl_cell), Paragraph("4 d", tbl_cell), Paragraph("Backend Lead Developer", tbl_cell), Paragraph("INR 18,000", tbl_cell), Paragraph("OpenAPI 3.0 spec & Postman collections.", tbl_cell)],
    [Paragraph("1.2.3", tbl_cell_bold), Paragraph("Responsive UI/UX & Wireframes", tbl_cell), Paragraph("5 d", tbl_cell), Paragraph("UI/UX Designer", tbl_cell), Paragraph("INR 22,000", tbl_cell), Paragraph("Figma interactive responsive prototypes.", tbl_cell)],
    [Paragraph("1.2.4", tbl_cell_bold), Paragraph("AWS Cloud Blueprint", tbl_cell), Paragraph("4 d", tbl_cell), Paragraph("Cloud Architect", tbl_cell), Paragraph("INR 18,000", tbl_cell), Paragraph("VPC topology & Terraform cloud plan.", tbl_cell)],
    [Paragraph("1.3.1", tbl_cell_bold), Paragraph("Multi-Tenant RBAC & Security", tbl_cell), Paragraph("5 d", tbl_cell), Paragraph("Backend Security Engineer", tbl_cell), Paragraph("INR 22,000", tbl_cell), Paragraph("Spring Security filter chain with JWT.", tbl_cell)],
    [Paragraph("1.3.2", tbl_cell_bold), Paragraph("Attendance Engine & Offline Sync", tbl_cell), Paragraph("7 d", tbl_cell), Paragraph("Full-Stack Developer", tbl_cell), Paragraph("INR 32,000", tbl_cell), Paragraph("Attendance module with local offline cache.", tbl_cell)],
    [Paragraph("1.3.3", tbl_cell_bold), Paragraph("BEO Monthly Excel Report Engine", tbl_cell), Paragraph("5 d", tbl_cell), Paragraph("Backend Developer", tbl_cell), Paragraph("INR 24,000", tbl_cell), Paragraph("Apache POI formatted BEO Excel generator.", tbl_cell)],
    [Paragraph("1.3.4", tbl_cell_bold), Paragraph("Circulars Repository & Receipts", tbl_cell), Paragraph("4 d", tbl_cell), Paragraph("Full-Stack Developer", tbl_cell), Paragraph("INR 18,000", tbl_cell), Paragraph("PDF circular upload & read receipts log.", tbl_cell)],
    [Paragraph("1.3.5", tbl_cell_bold), Paragraph("Cluster Review Meeting Scheduler", tbl_cell), Paragraph("3 d", tbl_cell), Paragraph("Full-Stack Developer", tbl_cell), Paragraph("INR 16,000", tbl_cell), Paragraph("Meeting coordinator & RSVP tracker.", tbl_cell)],
    [Paragraph("1.3.6", tbl_cell_bold), Paragraph("Events & Multi-Photo Gallery", tbl_cell), Paragraph("4 d", tbl_cell), Paragraph("Full-Stack Developer", tbl_cell), Paragraph("INR 20,000", tbl_cell), Paragraph("Event proof upload & public photo grid.", tbl_cell)],
    [Paragraph("1.3.7", tbl_cell_bold), Paragraph("Dynamic Form Builder & Engine", tbl_cell), Paragraph("6 d", tbl_cell), Paragraph("Senior Developer", tbl_cell), Paragraph("INR 26,000", tbl_cell), Paragraph("Dynamic survey builder & Excel export.", tbl_cell)],
    [Paragraph("1.3.8", tbl_cell_bold), Paragraph("Public Transparency Portal", tbl_cell), Paragraph("4 d", tbl_cell), Paragraph("Frontend Developer", tbl_cell), Paragraph("INR 18,000", tbl_cell), Paragraph("Public UDISE school directory search.", tbl_cell)],
    [Paragraph("1.4.1", tbl_cell_bold), Paragraph("Modular AWS Terraform IaC", tbl_cell), Paragraph("5 d", tbl_cell), Paragraph("DevOps Engineer", tbl_cell), Paragraph("INR 28,000", tbl_cell), Paragraph("Terraform modules for ECS, RDS, S3, CDN.", tbl_cell)],
    [Paragraph("1.4.2", tbl_cell_bold), Paragraph("GitHub Actions CI/CD Automation", tbl_cell), Paragraph("4 d", tbl_cell), Paragraph("DevOps Engineer", tbl_cell), Paragraph("INR 22,000", tbl_cell), Paragraph("Automated GitHub Actions deploy pipeline.", tbl_cell)],
    [Paragraph("1.4.3", tbl_cell_bold), Paragraph("Performance Tuning & Audit", tbl_cell), Paragraph("3 d", tbl_cell), Paragraph("Security Auditor / Lead", tbl_cell), Paragraph("INR 18,000", tbl_cell), Paragraph("Database composite indexing & OWASP scan.", tbl_cell)],
    [Paragraph("1.5.1", tbl_cell_bold), Paragraph("Automated Test Suite (JUnit)", tbl_cell), Paragraph("4 d", tbl_cell), Paragraph("QA Automation Engineer", tbl_cell), Paragraph("INR 20,000", tbl_cell), Paragraph("Automated unit & tenancy test suites.", tbl_cell)],
    [Paragraph("1.5.2", tbl_cell_bold), Paragraph("Field Pilot Rollout & UAT", tbl_cell), Paragraph("3 d", tbl_cell), Paragraph("Project Manager / Lead", tbl_cell), Paragraph("INR 14,000", tbl_cell), Paragraph("5-school pilot trial with signed UAT.", tbl_cell)],
    [Paragraph("1.5.3", tbl_cell_bold), Paragraph("Documentation & Handover", tbl_cell), Paragraph("3 d", tbl_cell), Paragraph("Technical Writer / PM", tbl_cell), Paragraph("INR 12,000", tbl_cell), Paragraph("Final project documentation & viva deck.", tbl_cell)],
    [Paragraph("<b>TOTAL</b>", tbl_cell_bold), Paragraph("<b>Cost Baseline (21 Work Packages)</b>", tbl_cell_bold), Paragraph("<b>80 d</b>", tbl_cell_bold), Paragraph("<b>Full Project Team</b>", tbl_cell_bold), Paragraph("<b>INR 4,10,000</b>", tbl_cell_bold), Paragraph("<b>Complete Platform Baseline</b>", tbl_cell_bold)]
]

tbl_wbs_p = Table(wbs_summary_rows, colWidths=[38, 142, 28, 110, 57, 112])
w_style = [
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF3C7"))
]
for idx in range(1, len(wbs_summary_rows)-1):
    if idx % 2 == 1:
        w_style.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor("#F8FAFC")))
tbl_wbs_p.setStyle(TableStyle(w_style))
story.append(tbl_wbs_p)

story.append(Spacer(1, 10))

story.append(Paragraph("4. Conclusion & Baseline Traceability", h1_style))
story.append(Paragraph(
    "Assignment 1 establishes the verified project management foundation for ShalaConnect. By formalizing the Project Charter, "
    "decomposing scope under the 100% Rule, and defining all 21 lowest-level work packages with realistic costs and schedules, "
    "this submission creates an unambiguous baseline for Assignment 2 (Activity Network, CPM, Gantt, and Budget S-Curve), "
    "Assignment 3 (Kanban Execution & EVM Control), and Assignment 4 (Risk Management Framework).", body_style
))
story.append(Paragraph(
    "<b>Declaration of Authorship:</b> I declare that this assignment represents authentic academic project management work "
    "developed for the B.Tech Computer Engineering program at MITAOE Pune, strictly conforming to PMI PMBOK Guide 7th Edition standards.", body_style
))

doc.build(story, canvasmaker=NumberedCanvas)
print(f"Generated 100% English Assignment_1_Report.pdf at {pdf_path}")
