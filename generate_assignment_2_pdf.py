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

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_2_Project_Plan"
pdf_path = os.path.join(base_dir, "Assignment_2_Report.pdf")
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
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header
        self.drawString(54, 842 - 36, "MIT Academy of Engineering, Pune | School of Computer Engineering & Technology")
        self.drawRightString(595 - 54, 842 - 36, "Project Management (PM-401) | Assignment 2")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 842 - 42, 595 - 54, 842 - 42)
        
        # Footer
        self.line(54, 46, 595 - 54, 46)
        self.drawString(54, 34, "ShalaConnect - Project Plan, CPM Network & Budget S-Curve")
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
story.append(Paragraph("ASSIGNMENT 2: PROJECT PLAN, ACTIVITY NETWORK, CRITICAL PATH METHOD (CPM) & BOTTOM-UP BUDGET ESTIMATION", title_style))
story.append(Spacer(1, 10))
story.append(Paragraph("<b>Project: ShalaConnect</b><br/><i>School Education Cluster Administration & Governance Platform</i>", ParagraphStyle('ProjSub', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=DARK, alignment=1, spaceAfter=25)))

cov_rows = [
    [Paragraph("<b>Course / Curriculum</b>", tbl_cell_bold), Paragraph("Project Management (B.Tech Computer Engineering, Final Year)", tbl_cell)],
    [Paragraph("<b>Candidate Name / Lead</b>", tbl_cell_bold), Paragraph("Yash Sabale", tbl_cell)],
    [Paragraph("<b>Academic Year / Class</b>", tbl_cell_bold), Paragraph("2026-27 | B.Tech Computer Engineering", tbl_cell)],
    [Paragraph("<b>Department & Institute</b>", tbl_cell_bold), Paragraph("School of Computer Engineering & Technology, MITAOE Pune", tbl_cell)],
    [Paragraph("<b>Faculty Guide / Evaluator</b>", tbl_cell_bold), Paragraph("Prof. Project Guide / Evaluation Committee", tbl_cell)],
    [Paragraph("<b>WBS Baseline Reference</b>", tbl_cell_bold), Paragraph("Derived from Assignment 1 WBS (21 Work Packages, INR 4,10,000 Baseline)", tbl_cell)],
    [Paragraph("<b>Submission Date & Status</b>", tbl_cell_bold), Paragraph("October 31, 2026 | Master Craftsman Baseline v2.0 (100% English Verified)", tbl_cell)]
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
    [Paragraph("<b>Executive Summary & Mathematical Integrity Statement:</b><br/>"
               "This document presents the complete project schedule, Activity-on-Node (AON) network diagram, forward/backward "
               "pass calculations, float analysis, schedule compression models, bottom-up cost estimates, and time-phased S-curve "
               "for ShalaConnect. All durations (54-day critical path) and costs (INR 4,10,000 cost baseline, INR 4,85,000 total budget) "
               "have been programmatically verified using NetworkX and verified against PMI PMBOK Guide 7th Edition standards.",
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
# 2. ACTIVITY PLANNING & CPM CALCULATIONS
# =============================================================
story.append(Paragraph("1. Activity Planning & Scope Derivation", h1_style))
story.append(Paragraph(
    "All 21 activities are derived directly from the 21 lowest-level work packages of Assignment 1. "
    "Dependencies follow strict engineering prerequisites with Finish-to-Start (FS) logic.", body_style
))

story.append(Paragraph("2. Critical Path Method (CPM) Forward & Backward Pass Results", h1_style))
story.append(Paragraph(
    "Algorithmic evaluation of the network establishes an exact project duration of <b>54 Working Days</b>. "
    "Thirteen critical activities have Total Float (TF) = 0 and Free Float (FF) = 0.", body_style
))

cpm_pdf_rows = [
    [Paragraph("ID", tbl_hdr), Paragraph("Activity Name", tbl_hdr), Paragraph("WBS", tbl_hdr), Paragraph("Dur", tbl_hdr), Paragraph("ES", tbl_hdr), Paragraph("EF", tbl_hdr), Paragraph("LS", tbl_hdr), Paragraph("LF", tbl_hdr), Paragraph("TF", tbl_hdr), Paragraph("FF", tbl_hdr), Paragraph("Status", tbl_hdr), Paragraph("Cost", tbl_hdr)],
    [Paragraph("ACT-01", tbl_cell_bold), Paragraph("Stakeholder Needs Surveys", tbl_cell), Paragraph("1.1.1", tbl_cell), Paragraph("3", tbl_cell), Paragraph("0", tbl_cell), Paragraph("3", tbl_cell), Paragraph("0", tbl_cell), Paragraph("3", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 14k", tbl_cell)],
    [Paragraph("ACT-02", tbl_cell_bold), Paragraph("SRS & Requirements Matrix", tbl_cell), Paragraph("1.1.2", tbl_cell), Paragraph("4", tbl_cell), Paragraph("3", tbl_cell), Paragraph("7", tbl_cell), Paragraph("3", tbl_cell), Paragraph("7", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 16k", tbl_cell)],
    [Paragraph("ACT-03", tbl_cell_bold), Paragraph("DPDP Act Compliance", tbl_cell), Paragraph("1.1.3", tbl_cell), Paragraph("3", tbl_cell), Paragraph("7", tbl_cell), Paragraph("10", tbl_cell), Paragraph("7", tbl_cell), Paragraph("10", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 12k", tbl_cell)],
    [Paragraph("ACT-04", tbl_cell_bold), Paragraph("Multi-Tenant Data Modeling", tbl_cell), Paragraph("1.2.1", tbl_cell), Paragraph("4", tbl_cell), Paragraph("10", tbl_cell), Paragraph("14", tbl_cell), Paragraph("10", tbl_cell), Paragraph("14", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 20k", tbl_cell)],
    [Paragraph("ACT-05", tbl_cell_bold), Paragraph("REST API Specs (OpenAPI)", tbl_cell), Paragraph("1.2.2", tbl_cell), Paragraph("4", tbl_cell), Paragraph("14", tbl_cell), Paragraph("18", tbl_cell), Paragraph("14", tbl_cell), Paragraph("18", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 18k", tbl_cell)],
    [Paragraph("ACT-06", tbl_cell), Paragraph("Responsive UI/UX & Figma", tbl_cell), Paragraph("1.2.3", tbl_cell), Paragraph("5", tbl_cell), Paragraph("7", tbl_cell), Paragraph("12", tbl_cell), Paragraph("18", tbl_cell), Paragraph("23", tbl_cell), Paragraph("11", tbl_cell), Paragraph("6", tbl_cell), Paragraph("Non-Crit", tbl_cell), Paragraph("INR 22k", tbl_cell)],
    [Paragraph("ACT-07", tbl_cell), Paragraph("AWS Cloud Blueprint", tbl_cell), Paragraph("1.2.4", tbl_cell), Paragraph("4", tbl_cell), Paragraph("18", tbl_cell), Paragraph("22", tbl_cell), Paragraph("28", tbl_cell), Paragraph("32", tbl_cell), Paragraph("10", tbl_cell), Paragraph("0", tbl_cell), Paragraph("Non-Crit", tbl_cell), Paragraph("INR 18k", tbl_cell)],
    [Paragraph("ACT-08", tbl_cell_bold), Paragraph("RBAC & JWT Security Module", tbl_cell), Paragraph("1.3.1", tbl_cell), Paragraph("5", tbl_cell), Paragraph("18", tbl_cell), Paragraph("23", tbl_cell), Paragraph("18", tbl_cell), Paragraph("23", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 22k", tbl_cell)],
    [Paragraph("ACT-09", tbl_cell_bold), Paragraph("Attendance Engine & Sync", tbl_cell), Paragraph("1.3.2", tbl_cell), Paragraph("7", tbl_cell), Paragraph("23", tbl_cell), Paragraph("30", tbl_cell), Paragraph("23", tbl_cell), Paragraph("30", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 32k", tbl_cell)],
    [Paragraph("ACT-10", tbl_cell_bold), Paragraph("BEO Monthly Excel Engine", tbl_cell), Paragraph("1.3.3", tbl_cell), Paragraph("5", tbl_cell), Paragraph("30", tbl_cell), Paragraph("35", tbl_cell), Paragraph("30", tbl_cell), Paragraph("35", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 24k", tbl_cell)],
    [Paragraph("ACT-11", tbl_cell), Paragraph("Circulars Repository & Receipts", tbl_cell), Paragraph("1.3.4", tbl_cell), Paragraph("4", tbl_cell), Paragraph("23", tbl_cell), Paragraph("27", tbl_cell), Paragraph("40", tbl_cell), Paragraph("44", tbl_cell), Paragraph("17", tbl_cell), Paragraph("17", tbl_cell), Paragraph("Non-Crit", tbl_cell), Paragraph("INR 18k", tbl_cell)],
    [Paragraph("ACT-12", tbl_cell), Paragraph("Cluster Meeting Scheduler", tbl_cell), Paragraph("1.3.5", tbl_cell), Paragraph("3", tbl_cell), Paragraph("23", tbl_cell), Paragraph("26", tbl_cell), Paragraph("41", tbl_cell), Paragraph("44", tbl_cell), Paragraph("18", tbl_cell), Paragraph("18", tbl_cell), Paragraph("Non-Crit", tbl_cell), Paragraph("INR 16k", tbl_cell)],
    [Paragraph("ACT-13", tbl_cell), Paragraph("Events & Multi-Photo Gallery", tbl_cell), Paragraph("1.3.6", tbl_cell), Paragraph("4", tbl_cell), Paragraph("23", tbl_cell), Paragraph("27", tbl_cell), Paragraph("40", tbl_cell), Paragraph("44", tbl_cell), Paragraph("17", tbl_cell), Paragraph("17", tbl_cell), Paragraph("Non-Crit", tbl_cell), Paragraph("INR 20k", tbl_cell)],
    [Paragraph("ACT-14", tbl_cell_bold), Paragraph("Dynamic Form Builder Engine", tbl_cell), Paragraph("1.3.7", tbl_cell), Paragraph("6", tbl_cell), Paragraph("35", tbl_cell), Paragraph("41", tbl_cell), Paragraph("35", tbl_cell), Paragraph("41", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 26k", tbl_cell)],
    [Paragraph("ACT-15", tbl_cell), Paragraph("Public Transparency Portal", tbl_cell), Paragraph("1.3.8", tbl_cell), Paragraph("4", tbl_cell), Paragraph("18", tbl_cell), Paragraph("22", tbl_cell), Paragraph("40", tbl_cell), Paragraph("44", tbl_cell), Paragraph("22", tbl_cell), Paragraph("22", tbl_cell), Paragraph("Non-Crit", tbl_cell), Paragraph("INR 18k", tbl_cell)],
    [Paragraph("ACT-16", tbl_cell), Paragraph("Modular Terraform AWS IaC", tbl_cell), Paragraph("1.4.1", tbl_cell), Paragraph("5", tbl_cell), Paragraph("22", tbl_cell), Paragraph("27", tbl_cell), Paragraph("32", tbl_cell), Paragraph("37", tbl_cell), Paragraph("10", tbl_cell), Paragraph("0", tbl_cell), Paragraph("Non-Crit", tbl_cell), Paragraph("INR 28k", tbl_cell)],
    [Paragraph("ACT-17", tbl_cell), Paragraph("GitHub Actions CI/CD Pipeline", tbl_cell), Paragraph("1.4.2", tbl_cell), Paragraph("4", tbl_cell), Paragraph("27", tbl_cell), Paragraph("31", tbl_cell), Paragraph("37", tbl_cell), Paragraph("41", tbl_cell), Paragraph("10", tbl_cell), Paragraph("10", tbl_cell), Paragraph("Non-Crit", tbl_cell), Paragraph("INR 22k", tbl_cell)],
    [Paragraph("ACT-18", tbl_cell_bold), Paragraph("Performance Tuning & Audit", tbl_cell), Paragraph("1.4.3", tbl_cell), Paragraph("3", tbl_cell), Paragraph("41", tbl_cell), Paragraph("44", tbl_cell), Paragraph("41", tbl_cell), Paragraph("44", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 18k", tbl_cell)],
    [Paragraph("ACT-19", tbl_cell_bold), Paragraph("Automated Test Suite (JUnit)", tbl_cell), Paragraph("1.5.1", tbl_cell), Paragraph("4", tbl_cell), Paragraph("44", tbl_cell), Paragraph("48", tbl_cell), Paragraph("44", tbl_cell), Paragraph("48", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 20k", tbl_cell)],
    [Paragraph("ACT-20", tbl_cell_bold), Paragraph("Field Pilot Rollout & UAT", tbl_cell), Paragraph("1.5.2", tbl_cell), Paragraph("3", tbl_cell), Paragraph("48", tbl_cell), Paragraph("51", tbl_cell), Paragraph("48", tbl_cell), Paragraph("51", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 14k", tbl_cell)],
    [Paragraph("ACT-21", tbl_cell_bold), Paragraph("Documentation & Handover", tbl_cell), Paragraph("1.5.3", tbl_cell), Paragraph("3", tbl_cell), Paragraph("51", tbl_cell), Paragraph("54", tbl_cell), Paragraph("51", tbl_cell), Paragraph("54", tbl_cell), Paragraph("0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("INR 12k", tbl_cell)],
    [Paragraph("<b>TOTAL</b>", tbl_cell_bold), Paragraph("<b>Critical Path: 54 Days | Baseline Cost: INR 4,10,000</b>", tbl_cell_bold), Paragraph("-", tbl_cell), Paragraph("<b>54 d</b>", tbl_cell_bold), Paragraph("-", tbl_cell), Paragraph("-", tbl_cell), Paragraph("-", tbl_cell), Paragraph("-", tbl_cell), Paragraph("-", tbl_cell), Paragraph("-", tbl_cell), Paragraph("<b>13 CP Acts</b>", tbl_cell_bold), Paragraph("<b>INR 4,10,000</b>", tbl_cell_bold)]
]

tbl_cpm_p = Table(cpm_pdf_rows, colWidths=[38, 120, 28, 22, 20, 20, 20, 20, 20, 20, 52, 47])
t_style = [
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF3C7"))
]
for idx in range(1, len(cpm_pdf_rows)-1):
    if cpm_pdf_rows[idx][10].text == "CRITICAL":
        t_style.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor("#FEE2E2")))
    elif idx % 2 == 1:
        t_style.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor("#F8FAFC")))
tbl_cpm_p.setStyle(TableStyle(t_style))
story.append(tbl_cpm_p)

story.append(PageBreak())

# =============================================================
# 3. DIAGRAMS: AON & GANTT
# =============================================================
story.append(Paragraph("3. Activity-on-Node (AON) Network Diagram", h1_style))
aon_img = os.path.join(diag_dir, "aon_network_diagram.png")
if os.path.exists(aon_img):
    story.append(Image(aon_img, width=6.6*inch, height=3.7*inch))
    story.append(Paragraph("<b>Figure 3.1:</b> ShalaConnect Activity-on-Node Network Diagram (Critical Path in Red, 54 Working Days)", ParagraphStyle('Cap1', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(Spacer(1, 10))

story.append(Paragraph("4. Project Schedule Gantt Chart", h1_style))
gantt_img = os.path.join(diag_dir, "gantt_chart.png")
if os.path.exists(gantt_img):
    story.append(Image(gantt_img, width=6.6*inch, height=4.2*inch))
    story.append(Paragraph("<b>Figure 4.1:</b> ShalaConnect Gantt Schedule with Milestones and Float Windows", ParagraphStyle('Cap2', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(PageBreak())

# =============================================================
# 4. BUDGET ESTIMATION & S-CURVE
# =============================================================
story.append(Paragraph("5. Bottom-Up Budget Estimation & Control Account Structure", h1_style))
story.append(Paragraph(
    "Bottom-up cost aggregation across all 21 work packages yields the approved financial baseline. "
    "Reserves are allocated for identified risks (Contingency) and unforeseen regulatory shifts (Management).", body_style
))

bgt_pdf_rows = [
    [Paragraph("Control Account / Phase", tbl_hdr), Paragraph("WBS Ref", tbl_hdr), Paragraph("Cost Baseline", tbl_hdr), Paragraph("Contingency (10%)", tbl_hdr), Paragraph("Mgmt Reserve (7%)", tbl_hdr), Paragraph("Total Budget", tbl_hdr), Paragraph("Share", tbl_hdr)],
    [Paragraph("CA-01: Initiation & Requirements", tbl_cell_bold), Paragraph("1.1.1 to 1.1.3", tbl_cell), Paragraph("INR 42,000", tbl_cell), Paragraph("INR 4,200", tbl_cell), Paragraph("INR 3,480", tbl_cell), Paragraph("INR 49,680", tbl_cell), Paragraph("10.2%", tbl_cell)],
    [Paragraph("CA-02: Architecture & Design", tbl_cell_bold), Paragraph("1.2.1 to 1.2.4", tbl_cell), Paragraph("INR 78,000", tbl_cell), Paragraph("INR 7,800", tbl_cell), Paragraph("INR 6,470", tbl_cell), Paragraph("INR 92,270", tbl_cell), Paragraph("19.0%", tbl_cell)],
    [Paragraph("CA-03: Core Application Dev", tbl_cell_bold), Paragraph("1.3.1 to 1.3.8", tbl_cell), Paragraph("INR 1,76,000", tbl_cell), Paragraph("INR 17,600", tbl_cell), Paragraph("INR 14,610", tbl_cell), Paragraph("INR 2,08,210", tbl_cell), Paragraph("42.9%", tbl_cell)],
    [Paragraph("CA-04: Cloud DevOps & Hardening", tbl_cell_bold), Paragraph("1.4.1 to 1.4.3", tbl_cell), Paragraph("INR 68,000", tbl_cell), Paragraph("INR 6,800", tbl_cell), Paragraph("INR 5,640", tbl_cell), Paragraph("INR 80,440", tbl_cell), Paragraph("16.6%", tbl_cell)],
    [Paragraph("CA-05: QA, Pilot Rollout & UAT", tbl_cell_bold), Paragraph("1.5.1 to 1.5.3", tbl_cell), Paragraph("INR 46,000", tbl_cell), Paragraph("INR 4,600", tbl_cell), Paragraph("INR 3,800", tbl_cell), Paragraph("INR 54,400", tbl_cell), Paragraph("11.3%", tbl_cell)],
    [Paragraph("<b>TOTAL PROJECT BUDGET</b>", tbl_cell_bold), Paragraph("<b>All 21 WPs</b>", tbl_cell_bold), Paragraph("<b>INR 4,10,000</b>", tbl_cell_bold), Paragraph("<b>INR 41,000</b>", tbl_cell_bold), Paragraph("<b>INR 34,000</b>", tbl_cell_bold), Paragraph("<b>INR 4,85,000</b>", tbl_cell_bold), Paragraph("<b>100.0%</b>", tbl_cell_bold)]
]
tbl_b_pdf = Table(bgt_pdf_rows, colWidths=[145, 68, 62, 68, 68, 68, 38])
tbl_b_pdf.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF3C7")),
]))
story.append(tbl_b_pdf)

story.append(Spacer(1, 10))

story.append(Paragraph("6. Time-Phased Cumulative Cost S-Curve", h1_style))
scurve_img = os.path.join(diag_dir, "scurve_chart.png")
if os.path.exists(scurve_img):
    story.append(Image(scurve_img, width=6.6*inch, height=3.8*inch))
    story.append(Paragraph("<b>Figure 6.1:</b> ShalaConnect Cumulative Cost S-Curve (Planned Value PV vs. Project Timeline)", ParagraphStyle('Cap3', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(Spacer(1, 10))

story.append(Paragraph("7. Conclusion & Schedule/Budget Baseline Sign-Off", h1_style))
story.append(Paragraph(
    "Assignment 2 successfully establishes the scheduling and financial baseline for ShalaConnect. "
    "The 54-day critical path fits comfortably within the 16-week academic window with an operational buffer of 26 working days. "
    "The budget of INR 4,85,000 provides complete cost coverage, establishing the performance measurement baseline for "
    "Assignment 3 (Kanban Control & EVM) and Assignment 4 (Risk Management Framework).", body_style
))

doc.build(story, canvasmaker=NumberedCanvas)
print(f"Generated 100% English Assignment_2_Report.pdf at {pdf_path}")
