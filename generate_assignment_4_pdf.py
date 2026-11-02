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

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_4_Risk_Management"
pdf_path = os.path.join(base_dir, "Assignment_4_Report.pdf")
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
        self.drawRightString(595 - 54, 842 - 36, "Project Management (PM-401) | Assignment 4")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 842 - 42, 595 - 54, 842 - 42)
        
        # Footer
        self.line(54, 46, 595 - 54, 46)
        self.drawString(54, 34, "ShalaConnect - Risk Management Plan, RBS & Comprehensive Risk Register")
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
story.append(Paragraph("ASSIGNMENT 4: RISK MANAGEMENT PLAN, RISK BREAKDOWN STRUCTURE & COMPREHENSIVE RISK REGISTER", title_style))
story.append(Spacer(1, 10))
story.append(Paragraph("<b>Project: ShalaConnect</b><br/><i>School Education Cluster Administration & Governance Platform</i>", ParagraphStyle('ProjSub', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, textColor=DARK, alignment=1, spaceAfter=25)))

cov_rows = [
    [Paragraph("<b>Course / Curriculum</b>", tbl_cell_bold), Paragraph("Project Management (B.Tech Computer Engineering, Final Year)", tbl_cell)],
    [Paragraph("<b>Candidate Name / Lead</b>", tbl_cell_bold), Paragraph("Yash Sabale", tbl_cell)],
    [Paragraph("<b>Academic Year / Class</b>", tbl_cell_bold), Paragraph("2026-27 | B.Tech Computer Engineering", tbl_cell)],
    [Paragraph("<b>Department & Institute</b>", tbl_cell_bold), Paragraph("School of Computer Engineering & Technology, MITAOE Pune", tbl_cell)],
    [Paragraph("<b>Faculty Guide / Evaluator</b>", tbl_cell_bold), Paragraph("Prof. Project Guide / Evaluation Committee", tbl_cell)],
    [Paragraph("<b>Risk Governance Framework</b>", tbl_cell_bold), Paragraph("PMBOK 7th Ed. Compliant 5x5 Matrix & 20-Risk Register (16 Threats + 4 Opps)", tbl_cell)],
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
    [Paragraph("<b>Executive Summary & Risk Governance Statement:</b><br/>"
               "This document formalizes the Risk Management Plan and Master Risk Register for ShalaConnect. "
               "It catalogues 20 project-specific risks (16 threats and 4 opportunities) across a 6-pillar Risk Breakdown Structure (RBS), "
               "evaluates inherent vs. residual scores using a 5x5 Probability-Impact heatmap, establishes actionable mitigation "
               "playbooks for top priority risks, and allocates an INR 41,000 Contingency Reserve.",
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
# 2. RISK MANAGEMENT PLAN & RBS
# =============================================================
story.append(Paragraph("1. Risk Management Framework & Assessment Scoring", h1_style))
story.append(Paragraph(
    "Risk assessment utilizes a standardized 5x5 scoring model where $\\text{Risk Score} = \\text{Probability} \\times \\text{Impact}$ "
    "(Scale: 1 to 25). Prioritization classifies risks into: <b>Critical (15-25)</b>, <b>High (10-14)</b>, <b>Medium (5-9)</b>, "
    "and <b>Low (1-4)</b>. An INR 41,000 Contingency Reserve is dedicated to mitigating identified threats.", body_style
))

story.append(Paragraph("2. Risk Breakdown Structure (RBS)", h1_style))
story.append(Paragraph(
    "The RBS decomposes risk sources across six categories: Technical, Cost, Operational, Security/Legal, Schedule/Resource, "
    "and External/Opportunities.", body_style
))

rbs_img = os.path.join(diag_dir, "risk_breakdown_structure.png")
if os.path.exists(rbs_img):
    story.append(Image(rbs_img, width=6.6*inch, height=3.8*inch))
    story.append(Paragraph("<b>Figure 2.1:</b> ShalaConnect Hierarchical Risk Breakdown Structure (RBS)", ParagraphStyle('Cap1', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(PageBreak())

# =============================================================
# 3. 5x5 PROBABILITY-IMPACT HEATMAP
# =============================================================
story.append(Paragraph("3. 5x5 Probability-Impact (P-I) Heatmap Matrix", h1_style))
story.append(Paragraph(
    "The 5x5 heatmap maps all 20 project risks according to pre-mitigation severity. Critical risks (RSK-01, RSK-05, RSK-10) "
    "demand immediate architectural mitigation to ensure project success.", body_style
))

pi_img = os.path.join(diag_dir, "probability_impact_matrix.png")
if os.path.exists(pi_img):
    story.append(Image(pi_img, width=6.6*inch, height=4.8*inch))
    story.append(Paragraph("<b>Figure 3.1:</b> ShalaConnect 5x5 Probability-Impact Heatmap (16 Threats & 4 Opportunities)", ParagraphStyle('Cap2', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(PageBreak())

# =============================================================
# 4. TOP RISKS & PLAYBOOK DASHBOARD
# =============================================================
story.append(Paragraph("4. Master Risk Register Summary (Representative Priority Risks)", h1_style))

risk_pdf_rows = [
    [Paragraph("ID", tbl_hdr), Paragraph("Risk Title", tbl_hdr), Paragraph("Category", tbl_hdr), Paragraph("Inh PxI", tbl_hdr), Paragraph("Priority", tbl_hdr), Paragraph("Mitigation Strategy", tbl_hdr), Paragraph("Res PxI", tbl_hdr), Paragraph("Owner", tbl_hdr)],
    [Paragraph("RSK-01", tbl_cell_bold), Paragraph("Offline Attendance Sync Conflict", tbl_cell), Paragraph("Technical", tbl_cell), Paragraph("4x4=16", tbl_cell_bold), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("Server timestamp conflict diff & DB unique constraint.", tbl_cell), Paragraph("2x2=4", tbl_cell_bold), Paragraph("Full-Stack Lead", tbl_cell)],
    [Paragraph("RSK-05", tbl_cell_bold), Paragraph("Cross-Tenant Data Leakage", tbl_cell), Paragraph("Security", tbl_cell), Paragraph("3x5=15", tbl_cell_bold), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("Cryptographic JWT claims validation on all REST endpoints.", tbl_cell), Paragraph("1x3=3", tbl_cell_bold), Paragraph("Security Lead", tbl_cell)],
    [Paragraph("RSK-10", tbl_cell_bold), Paragraph("DPDP Act Statutory Non-Compliance", tbl_cell), Paragraph("Legal", tbl_cell), Paragraph("3x5=15", tbl_cell_bold), Paragraph("CRITICAL", tbl_cell_bold), Paragraph("Mandatory AWS Mumbai residency; AES-256 rest encryption.", tbl_cell), Paragraph("1x3=3", tbl_cell_bold), Paragraph("Lead Architect", tbl_cell)],
    [Paragraph("RSK-02", tbl_cell_bold), Paragraph("AWS Infrastructure Cost Overrun", tbl_cell), Paragraph("Cost", tbl_cell), Paragraph("4x3=12", tbl_cell_bold), Paragraph("HIGH", tbl_cell_bold), Paragraph("Serverless Fargate, non-prod single-AZ, AWS billing alerts.", tbl_cell), Paragraph("2x2=4", tbl_cell_bold), Paragraph("DevOps Engineer", tbl_cell)],
    [Paragraph("RSK-04", tbl_cell_bold), Paragraph("Apache POI Heap Exhaustion", tbl_cell), Paragraph("Technical", tbl_cell), Paragraph("3x4=12", tbl_cell_bold), Paragraph("HIGH", tbl_cell_bold), Paragraph("Streaming SXSSFWorkbook 100-row sliding window (<64MB).", tbl_cell), Paragraph("1x3=3", tbl_cell_bold), Paragraph("Backend Dev", tbl_cell)],
    [Paragraph("RSK-11", tbl_cell_bold), Paragraph("Key Developer SPoF", tbl_cell), Paragraph("Resource", tbl_cell), Paragraph("3x4=12", tbl_cell_bold), Paragraph("HIGH", tbl_cell_bold), Paragraph("Modular decoupled code, OpenAPI specs, pair cross-training.", tbl_cell), Paragraph("1x2=2", tbl_cell_bold), Paragraph("Project Manager", tbl_cell)],
    [Paragraph("OPP-17", tbl_cell_bold), Paragraph("PWA Zero-Data Caching", tbl_cell), Paragraph("Technical", tbl_cell), Paragraph("4x3=12", tbl_cell_bold), Paragraph("OPPORTUNITY", tbl_cell_bold), Paragraph("Aggressive Workbox service worker client-side caching.", tbl_cell), Paragraph("4x4=16", tbl_cell_bold), Paragraph("Frontend Lead", tbl_cell)],
    [Paragraph("OPP-19", tbl_cell_bold), Paragraph("AWS Academic Cloud Grant", tbl_cell), Paragraph("Cost", tbl_cell), Paragraph("4x4=16", tbl_cell_bold), Paragraph("OPPORTUNITY", tbl_cell_bold), Paragraph("Apply for $500-$1000 USD AWS Educate cloud grant credits.", tbl_cell), Paragraph("4x4=16", tbl_cell_bold), Paragraph("DevOps Engineer", tbl_cell)]
]
tbl_r_pdf = Table(risk_pdf_rows, colWidths=[40, 110, 52, 44, 60, 105, 38, 48])
r_style = [
    ('BACKGROUND', (0,0), (-1,0), PRIMARY),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 3),
    ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ('BACKGROUND', (0,1), (-1,3), colors.HexColor("#FEE2E2")),
    ('BACKGROUND', (0,4), (-1,6), colors.HexColor("#FFEDD5")),
    ('BACKGROUND', (0,7), (-1,8), colors.HexColor("#DCFCE7")),
]
tbl_r_pdf.setStyle(TableStyle(r_style))
story.append(tbl_r_pdf)

story.append(Spacer(1, 10))

story.append(Paragraph("5. Risk Response & Residual Score Reduction Dashboard", h1_style))
resp_img = os.path.join(diag_dir, "risk_response_dashboard.png")
if os.path.exists(resp_img):
    story.append(Image(resp_img, width=6.6*inch, height=3.6*inch))
    story.append(Paragraph("<b>Figure 5.1:</b> Top Priority Risk Response Playbook & Residual Score Reduction", ParagraphStyle('Cap3', parent=body_style, alignment=1, textColor=colors.HexColor("#64748B"), fontSize=7.5)))

story.append(Spacer(1, 10))

story.append(Paragraph("6. Conclusion & Risk Governance Sign-Off", h1_style))
story.append(Paragraph(
    "Assignment 4 establishes an exhaustive risk governance framework for ShalaConnect. By identifying 20 meaningful "
    "project-specific threats and opportunities, evaluating them via a 5x5 heatmap, and formulating actionable mitigation playbooks, "
    "the project ensures that technical, financial, and regulatory risks are proactively controlled. Post-mitigation residual scores "
    "for all critical risks are reduced to Low/Medium (scores <= 4), confirming project robustness.", body_style
))

doc.build(story, canvasmaker=NumberedCanvas)
print(f"Generated 100% English Assignment_4_Report.pdf at {pdf_path}")
