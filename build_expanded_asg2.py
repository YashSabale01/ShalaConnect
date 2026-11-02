import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, NextPageTemplate, HRFlowable
)
from reportlab.pdfgen import canvas

# Institutional Corporate Color Palette
PRIMARY = colors.HexColor("#1B365D")
SECONDARY = colors.HexColor("#2C5282")
ACCENT = colors.HexColor("#D97706")
TEXT_DARK = colors.HexColor("#1A202C")
TEXT_MUTED = colors.HexColor("#4A5568")
BG_LIGHT = colors.HexColor("#F7FAFC")
BG_ALT = colors.HexColor("#EDF2F7")
BORDER_COLOR = colors.HexColor("#CBD5E0")
WHITE = colors.HexColor("#FFFFFF")
GREEN = colors.HexColor("#059669")
RED = colors.HexColor("#DC2626")

class DynamicCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                w, h = self._pagesize
                self.saveState()
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(SECONDARY)
                self.drawString(54, h - 36, "MIT ACADEMY OF ENGINEERING | PM-401 PROJECT MANAGEMENT (2026-27)")
                self.setFont("Helvetica", 8)
                self.setFillColor(TEXT_MUTED)
                self.drawRightString(w - 54, h - 36, "ShalaConnect Governance Platform | Yash Sabale")
                self.setStrokeColor(BORDER_COLOR)
                self.setLineWidth(0.75)
                self.line(54, h - 42, w - 54, h - 42)

                self.line(54, 46, w - 54, 46)
                self.setFont("Helvetica", 8)
                self.drawString(54, 34, "Assignment 2: Project Plan, CPM Network, Critical Path & Budget Baseline | Master Craftsman Tier")
                self.drawRightString(w - 54, 34, f"Page {self._pageNumber} of {num_pages}")
                self.restoreState()
            super().showPage()
        super().save()

def get_doc_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('CoverSubject', fontName='Helvetica-Bold', fontSize=26, leading=30, alignment=1, textColor=PRIMARY))
    styles.add(ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=14, leading=18, alignment=1, textColor=SECONDARY))
    styles.add(ParagraphStyle('CoverMetaL', fontName='Helvetica-Bold', fontSize=10, leading=15, textColor=TEXT_DARK))
    styles.add(ParagraphStyle('CoverMetaV', fontName='Helvetica', fontSize=10, leading=15, textColor=TEXT_DARK))
    styles.add(ParagraphStyle('DocH1', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=PRIMARY, spaceBefore=12, spaceAfter=6, keepWithNext=True))
    styles.add(ParagraphStyle('DocH2', fontName='Helvetica-Bold', fontSize=10.0, leading=13.5, textColor=SECONDARY, spaceBefore=9, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle('DocH3', fontName='Helvetica-Bold', fontSize=9.0, leading=12, textColor=TEXT_DARK, spaceBefore=6, spaceAfter=3, keepWithNext=True))
    styles.add(ParagraphStyle('DocBody', fontName='Helvetica', fontSize=8.5, leading=12, textColor=TEXT_DARK, spaceAfter=5))
    styles.add(ParagraphStyle('DocBullet', fontName='Helvetica', fontSize=8.5, leading=12, textColor=TEXT_DARK, leftIndent=12, spaceAfter=3))
    styles.add(ParagraphStyle('DocCallout', fontName='Helvetica-Oblique', fontSize=8.0, leading=11, textColor=PRIMARY, spaceBefore=3, spaceAfter=4))
    styles.add(ParagraphStyle('DocFormula', fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, alignment=1, textColor=PRIMARY, spaceBefore=4, spaceAfter=4))
    styles.add(ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, alignment=1, textColor=WHITE))
    styles.add(ParagraphStyle('TableCell', fontName='Helvetica', fontSize=7.0, leading=9.0, textColor=TEXT_DARK))
    styles.add(ParagraphStyle('TableCellBold', fontName='Helvetica-Bold', fontSize=7.0, leading=9.0, textColor=TEXT_DARK))
    styles.add(ParagraphStyle('FigureCaption', fontName='Helvetica-Bold', fontSize=8.5, leading=11, alignment=1, textColor=SECONDARY, spaceBefore=6, spaceAfter=10))
    return styles

def build_assignment_2():
    pdf_path = "Project_Management_Submissions/Assignment_2_Project_Plan/Assignment_2_Report.pdf"
    doc = BaseDocTemplate(pdf_path, pagesize=letter)
    p_frame = Frame(54, 54, letter[0]-108, letter[1]-108, id='F_Port')
    l_frame = Frame(54, 54, letter[1]-108, letter[0]-108, id='F_Land')
    doc.addPageTemplates([
        PageTemplate(id='Portrait', frames=p_frame, pagesize=letter),
        PageTemplate(id='Landscape', frames=l_frame, pagesize=(letter[1], letter[0]))
    ])

    styles = get_doc_styles()
    story = []

    # ==========================================
    # COVER PAGE (Minimal, Clean Academic Style - No Top College Header)
    # ==========================================
    story.append(Spacer(1, 140))
    story.append(Paragraph("PROJECT MANAGEMENT", styles['CoverSubject']))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Assignment 2: Project Plan, Critical Path and Budget Estimation", styles['CoverTitle']))

    story.append(Spacer(1, 160))

    meta_rows = [
        [Paragraph("Name:", styles['CoverMetaL']), Paragraph("Yash Janardan Sabale", styles['CoverMetaV'])],
        [Paragraph("PRN:", styles['CoverMetaL']), Paragraph("202301040087", styles['CoverMetaV'])],
        [Paragraph("Branch:", styles['CoverMetaL']), Paragraph("Computer Engineering", styles['CoverMetaV'])],
        [Paragraph("Academic Year:", styles['CoverMetaL']), Paragraph("2026-27", styles['CoverMetaV'])],
        [Paragraph("College:", styles['CoverMetaL']), Paragraph("MIT Academy of Engineering, Alandi, Pune", styles['CoverMetaV'])],
    ]
    t_meta = Table(meta_rows, colWidths=[110, 260], hAlign='CENTER')
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # ==========================================
    # CHAPTER 1: SCHEDULING METHODOLOGY & PERT
    # ==========================================
    story.append(Paragraph("1. Project Scheduling Methodology & Activity Definition", styles['DocH1']))
    story.append(Paragraph("1.1 Derivation of Activities from WBS Work Packages", styles['DocH2']))
    story.append(Paragraph(
        "Project scheduling transforms static deliverables into a dynamic, time-phased operational model. Every activity in the schedule register maps 1:1 to a corresponding lowest-level work package in the WBS Dictionary (Assignment 1). Activities represent discrete, executable tasks with defined input conditions, estimated working-day durations, assigned engineering resources, and verifiable completion milestones.",
        styles['DocBody']
    ))
    story.append(Paragraph("1.2 Dependency Logic & Precedence Relationship Types", styles['DocH2']))
    story.append(Paragraph(
        "Logical sequencing applies the four standard precedence relationship types defined in PMBOK Guide 7th Edition:<br/>"
        "&bull; <b>Finish-to-Start (FS):</b> Successor activity cannot begin until its predecessor finishes. (Default dependency across 85% of project paths, e.g., ACT-01 Requirements must finish before ACT-02 Architecture can begin).<br/>"
        "&bull; <b>Start-to-Start (SS):</b> Successor activity begins concurrently after predecessor begins, with justified lead/lag. (Utilized between ACT-04 DB Schema and ACT-05 Cloud Infrastructure with a 4-day lag).<br/>"
        "&bull; <b>Finish-to-Finish (FF):</b> Successor activity cannot finish until predecessor finishes. (Utilized between ACT-18 Load Testing and ACT-20 UAT).<br/>"
        "&bull; <b>Start-to-Finish (SF):</b> Successor cannot finish until predecessor starts. (Evaluated and rejected to prevent unmanaged dependency loops).",
        styles['DocBody']
    ))

    story.append(Paragraph("1.3 Three-Point PERT Duration Estimation & Statistical Risk Analysis", styles['DocH2']))
    story.append(Paragraph(
        "Activity durations were estimated using **Three-Point Beta / PERT Estimation** to incorporate technical uncertainty:<br/>"
        "$$\\text{Expected Duration } (T_e) = \\frac{O + 4M + P}{6}, \\quad \\text{Standard Deviation } (\\sigma) = \\frac{P - O}{6}, \\quad \\text{Variance } (\\sigma^2) = \\left(\\frac{P - O}{6}\\right)^2$$"
        "Where $O$ is the optimistic duration (best-case scenario), $M$ is the most likely duration, and $P$ is the pessimistic duration under adverse operational friction (e.g., unexpected schema migrations or network timeout anomalies).",
        styles['DocBody']
    ))

    pert_headers = [Paragraph("Act ID", styles['TableHeader']), Paragraph("Activity Name", styles['TableHeader']),
                    Paragraph("Opt (O)", styles['TableHeader']), Paragraph("ML (M)", styles['TableHeader']),
                    Paragraph("Pess (P)", styles['TableHeader']), Paragraph("Te (Days)", styles['TableHeader']),
                    Paragraph("StdDev", styles['TableHeader']), Paragraph("Variance", styles['TableHeader'])]
    
    pert_rows = [
        ["ACT-01", "Requirements Gathering", "2.0d", "3.0d", "4.0d", "3.0d", "0.33", "0.11"],
        ["ACT-02", "System Architecture & Specs", "3.0d", "4.0d", "5.0d", "4.0d", "0.33", "0.11"],
        ["ACT-03", "Government Compliance Audit", "2.0d", "3.0d", "4.0d", "3.0d", "0.33", "0.11"],
        ["ACT-04", "Database Schema & Multi-Tenancy", "3.0d", "4.0d", "5.0d", "4.0d", "0.33", "0.11"],
        ["ACT-05", "Cloud VPC & Terraform IAC", "4.0d", "5.0d", "6.0d", "5.0d", "0.33", "0.11"],
        ["ACT-06", "Spring Boot Core Setup", "4.0d", "5.0d", "6.0d", "5.0d", "0.33", "0.11"],
        ["ACT-07", "Docker Containerization", "3.0d", "4.0d", "5.0d", "4.0d", "0.33", "0.11"],
        ["ACT-08", "Authentication & RBAC Engine", "3.0d", "4.0d", "5.0d", "4.0d", "0.33", "0.11"],
        ["ACT-09", "School Registry Profile Module", "4.0d", "5.0d", "6.0d", "5.0d", "0.33", "0.11"],
        ["ACT-10", "Teacher Allocation Module", "4.0d", "5.0d", "6.0d", "5.0d", "0.33", "0.11"],
        ["ACT-11", "Student Enrollment Bulk CSV", "4.0d", "6.0d", "8.0d", "6.0d", "0.67", "0.44"],
        ["ACT-12", "Attendance Geo-Fencing PWA", "4.0d", "5.0d", "6.0d", "5.0d", "0.33", "0.11"],
        ["ACT-13", "School Inspection Audit", "3.0d", "4.0d", "5.0d", "4.0d", "0.33", "0.11"],
        ["ACT-14", "District Analytics BI Dashboard", "3.0d", "4.0d", "5.0d", "4.0d", "0.33", "0.11"],
        ["ACT-15", "Document Vault OCR Engine", "3.0d", "4.0d", "6.0d", "4.2d", "0.50", "0.25"],
        ["ACT-16", "Automated SMS Alert Gateway", "2.0d", "3.0d", "4.0d", "3.0d", "0.33", "0.11"],
        ["ACT-17", "Playwright Integration Testing", "4.0d", "5.0d", "7.0d", "5.2d", "0.50", "0.25"],
        ["ACT-18", "JMeter Load & Scalability", "3.0d", "4.0d", "5.0d", "4.0d", "0.33", "0.11"],
        ["ACT-19", "Security OWASP Penetration Test", "2.0d", "3.0d", "4.0d", "3.0d", "0.33", "0.11"],
        ["ACT-20", "Pilot District UAT Sign-Off", "3.0d", "4.0d", "5.0d", "4.0d", "0.33", "0.11"],
        ["ACT-21", "Production DNS Cutover", "4.0d", "5.0d", "6.0d", "5.0d", "0.33", "0.11"]
    ]

    t_pert_data = [pert_headers]
    for r in pert_rows:
        t_pert_data.append([
            Paragraph(r[0], styles['TableCellBold']),
            Paragraph(r[1], styles['TableCell']),
            Paragraph(r[2], styles['TableCell']),
            Paragraph(r[3], styles['TableCell']),
            Paragraph(r[4], styles['TableCell']),
            Paragraph(r[5], styles['TableCellBold']),
            Paragraph(r[6], styles['TableCell']),
            Paragraph(r[7], styles['TableCell'])
        ])

    t_pert = Table(t_pert_data, colWidths=[45, 160, 42, 42, 42, 55, 45, 45], repeatRows=1)
    t_pert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_pert)
    story.append(Spacer(1, 10))

    # PERT Normal Distribution Confidence Table
    story.append(Paragraph("1.4 Statistical Confidence Analysis & Completion Probability Modeling", styles['DocH2']))
    story.append(Paragraph(
        "By applying the Central Limit Theorem across the 13 zero-float activities on the critical path, the project duration follows a normal distribution with mean $\\mu_{\\text{CP}} = 54.0\\text{ days}$ and standard deviation $\\sigma_{\\text{CP}} = \\sqrt{\\sum \\sigma^2} = \\sqrt{1.88} = 1.37\\text{ days}$. The cumulative probability of finishing on or before target day $X$ is computed via the standard normal variable $Z = \\frac{X - \\mu}{\\sigma}$:",
        styles['DocBody']
    ))

    prob_headers = [Paragraph("Target Delivery Day (X)", styles['TableHeader']), Paragraph("Standard Z-Score", styles['TableHeader']), Paragraph("Cumulative Normal Probability P(T &le; X)", styles['TableHeader']), Paragraph("Academic Milestone Context", styles['TableHeader'])]
    prob_rows = [
        ["50 Working Days", "-2.92", "0.18%", "Aggressive accelerated target (requires crashing)"],
        ["52 Working Days", "-1.46", "7.21%", "Early completion before pilot evaluation"],
        ["54 Working Days", "0.00", "50.00%", "Deterministic CPM Baseline Milestone"],
        ["56 Working Days", "+1.46", "92.79%", "Minor non-critical delay absorption"],
        ["60 Working Days", "+4.38", "99.99%", "Buffer absorption (well within semester)"],
        ["80 Working Days", "+18.98", ">99.999%", "Authorized 16-Week Academic Window Limit"]
    ]
    t_prob_data = [prob_headers]
    for r in prob_rows:
        t_prob_data.append([
            Paragraph(r[0], styles['TableCellBold']),
            Paragraph(r[1], styles['TableCellBold']),
            Paragraph(r[2], styles['TableCellBold']),
            Paragraph(r[3], styles['TableCell'])
        ])
    t_prob = Table(t_prob_data, colWidths=[110, 85, 135, 174])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 10))

    # ==========================================
    # CHAPTER 2: CPM MATHEMATICS & MASTER TABLE
    # ==========================================
    story.append(Paragraph("2. Critical Path Method (CPM) Detailed Mathematical Formulations", styles['DocH1']))
    story.append(Paragraph(
        "Critical Path Method (CPM) calculations utilize deterministic forward and backward pass network traversals across all 21 nodes:",
        styles['DocBody']
    ))
    story.append(Paragraph("<b>1. Forward Pass (Early Dates):</b><br/>"
                           "Early Start (ES) = $\\max[\\text{Early Finish (EF) of all immediate predecessors}]$<br/>"
                           "Early Finish (EF) = $\\text{Early Start (ES)} + \\text{Duration (D)}$", styles['DocFormula']))
    story.append(Paragraph("<b>2. Backward Pass (Late Dates):</b><br/>"
                           "Late Finish (LF) = $\\min[\\text{Late Start (LS) of all immediate successors}]$<br/>"
                           "Late Start (LS) = $\\text{Late Finish (LF)} - \\text{Duration (D)}$", styles['DocFormula']))
    story.append(Paragraph("<b>3. Float Formulations:</b><br/>"
                           "Total Float (TF) = $LS - ES = LF - EF$<br/>"
                           "Free Float (FF) = $\\min[\\text{ES of immediate successors}] - EF$", styles['DocFormula']))
    story.append(Paragraph("<b>4. Critical Activity Identity:</b> Any activity with $TF = 0$ days is strictly critical. A delay in any critical activity causes a 1:1 delay in the final project delivery date.", styles['DocCallout']))

    # Master CPM Activity Table
    cpm_table_headers = [Paragraph("ID", styles['TableHeader']), Paragraph("Activity Name", styles['TableHeader']),
                         Paragraph("Dur", styles['TableHeader']), Paragraph("Pred", styles['TableHeader']),
                         Paragraph("ES", styles['TableHeader']), Paragraph("EF", styles['TableHeader']),
                         Paragraph("LS", styles['TableHeader']), Paragraph("LF", styles['TableHeader']),
                         Paragraph("TF", styles['TableHeader']), Paragraph("FF", styles['TableHeader']),
                         Paragraph("Status", styles['TableHeader']), Paragraph("Cost (INR)", styles['TableHeader'])]

    cpm_rows = [
        ["ACT-01", "Requirements Gathering", "3d", "-", "0", "3", "0", "3", "0", "0", "CRITICAL", "18,000"],
        ["ACT-02", "Arch & Specs Blueprint", "4d", "01", "3", "7", "3", "7", "0", "0", "CRITICAL", "24,000"],
        ["ACT-03", "Regulatory Compliance", "3d", "02", "7", "10", "38", "41", "31", "31", "Non-Crit", "18,000"],
        ["ACT-04", "DB Schema Multi-Tenancy", "4d", "02", "7", "11", "7", "11", "0", "0", "CRITICAL", "30,000"],
        ["ACT-05", "Cloud VPC & Terraform", "5d", "04", "11", "16", "12", "17", "1", "0", "Near-Crit", "36,000"],
        ["ACT-06", "Spring Boot Core Setup", "5d", "04", "11", "16", "11", "16", "0", "0", "CRITICAL", "42,000"],
        ["ACT-07", "Docker Containerization", "4d", "05, 06", "16", "20", "37", "41", "21", "21", "Non-Crit", "24,000"],
        ["ACT-08", "Authentication & RBAC", "4d", "06", "16", "20", "16", "20", "0", "0", "CRITICAL", "30,000"],
        ["ACT-09", "School Registry Profile", "5d", "08", "20", "25", "20", "25", "0", "0", "CRITICAL", "26,500"],
        ["ACT-10", "Teacher Allocation Module", "5d", "09", "25", "30", "25", "30", "0", "0", "CRITICAL", "29,000"],
        ["ACT-11", "Student Enrollment Bulk", "6d", "10", "30", "36", "35", "41", "5", "5", "Non-Crit", "34,000"],
        ["ACT-12", "Attendance Geo-Fencing", "5d", "10", "30", "35", "36", "41", "6", "6", "Non-Crit", "26,500"],
        ["ACT-13", "School Inspection Audit", "4d", "10", "30", "34", "30", "34", "0", "0", "CRITICAL", "21,500"],
        ["ACT-14", "District Analytics BI", "4d", "13", "34", "38", "34", "38", "0", "0", "CRITICAL", "24,000"],
        ["ACT-15", "Document Vault OCR", "4d", "13", "34", "38", "34", "38", "0", "0", "CRIT-SUB", "19,500"],
        ["ACT-16", "Automated SMS Alerting", "3d", "14, 15", "38", "41", "38", "41", "0", "0", "CRITICAL", "18,000"],
        ["ACT-17", "Playwright Integration", "5d", "16", "41", "46", "41", "46", "0", "0", "CRITICAL", "27,000"],
        ["ACT-18", "JMeter Load Scalability", "4d", "17", "46", "50", "46", "50", "0", "0", "Near-Crit", "22,000"],
        ["ACT-19", "Security OWASP Pentest", "3d", "17", "46", "49", "46", "49", "0", "0", "CRITICAL", "18,500"],
        ["ACT-20", "Pilot District UAT", "4d", "18, 19", "49", "53", "50", "54", "1", "1", "Near-Crit", "14,500"],
        ["ACT-21", "Production DNS Cutover", "5d", "19", "49", "54", "49", "54", "0", "0", "CRITICAL", "21,000"],
    ]

    cpm_table_data = [cpm_table_headers]
    for r in cpm_rows:
        is_crit = "CRIT" in r[10]
        c_style = styles['TableCellBold'] if is_crit else styles['TableCell']
        cpm_table_data.append([
            Paragraph(r[0], c_style),
            Paragraph(r[1], c_style),
            Paragraph(r[2], styles['TableCellBold']),
            Paragraph(r[3], styles['TableCell']),
            Paragraph(r[4], styles['TableCell']),
            Paragraph(r[5], styles['TableCell']),
            Paragraph(r[6], styles['TableCell']),
            Paragraph(r[7], styles['TableCell']),
            Paragraph(r[8], styles['TableCellBold']),
            Paragraph(r[9], styles['TableCell']),
            Paragraph(r[10], c_style),
            Paragraph(r[11], styles['TableCellBold'])
        ])

    cpm_table_data.append([
        Paragraph("TOTAL", styles['TableHeader']),
        Paragraph("Deterministic Critical Path", styles['TableHeader']),
        Paragraph("54d", styles['TableHeader']),
        Paragraph("-", styles['TableHeader']),
        Paragraph("0", styles['TableHeader']),
        Paragraph("54", styles['TableHeader']),
        Paragraph("0", styles['TableHeader']),
        Paragraph("54", styles['TableHeader']),
        Paragraph("0d", styles['TableHeader']),
        Paragraph("0d", styles['TableHeader']),
        Paragraph("13 Zero-Float", styles['TableHeader']),
        Paragraph("4,10,000", styles['TableHeader'])
    ])

    t_cpm = Table(cpm_table_data, colWidths=[36, 100, 22, 32, 20, 20, 20, 20, 20, 20, 54, 40], repeatRows=1)
    t_cpm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BACKGROUND', (0,-1), (-1,-1), SECONDARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_cpm)
    story.append(Spacer(1, 10))

    # ==========================================
    # PATH ENUMERATION TABLE (Academic Depth)
    # ==========================================
    story.append(Paragraph("2.2 Complete Network Path Enumeration & Structural Float Spectrum", styles['DocH2']))
    story.append(Paragraph(
        "A formal combinatorial traversal across the Directed Acyclic Graph (DAG) identifies key structural paths connecting Project Start to Project Finish:",
        styles['DocBody']
    ))

    paths_data = [
        [Paragraph("Path ID", styles['TableHeader']), Paragraph("Complete Sequence of Activities", styles['TableHeader']), Paragraph("Total Dur", styles['TableHeader']), Paragraph("Path Float", styles['TableHeader']), Paragraph("Risk Classification", styles['TableHeader'])],
        [Paragraph("PATH-01", styles['TableCellBold']), Paragraph("01 -> 02 -> 04 -> 06 -> 08 -> 09 -> 10 -> 13 -> 14 -> 16 -> 17 -> 19 -> 21", styles['TableCellBold']), Paragraph("54 Days", styles['TableCellBold']), Paragraph("0 Days", styles['TableCellBold']), Paragraph("CRITICAL PATH (Zero Float)", styles['TableCellBold'])],
        [Paragraph("PATH-02", styles['TableCellBold']), Paragraph("01 -> 02 -> 04 -> 06 -> 08 -> 09 -> 10 -> 13 -> 15 -> 16 -> 17 -> 19 -> 21", styles['TableCellBold']), Paragraph("54 Days", styles['TableCellBold']), Paragraph("0 Days", styles['TableCellBold']), Paragraph("CRITICAL SUB-PATH (OCR Engine)", styles['TableCellBold'])],
        [Paragraph("PATH-03", styles['TableCellBold']), Paragraph("01 -> 02 -> 04 -> 06 -> 08 -> 09 -> 10 -> 13 -> 14 -> 16 -> 17 -> 18 -> 20", styles['TableCell']), Paragraph("53 Days", styles['TableCellBold']), Paragraph("1 Day", styles['TableCellBold']), Paragraph("NEAR-CRITICAL (Load Test)", styles['TableCell'])],
        [Paragraph("PATH-04", styles['TableCellBold']), Paragraph("01 -> 02 -> 04 -> 05 -> 07 -> 16 -> 17 -> 19 -> 21", styles['TableCell']), Paragraph("33 Days", styles['TableCell']), Paragraph("21 Days", styles['TableCellBold']), Paragraph("Low Risk (Cloud Infra)", styles['TableCell'])],
        [Paragraph("PATH-05", styles['TableCellBold']), Paragraph("01 -> 02 -> 04 -> 06 -> 08 -> 09 -> 10 -> 11 -> 16 -> 17 -> 19 -> 21", styles['TableCell']), Paragraph("49 Days", styles['TableCell']), Paragraph("5 Days", styles['TableCellBold']), Paragraph("Moderate Risk (Bulk CSV)", styles['TableCell'])],
        [Paragraph("PATH-06", styles['TableCellBold']), Paragraph("01 -> 02 -> 04 -> 06 -> 08 -> 09 -> 10 -> 12 -> 16 -> 17 -> 19 -> 21", styles['TableCell']), Paragraph("48 Days", styles['TableCell']), Paragraph("6 Days", styles['TableCellBold']), Paragraph("Moderate Risk (Attendance PWA)", styles['TableCell'])],
        [Paragraph("PATH-07", styles['TableCellBold']), Paragraph("01 -> 02 -> 03 -> 16 -> 17 -> 19 -> 21", styles['TableCell']), Paragraph("23 Days", styles['TableCell']), Paragraph("31 Days", styles['TableCellBold']), Paragraph("Low Risk (Compliance)", styles['TableCell'])]
    ]
    t_paths = Table(paths_data, colWidths=[55, 230, 55, 55, 81])
    t_paths.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_paths)
    story.append(Spacer(1, 10))

    # Critical Chain Project Management (CCPM) Theory (Academic Expansion)
    story.append(Paragraph("2.3 Critical Chain Project Management (CCPM) vs. Critical Path Method (CPM)", styles['DocH2']))
    story.append(Paragraph(
        "While CPM provides deterministic mathematical boundaries, real-world execution is subject to human behavioral friction documented in Critical Chain Project Management (Goldratt, 1997):<br/>"
        "&bull; <b>Student Syndrome:</b> Engineers delay initiating work until the final deadline approaches, wasting early schedule float.<br/>"
        "&bull; <b>Parkinson's Law:</b> Work expands to fill the time allocated for its completion, preventing early finishes from advancing subsequent milestones.<br/>"
        "&bull; <b>Sandbagging:</b> Individual developers embed private safety margins into their task duration estimates.<br/>"
        "<b>ShalaConnect Strategic Mitigation:</b> Durations are estimated aggressively at median 50% likelihood (54 deterministic days). All safety margins are stripped from individual work packages and consolidated into a **centralized 26-day Project Buffer** at the end of the project chain, plus dedicated feeding buffers where non-critical paths merge into the critical path.",
        styles['DocBody']
    ))

    # ==========================================
    # LANDSCAPE PAGES 1, 2, 3, 4: CPM, GANTT & HISTOGRAM
    # ==========================================
    story.append(NextPageTemplate('Landscape'))
    story.append(PageBreak())
    story.append(Paragraph("Figure 2.1: Activity-on-Node (AON) Network Diagram with Standard 7-Block CPM Nodes", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/aon_network_diagram.png", width=9.8*inch, height=5.5*inch))
    story.append(Paragraph("The complete AON CPM network shows all 21 activities with early/late start and finish times, durations, and float values. The critical path (54 working days, 13 zero-float activities) is highlighted in bold red. Non-critical dependency connectors are shown in dashed lines.", styles['DocCallout']))

    story.append(PageBreak())
    story.append(Paragraph("Figure 2.2: Dedicated Critical Path Linear Traversal (Day 0 to Day 54 Milestone Sequence)", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/critical_path_traversal.png", width=9.8*inch, height=3.2*inch))
    story.append(Paragraph("Dedicated linear view of the 13 activities forming the unyielding Critical Path (Total Float = 0 days). Any delay along this sequence directly slips the Day 54 production release milestone.", styles['DocCallout']))

    story.append(PageBreak())
    story.append(Paragraph("Figure 2.3: 16-Week Schedule Baseline Gantt Chart Across Academic Semester", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/gantt_chart.png", width=9.8*inch, height=5.5*inch))
    story.append(Paragraph("Gantt schedule plotted across the 16-week (80-day) academic calendar. Critical activities are rendered in solid red bars; non-critical activities are shown in slate blue. The 26-day operational buffer absorbs university examinations and pilot school review cycles.", styles['DocCallout']))

    story.append(PageBreak())
    story.append(Paragraph("Figure 2.4: Resource Allocation & Staffing Utilization Histogram Across 16 Weeks", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/resource_allocation_chart.png", width=9.8*inch, height=5.0*inch))
    story.append(Paragraph("Weekly person-day staffing distribution across five core project roles, validating that peak engineering load remains balanced under 22 person-days per week during sprint execution.", styles['DocCallout']))

    # ==========================================
    # RETURN TO PORTRAIT: COMPRESSION & BUDGETING
    # ==========================================
    story.append(NextPageTemplate('Portrait'))
    story.append(PageBreak())

    story.append(Paragraph("3. Schedule Compression Analysis: Crashing vs. Fast-Tracking", styles['DocH1']))
    story.append(Paragraph(
        "To evaluate schedule risk mitigation options under severe external delays, formal schedule compression analysis was conducted:",
        styles['DocBody']
    ))
    story.append(Paragraph("<b>1. Crashing Analysis:</b><br/>"
                           "Crashing adds financial resources to compress duration along the critical path at the lowest marginal cost slope:<br/>"
                           "$$\\text{Cost Slope} = \\frac{\\text{Crash Cost} - \\text{Normal Cost}}{\\text{Normal Duration} - \\text{Crash Duration}}$$", styles['DocFormula']))

    crash_data = [
        [Paragraph("Critical Activity", styles['TableHeader']), Paragraph("Normal Dur", styles['TableHeader']), Paragraph("Crash Dur", styles['TableHeader']), Paragraph("Normal Cost", styles['TableHeader']), Paragraph("Crash Cost", styles['TableHeader']), Paragraph("Cost Slope / Day", styles['TableHeader']), Paragraph("Feasibility", styles['TableHeader'])],
        [Paragraph("ACT-06: Spring Boot Setup", styles['TableCellBold']), Paragraph("5d", styles['TableCell']), Paragraph("3d", styles['TableCell']), Paragraph("INR 42,000", styles['TableCell']), Paragraph("INR 48,000", styles['TableCell']), Paragraph("INR 3,000 / day", styles['TableCellBold']), Paragraph("RECOMMENDED (Priority 1)", styles['TableCellBold'])],
        [Paragraph("ACT-17: Playwright Integration", styles['TableCellBold']), Paragraph("5d", styles['TableCell']), Paragraph("3d", styles['TableCell']), Paragraph("INR 27,000", styles['TableCell']), Paragraph("INR 32,000", styles['TableCell']), Paragraph("INR 2,500 / day", styles['TableCellBold']), Paragraph("RECOMMENDED (Priority 2)", styles['TableCellBold'])],
        [Paragraph("ACT-04: DB Schema Multi-Tenant", styles['TableCellBold']), Paragraph("4d", styles['TableCell']), Paragraph("3d", styles['TableCell']), Paragraph("INR 30,000", styles['TableCell']), Paragraph("INR 36,000", styles['TableCell']), Paragraph("INR 6,000 / day", styles['TableCellBold']), Paragraph("High Risk (Liquibase)", styles['TableCell'])],
        [Paragraph("ACT-10: Teacher Allocation", styles['TableCellBold']), Paragraph("5d", styles['TableCell']), Paragraph("4d", styles['TableCell']), Paragraph("INR 29,000", styles['TableCell']), Paragraph("INR 34,000", styles['TableCell']), Paragraph("INR 5,000 / day", styles['TableCellBold']), Paragraph("Moderate Cost", styles['TableCell'])]
    ]
    t_crash = Table(crash_data, colWidths=[110, 45, 45, 60, 60, 80, 104])
    t_crash.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_crash)

    story.append(Paragraph(
        "<b>2. Fast-Tracking Analysis:</b><br/>"
        "Fast-tracking executes sequential critical path activities in parallel. In ShalaConnect, ACT-05 (Cloud VPC) is fast-tracked with ACT-06 (Spring Boot Setup) using a Start-to-Start (SS) dependency with a 2-day lag, shaving 3 days off parallel infrastructure ramp-up with zero added cost.",
        styles['DocBody']
    ))

    # Unit Cost Rate Analysis (Academic Expansion)
    story.append(Paragraph("4. Bottom-Up Cost Estimation & Budget Aggregation", styles['DocH1']))
    story.append(Paragraph("4.1 Resource Unit Labor Rates & Infrastructure Cost Model", styles['DocH2']))
    story.append(Paragraph(
        "Activity costs are derived bottom-up using standardized professional billing rates across engineering roles, cloud computing resources, and tooling licenses:",
        styles['DocBody']
    ))

    rates_headers = [Paragraph("Engineering Role / Resource Category", styles['TableHeader']), Paragraph("Unit Daily Rate (INR)", styles['TableHeader']), Paragraph("Allocated Days", styles['TableHeader']), Paragraph("Total Cost (INR)", styles['TableHeader']), Paragraph("Primary Responsibility", styles['TableHeader'])]
    rates_rows = [
        ["Project Manager & Lead Architect", "INR 6,000 / day", "15 Person-Days", "INR 90,000", "System architecture, governance, stakeholder reviews"],
        ["Senior Backend Engineer (Spring Boot)", "INR 5,000 / day", "25 Person-Days", "INR 1,25,000", "REST APIs, auth, business logic, integrations"],
        ["Frontend & PWA Specialist (React 18)", "INR 4,500 / day", "20 Person-Days", "INR 90,000", "PWA UI, Leaflet GPS, offline sync cache"],
        ["Database Administrator (PostgreSQL DBA)", "INR 5,000 / day", "8 Person-Days", "INR 40,000", "Multi-tenant DDL, Liquibase, indexing, backups"],
        ["QA & Automation Lead (Playwright)", "INR 4,000 / day", "13 Person-Days", "INR 52,000", "End-to-end testing, JMeter load, UAT support"],
        ["DevOps & Cloud Specialist (AWS / Docker)", "INR 5,500 / day", "10 Person-Days", "INR 55,000", "Terraform IAC, ECS Fargate, CI/CD pipeline"],
        ["AWS Cloud Hosting & Third-Party APIs", "Fixed Monthly", "16 Weeks (4 Mos)", "INR 28,000", "ECS, RDS Multi-AZ, S3, Route 53, Twilio SMS"]
    ]
    t_rates_data = [rates_headers]
    for r in rates_rows:
        t_rates_data.append([
            Paragraph(r[0], styles['TableCellBold']),
            Paragraph(r[1], styles['TableCellBold']),
            Paragraph(r[2], styles['TableCell']),
            Paragraph(r[3], styles['TableCellBold']),
            Paragraph(r[4], styles['TableCell'])
        ])
    t_rates = Table(t_rates_data, colWidths=[130, 80, 75, 80, 111])
    t_rates.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_rates)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4.2 Control Account Cost Aggregation & Reserve Separation", styles['DocH2']))
    story.append(Paragraph(
        "Project financial management applies bottom-up activity costing aggregated into five Control Accounts (CA-01 through CA-05). Contingency and management reserves are explicitly separated per PMBOK standards:",
        styles['DocBody']
    ))

    budget_table_data = [
        [Paragraph("Budget Component / Control Account", styles['TableHeader']), Paragraph("Direct Cost (INR)", styles['TableHeader']), Paragraph("Indirect Cost (INR)", styles['TableHeader']), Paragraph("Aggregated Cost (INR)", styles['TableHeader']), Paragraph("% of Budget", styles['TableHeader'])],
        [Paragraph("CA-01: Project Inception & Compliance", styles['TableCellBold']), Paragraph("50,000", styles['TableCell']), Paragraph("10,000", styles['TableCell']), Paragraph("60,000", styles['TableCellBold']), Paragraph("12.37%", styles['TableCell'])],
        [Paragraph("CA-02: Architecture & Foundation Infrastructure", styles['TableCellBold']), Paragraph("1,10,000", styles['TableCell']), Paragraph("22,000", styles['TableCell']), Paragraph("1,32,000", styles['TableCellBold']), Paragraph("27.22%", styles['TableCell'])],
        [Paragraph("CA-03: Core Educational Service Modules", styles['TableCellBold']), Paragraph("1,21,000", styles['TableCell']), Paragraph("28,000", styles['TableCell']), Paragraph("1,49,000", styles['TableCellBold']), Paragraph("30.72%", styles['TableCell'])],
        [Paragraph("CA-04: Quality Assurance, Security & Pentest", styles['TableCellBold']), Paragraph("25,000", styles['TableCell']), Paragraph("8,500", styles['TableCell']), Paragraph("33,500", styles['TableCellBold']), Paragraph("6.91%", styles['TableCell'])],
        [Paragraph("CA-05: Deployment, Pilot UAT & Handover", styles['TableCellBold']), Paragraph("30,000", styles['TableCell']), Paragraph("5,500", styles['TableCell']), Paragraph("35,500", styles['TableCellBold']), Paragraph("7.32%", styles['TableCell'])],
        [Paragraph("COST BASELINE (BAC - Aggregated Work Packages)", styles['TableHeader']), Paragraph("3,36,000", styles['TableHeader']), Paragraph("74,000", styles['TableHeader']), Paragraph("4,10,000", styles['TableHeader']), Paragraph("84.54%", styles['TableHeader'])],
        [Paragraph("Contingency Reserve (10% - Identified Risk Register Threats)", styles['TableCellBold']), Paragraph("-", styles['TableCell']), Paragraph("-", styles['TableCell']), Paragraph("41,000", styles['TableCellBold']), Paragraph("8.45%", styles['TableCell'])],
        [Paragraph("Management Reserve (7% - Unforeseen Regulatory / Sponsor Scope)", styles['TableCellBold']), Paragraph("-", styles['TableCell']), Paragraph("-", styles['TableCell']), Paragraph("34,000", styles['TableCellBold']), Paragraph("7.01%", styles['TableCell'])],
        [Paragraph("TOTAL APPROVED PROJECT BUDGET", styles['TableHeader']), Paragraph("3,36,000", styles['TableHeader']), Paragraph("74,000", styles['TableHeader']), Paragraph("4,85,000", styles['TableHeader']), Paragraph("100.00%", styles['TableHeader'])]
    ]
    t_b = Table(budget_table_data, colWidths=[184, 80, 80, 90, 70])
    t_b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BACKGROUND', (0,6), (-1,6), SECONDARY),
        ('BACKGROUND', (0,-1), (-1,-1), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_b)
    story.append(Spacer(1, 10))

    # Time-Phased Weekly Spend Table (Academic Depth)
    story.append(Paragraph("4.3 Time-Phased Cumulative Expenditure Schedule (16 Weeks)", styles['DocH2']))
    cash_flow_data = [
        [Paragraph("Wk", styles['TableHeader']), Paragraph("Milestone Focus", styles['TableHeader']), Paragraph("Wkly Direct", styles['TableHeader']), Paragraph("Wkly Indir", styles['TableHeader']), Paragraph("Wkly Total", styles['TableHeader']), Paragraph("Cumul Spend (PV)", styles['TableHeader']), Paragraph("% of BAC", styles['TableHeader'])],
        ["W1", "Project Inception & SRS", "15,000", "3,000", "18,000", "INR 18,000", "4.39%"],
        ["W2", "C4 Architecture & DPDPA", "35,000", "7,000", "42,000", "INR 60,000", "14.63%"],
        ["W3", "DB Schema & Terraform", "28,000", "6,000", "34,000", "INR 94,000", "22.93%"],
        ["W4", "Spring Boot & Docker", "38,000", "8,000", "46,000", "INR 1,40,000", "34.15%"],
        ["W5", "Auth RBAC & School Registry", "32,000", "7,000", "39,000", "INR 1,79,000", "43.66%"],
        ["W6", "Teacher Module & Ingestion", "30,000", "6,500", "36,500", "INR 2,15,500", "52.56%"],
        ["W7", "Attendance PWA Geofencing", "24,000", "5,500", "29,500", "INR 2,45,000", "59.76%"],
        ["W8", "School Inspection & Analytics", "35,000", "8,000", "43,000", "INR 2,88,000", "70.24%"],
        ["W9", "OCR Vault & SMS Alerts", "26,000", "6,000", "32,000", "INR 3,20,000", "78.05%"],
        ["W10", "Playwright Automation Suite", "15,000", "4,000", "19,000", "INR 3,39,000", "82.68%"],
        ["W11", "JMeter & OWASP Pentest", "18,000", "4,500", "22,500", "INR 3,61,500", "88.17%"],
        ["W12", "Pilot District UAT", "15,000", "3,500", "18,500", "INR 3,80,000", "92.68%"],
        ["W13", "User Defect Remediation", "8,000", "2,000", "10,000", "INR 3,90,000", "95.12%"],
        ["W14", "Production DNS Cutover", "10,000", "2,000", "12,000", "INR 4,02,000", "98.05%"],
        ["W15", "Operational Runbook Handover", "5,000", "1,500", "6,500", "INR 4,08,500", "99.63%"],
        ["W16", "Final Project Closeout", "1,000", "500", "1,500", "INR 4,10,000", "100.00%"]
    ]

    t_cf_data = [cash_flow_data[0]]
    for r in cash_flow_data[1:]:
        t_cf_data.append([
            Paragraph(r[0], styles['TableCellBold']),
            Paragraph(r[1], styles['TableCell']),
            Paragraph(r[2], styles['TableCell']),
            Paragraph(r[3], styles['TableCell']),
            Paragraph(r[4], styles['TableCellBold']),
            Paragraph(r[5], styles['TableCellBold']),
            Paragraph(r[6], styles['TableCell'])
        ])

    t_cf = Table(t_cf_data, colWidths=[28, 150, 60, 60, 65, 85, 56], repeatRows=1)
    t_cf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_cf)

    # ==========================================
    # LANDSCAPE PAGES 5 & 6: BUDGET DONUT & S-CURVE
    # ==========================================
    story.append(NextPageTemplate('Landscape'))
    story.append(PageBreak())
    story.append(Paragraph("Figure 2.5: Budget Breakdown: Control Account Donut & Total Budget Composition", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/budget_breakdown_chart.png", width=9.8*inch, height=5.0*inch))
    story.append(Paragraph("Financial visualization showing the Cost Baseline (BAC = INR 4,10,000) distributed across 5 Control Accounts, alongside the Contingency Reserve (INR 41,000) and Management Reserve (INR 34,000) forming the Total Budget of INR 4,85,000.", styles['DocCallout']))

    story.append(PageBreak())
    story.append(Paragraph("Figure 2.6: Time-Phased Cumulative Expenditure S-Curve Across 16 Weeks", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/scurve_chart.png", width=9.8*inch, height=5.2*inch))
    story.append(Paragraph("Time-phased cumulative spend S-Curve showing weekly capital drawdown against the approved Cost Baseline (BAC = INR 4,10,000). The curve follows classic project lifecycle dynamics: slow initial startup spend, accelerated development burn during Weeks 4-9, and asymptotic leveling during testing and handover.", styles['DocCallout']))

    # ==========================================
    # RETURN TO PORTRAIT: REFERENCES
    # ==========================================
    story.append(NextPageTemplate('Portrait'))
    story.append(PageBreak())

    story.append(Paragraph("5. Academic References & IEEE Bibliography", styles['DocH1']))
    refs2 = [
        "[1] Project Management Institute, *Practice Standard for Scheduling*, 3rd ed. Newtown Square, PA: PMI, 2019.",
        "[2] J. R. Meredith, S. J. Mantel Jr., and S. M. Shafer, *Project Management: A Managerial Approach*, 10th ed. Hoboken, NJ: Wiley, 2017.",
        "[3] H. Kerzner, *Project Management: A Systems Approach to Planning, Scheduling, and Controlling*, 13th ed. Hoboken, NJ: Wiley, 2022.",
        "[4] R. V. Moder, C. R. Phillips, and E. W. Davis, *Project Management with CPM, PERT and Precedence Diagramming*, 3rd ed. New York: Van Nostrand Reinhold, 1983.",
        "[5] Association for the Advancement of Cost Engineering (AACE) International, *Cost Engineering Terminology*, Recommended Practice No. 10S-90, 2020.",
        "[6] E. M. Goldratt, *Critical Chain*, Great Barrington, MA: North River Press, 1997."
    ]
    for r in refs2:
        story.append(Paragraph(r, styles['DocBullet']))

    doc.build(story, canvasmaker=DynamicCanvas)
    print(f"Masterpiece Expanded Assignment 2 Report successfully generated: {pdf_path}")

if __name__ == "__main__":
    build_assignment_2()
