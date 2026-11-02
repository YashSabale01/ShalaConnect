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

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_3_Kanban_Control"
pdf_path = os.path.join(base_dir, "Assignment_3_Report.pdf")
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
        self.drawRightString(595 - 54, 842 - 36, "Project Management (PM-401) | Assignment 3")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 842 - 42, 595 - 54, 842 - 42)
        
        # Footer
        self.line(54, 46, 595 - 54, 46)
        self.drawString(54, 34, "ShalaConnect - Kanban Board, RACI Matrix & EVM Control Plan")
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
    fontSize=16,
    leading=20,
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
    fontSize=12,
    leading=15,
    textColor=PRIMARY,
    spaceBefore=14,
    spaceAfter=6,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
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
story.append(Paragraph("ASSIGNMENT 3: KANBAN BOARD, EXECUTION CONTROL PLAN, RACI MATRIX & EARNED VALUE MANAGEMENT (EVM)", title_style))
story.append(Spacer(1, 10))
story.append(Paragraph("<b>Project: ShalaConnect</b><br/><i>School Education Cluster Administration & Governance Platform</i>", ParagraphStyle('ProjSub', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=DARK, alignment=1, spaceAfter=25)))

cov_rows = [
    [Paragraph("<b>Course / Curriculum</b>", tbl_cell_bold), Paragraph("Project Management (B.Tech Computer Engineering, Final Year)", tbl_cell)],
    [Paragraph("<b>Candidate Name / Lead</b>", tbl_cell_bold), Paragraph("Yash Sabale", tbl_cell)],
    [Paragraph("<b>Academic Year / Class</b>", tbl_cell_bold), Paragraph("2026-27 | B.Tech Computer Engineering", tbl_cell)],
    [Paragraph("<b>Department & Institute</b>", tbl_cell_bold), Paragraph("School of Computer Engineering & Technology, MITAOE Pune", tbl_cell)],
    [Paragraph("<b>Faculty Guide / Evaluator</b>", tbl_cell_bold), Paragraph("Prof. Project Guide / Evaluation Committee", tbl_cell)],
    [Paragraph("<b>Interactive Functional Artifact</b>", tbl_cell_bold), Paragraph("Standalone Web-Based Kanban Application with Dynamic EVM Engine", tbl_cell)],
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
    [Paragraph("<b>Executive Summary & Execution Control Statement:</b><br/>"
               "This submission details the operational execution management system for ShalaConnect. It encompasses a functional "
               "5-column Kanban dashboard with WIP limits and Little's Law flow metrics, a single-accountability RACI matrix "
               "covering all 21 WBS packages, an execution control plan, and a mathematically verified Earned Value Management (EVM) "
               "engine with Day 35 snapshot analysis (CPI = 1.05, SPI = 0.93, EAC = INR 3,90,476).",
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
# 2. KANBAN ARCHITECTURE & WORKFLOW
# =============================================================
story.append(Paragraph("1. Functional Kanban Board Architecture & Lean Flow", h1_style))
story.append(Paragraph(
    "ShalaConnect operationalizes Agile Lean execution through a 5-column Kanban workflow (Backlog, To Do, In Progress, "
    "Testing/Review, Done). Work in Progress (WIP) limits enforce flow efficiency by preventing multitasking bottlenecks. "
    "The complete functional web application is provided in <code>Kanban_Dashboard/Source_Code/index.html</code>.", body_style
))

kanban_img = os.path.join(diag_dir, "kanban_workflow_diagram.png")
if os.path.exists(kanban_img):
    story.append(Image(kanban_img, width=6.6*inch, height=3.3*inch))
    story.append(Paragraph("<b>Figure 1.1:</b> ShalaConnect Kanban Process Flow with WIP Limits and Flow Metrics", ParagraphStyle('Cap1', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(Spacer(1, 8))

story.append(Paragraph("2. Kanban Lean Process Metrics & Flow Calculations", h1_style))
story.append(Paragraph(
    "• <b>Lead Time:</b> Average 11.2 Days from Backlog initiation to production deployment in Done.<br/>"
    "• <b>Cycle Time:</b> Average 4.8 Days of active development from In Progress to Done.<br/>"
    "• <b>Throughput:</b> 3.5 completed work packages per week (0.7 packages per working day).<br/>"
    "• <b>Little's Law Validation:</b> $\\text{WIP} = \\text{Throughput} \\times \\text{Cycle Time} = 0.7 \\times 4.8 = 3.36$ tasks, validating observed WIP stability.<br/>"
    "• <b>Flow Efficiency:</b> $(4.8 / 11.2) \\times 100 = 42.8\\%$, exceeding standard industry benchmarks.", body_style
))

story.append(PageBreak())

# =============================================================
# 3. RACI RESPONSIBILITY ASSIGNMENT MATRIX
# =============================================================
story.append(Paragraph("3. RACI Responsibility Assignment Matrix", h1_style))
story.append(Paragraph(
    "The RACI matrix governs all 21 WBS work packages under the strict PMBOK Single-Accountability Rule: exactly one role "
    "is designated Accountable (A) per deliverable, preventing conflicting decision authority.", body_style
))

raci_img = os.path.join(diag_dir, "raci_matrix_diagram.png")
if os.path.exists(raci_img):
    story.append(Image(raci_img, width=6.6*inch, height=4.1*inch))
    story.append(Paragraph("<b>Figure 3.1:</b> ShalaConnect RACI Matrix (R = Responsible, A = Accountable, C = Consulted, I = Informed)", ParagraphStyle('Cap2', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(PageBreak())

# =============================================================
# 4. EARNED VALUE MANAGEMENT (EVM)
# =============================================================
story.append(Paragraph("4. Earned Value Management (EVM) Performance Tracking", h1_style))
story.append(Paragraph(
    "EVM integrates scope, schedule, and cost performance measurements. A formal project snapshot at Day 35 reveals:", body_style
))

evm_rows = [
    [Paragraph("EVM Parameter / Metric", tbl_hdr), Paragraph("Formula", tbl_hdr), Paragraph("Day 35 Value", tbl_hdr), Paragraph("Performance Interpretation", tbl_hdr)],
    [Paragraph("Budget At Completion (BAC)", tbl_cell_bold), Paragraph("Baseline Sum", tbl_cell), Paragraph("INR 4,10,000", tbl_cell_bold), Paragraph("Total approved Cost Baseline.", tbl_cell)],
    [Paragraph("Planned Value (PV)", tbl_cell_bold), Paragraph("Planned S-Curve", tbl_cell), Paragraph("INR 3,20,000", tbl_cell_bold), Paragraph("Target baseline spend as of Day 35.", tbl_cell)],
    [Paragraph("Earned Value (EV)", tbl_cell_bold), Paragraph("Sum(WP Cost x %)", tbl_cell), Paragraph("INR 2,97,000", tbl_cell_bold), Paragraph("Physical work accomplished value.", tbl_cell)],
    [Paragraph("Actual Cost (AC)", tbl_cell_bold), Paragraph("Direct Expenditures", tbl_cell), Paragraph("INR 2,82,857", tbl_cell_bold), Paragraph("Actual recorded direct expenditure.", tbl_cell)],
    [Paragraph("Cost Variance (CV)", tbl_cell_bold), Paragraph("EV - AC", tbl_cell), Paragraph("+INR 14,143", tbl_cell_bold), Paragraph("Positive = Under Budget (Favorable Savings).", tbl_cell)],
    [Paragraph("Schedule Variance (SV)", tbl_cell_bold), Paragraph("EV - PV", tbl_cell), Paragraph("-INR 23,000", tbl_cell_bold), Paragraph("Negative = Slight Schedule Lag (Absorbable).", tbl_cell)],
    [Paragraph("Cost Performance Index (CPI)", tbl_cell_bold), Paragraph("EV / AC", tbl_cell), Paragraph("1.05", tbl_cell_bold), Paragraph("Achieving INR 1.05 work per INR 1.00 spent.", tbl_cell)],
    [Paragraph("Schedule Performance Index (SPI)", tbl_cell_bold), Paragraph("EV / PV", tbl_cell), Paragraph("0.93", tbl_cell_bold), Paragraph("Progressing at 93% of planned schedule rate.", tbl_cell)],
    [Paragraph("Estimate At Completion (EAC)", tbl_cell_bold), Paragraph("BAC / CPI", tbl_cell), Paragraph("INR 3,90,476", tbl_cell_bold), Paragraph("Projected total cost: INR 19,524 under budget.", tbl_cell)],
    [Paragraph("Variance At Completion (VAC)", tbl_cell_bold), Paragraph("BAC - EAC", tbl_cell), Paragraph("+INR 19,524", tbl_cell_bold), Paragraph("Anticipated cost surplus at project completion.", tbl_cell)]
]
tbl_evm_p = Table(evm_rows, colWidths=[130, 90, 85, 182])
tbl_evm_p.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#DCFCE7")),
    ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#FEF3C7")),
    ('BACKGROUND', (0,7), (-1,7), colors.HexColor("#DCFCE7")),
]))
story.append(tbl_evm_p)

story.append(Spacer(1, 8))

evm_img = os.path.join(diag_dir, "evm_scurve_analysis.png")
if os.path.exists(evm_img):
    story.append(Image(evm_img, width=6.6*inch, height=3.7*inch))
    story.append(Paragraph("<b>Figure 4.1:</b> ShalaConnect Earned Value Management Performance S-Curve (PV, EV, AC, CV, SV, and EAC Forecast)", ParagraphStyle('Cap3', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(Spacer(1, 8))

story.append(Paragraph("5. Conclusion & Baseline Traceability", h1_style))
story.append(Paragraph(
    "Assignment 3 demonstrates complete execution control over ShalaConnect. By combining a functional, interactive Kanban dashboard "
    "with rigorous Lean metrics (Lead Time, Cycle Time, WIP Limits) and PMBOK-standard Earned Value Management (EVM), the project "
    "verifies both operational agility and strict financial governance. At Day 35, the project demonstrates strong cost efficiency "
    "(CPI = 1.05) with minor schedule lag (SPI = 0.93) that is easily absorbed by the 26-day operational buffer.", body_style
))

doc.build(story, canvasmaker=NumberedCanvas)
print(f"Generated 100% English Assignment_3_Report.pdf at {pdf_path}")
