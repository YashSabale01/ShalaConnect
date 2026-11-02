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
PRIMARY = colors.HexColor("#1B365D")      # MITAOE Deep Navy
SECONDARY = colors.HexColor("#2C5282")    # Slate Blue
ACCENT = colors.HexColor("#D97706")       # Executive Amber
TEXT_DARK = colors.HexColor("#1A202C")    # Charcoal Dark
TEXT_MUTED = colors.HexColor("#4A5568")   # Gray Muted
BG_LIGHT = colors.HexColor("#F7FAFC")     # Table Light Gray
BG_ALT = colors.HexColor("#EDF2F7")       # Table Alternating
BORDER_COLOR = colors.HexColor("#CBD5E0") # Border Gray
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
                self.drawString(54, 34, "Assignment 1: Comprehensive Project Charter, WBS & WBS Dictionary | Master Craftsman Tier")
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

def build_assignment_1():
    pdf_path = "Project_Management_Submissions/Assignment_1_WBS/Assignment_1_Report.pdf"
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
    story.append(Paragraph("Assignment 1: Project Charter, WBS and WBS Dictionary", styles['CoverTitle']))

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
    # CHAPTER 1: STRATEGIC PROJECT CHARTER (Starts on Page 2)
    # ==========================================
    story.append(Paragraph("1. Strategic Project Charter (PMBOK 7th Edition Standard)", styles['DocH1']))
    story.append(Paragraph("1.1 Project Identification & Enterprise Metadata", styles['DocH2']))
    story.append(Paragraph(
        "<b>Project Title:</b> ShalaConnect - School Education Cluster Administration & Governance Platform.<br/>"
        "<b>Project Sponsor:</b> MIT Academy of Engineering (MITAOE) in academic partnership with District Zilla Parishad Education Department.<br/>"
        "<b>Lead Architect & Project Manager:</b> Yash Sabale (B.Tech Computer Engineering, MITAOE).<br/>"
        "<b>Technology Ecosystem:</b> Java 21 LTS, Spring Boot 3.2.3, React 18, PostgreSQL 16 Multi-Tenant, AWS ECS Fargate, ALB, S3, RDS Multi-AZ, Terraform 1.7.<br/>"
        "<b>Authorized Cost Baseline (BAC):</b> INR 4,10,000 | <b>Total Approved Project Budget:</b> INR 4,85,000 (including Reserves).<br/>"
        "<b>Approved Schedule Baseline:</b> 54 Deterministic Working Days across a 16-calendar-week (80-day) academic window.",
        styles['DocBody']
    ))

    story.append(Paragraph("1.2 Executive Background & Public Education Context", styles['DocH2']))
    story.append(Paragraph(
        "In Maharashtra's public school education system, primary and upper-primary schools within rural clusters (comprising 15 to 25 schools per cluster) are administered through decentralized Block Education Offices (BEO) and Zilla Parishad (ZP) headquarters. Currently, school administrative reporting, monthly pupil attendance, teacher service records, midday meal compliance, and academic inspections rely on fragmented physical paper ledgers. This operational fragmentation produces severe systemic liabilities: data collation takes 45 to 60 days, ghost-student accounting leads to mid-day meal leakages, teacher absenteeism remains untracked in remote tribal belt schools, and statutory school compliance reporting under the Right to Education (RTE) Act 2009 is routinely delayed. ShalaConnect is chartered to eliminate this administrative friction by deploying a resilient, offline-capable, multi-tenant digital governance backbone.",
        styles['DocBody']
    ))

    story.append(Paragraph("1.3 Fishbone (Ishikawa) Root-Cause Inefficiency Modeling", styles['DocH2']))
    story.append(Paragraph(
        "To establish the empirical business justification, a comprehensive Ishikawa Root-Cause Analysis was conducted across six operational domains of cluster education administration:",
        styles['DocBody']
    ))

    fishbone_data = [
        [Paragraph("Analysis Domain", styles['TableHeader']), Paragraph("Observed Administrative Failure", styles['TableHeader']), Paragraph("Underlying Root Cause", styles['TableHeader']), Paragraph("ShalaConnect Architectural Solution", styles['TableHeader'])],
        [Paragraph("<b>People</b>", styles['TableCellBold']), Paragraph("Staff reporting non-compliance & delayed records", styles['TableCell']), Paragraph("Senior headmasters lack digital software training", styles['TableCell']), Paragraph("Intuitive Marathi PWA UI; zero-training design", styles['TableCellBold'])],
        [Paragraph("<b>Process</b>", styles['TableCellBold']), Paragraph("45 to 60 days latency in attendance collation", styles['TableCell']), Paragraph("Physical ledger transport via postal/courier trips", styles['TableCell']), Paragraph("Sub-second cloud sync with automated aggregation", styles['TableCellBold'])],
        [Paragraph("<b>Technology</b>", styles['TableCellBold']), Paragraph("High system abandonment during portal entry", styles['TableCell']), Paragraph("Cloud tools fail without persistent broadband", styles['TableCell']), Paragraph("Offline-first SQLite PWA with background sync", styles['TableCellBold'])],
        [Paragraph("<b>Environment</b>", styles['TableCellBold']), Paragraph("Data loss during seasonal power brownouts", styles['TableCell']), Paragraph("Unstable rural 2G/3G telecom infrastructure", styles['TableCell']), Paragraph("Optimized local data cache & resilient retry queues", styles['TableCellBold'])],
        [Paragraph("<b>Measurement</b>", styles['TableCellBold']), Paragraph("Falsified student roll registers & meal counts", styles['TableCell']), Paragraph("Manual headcounts without digital audit logs", styles['TableCell']), Paragraph("GPS geofenced logs & cryptographic verification", styles['TableCellBold'])],
        [Paragraph("<b>Policy</b>", styles['TableCellBold']), Paragraph("RTE 30:1 Student-Teacher Ratio violations", styles['TableCell']), Paragraph("No automated mechanism to identify staff deficits", styles['TableCell']), Paragraph("Automated teacher rationalization engine", styles['TableCellBold'])]
    ]
    t_fish = Table(fishbone_data, colWidths=[65, 135, 145, 159])
    t_fish.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_fish)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.4 Strategic Alignment & Legislative Mandates", styles['DocH2']))
    story.append(Paragraph(
        "ShalaConnect directly implements statutory mandates established by national and state educational policies:<br/>"
        "&bull; <b>National Education Policy (NEP 2020 - Sections 3.4 & 5.14):</b> Mandates the operational integration of school clusters to optimize teacher resource allocation, ensure specialized subject teaching, and establish real-time digital governance.<br/>"
        "&bull; <b>Right to Education Act (RTE 2009 - Section 25):</b> Legally requires continuous pupil-teacher ratio monitoring and transparent cluster inspection records.<br/>"
        "&bull; <b>PM-SHRI Scheme:</b> Provides central infrastructural funding incentives for schools demonstrating digital administration, transparent student enrollment auditing, and paperless governance.<br/>"
        "&bull; <b>Digital Personal Data Protection Act (DPDPA 2023):</b> Mandates cryptographic data security and strict parental consent logging for student records.",
        styles['DocBody']
    ))

    story.append(Paragraph("1.5 Quantified SMART Project Objectives", styles['DocH2']))
    smart_data = [
        [Paragraph("SMART Attribute", styles['TableHeader']), Paragraph("Target Engineering Milestone", styles['TableHeader']), Paragraph("Quantified Performance Metric", styles['TableHeader']), Paragraph("Verification Gate", styles['TableHeader'])],
        [Paragraph("<b>Specific</b>", styles['TableCellBold']), Paragraph("Deploy multi-tenant platform across 20 cluster schools.", styles['TableCell']), Paragraph("20 schools, 150+ teachers, 4,500+ students onboarded.", styles['TableCellBold']), Paragraph("Pilot UAT Sign-Off", styles['TableCell'])],
        [Paragraph("<b>Measurable</b>", styles['TableCellBold']), Paragraph("Eliminate physical paper logs and compress reporting latency.", styles['TableCell']), Paragraph("Reporting latency < 5 seconds; 100% paperless daily logs.", styles['TableCellBold']), Paragraph("District Analytics BI", styles['TableCell'])],
        [Paragraph("<b>Achievable</b>", styles['TableCellBold']), Paragraph("Build on verified open-source enterprise stack with AWS cloud.", styles['TableCell']), Paragraph("p95 latency < 500ms; >99.5% uptime during morning peak.", styles['TableCellBold']), Paragraph("JMeter Load Test", styles['TableCell'])],
        [Paragraph("<b>Relevant</b>", styles['TableCellBold']), Paragraph("Fulfill NEP 2020, RTE Act 2009, and DPDPA 2023 guidelines.", styles['TableCell']), Paragraph("Zero high/critical OWASP bugs; AES-256 field encryption.", styles['TableCellBold']), Paragraph("OWASP Pentest Audit", styles['TableCell'])],
        [Paragraph("<b>Time-bound</b>", styles['TableCellBold']), Paragraph("Complete full engineering, QA, UAT, and production cutover.", styles['TableCell']), Paragraph("54 Deterministic CPM Working Days (within 16 weeks).", styles['TableCellBold']), Paragraph("Final Acceptance Sign-Off", styles['TableCell'])]
    ]
    t_smart = Table(smart_data, colWidths=[70, 160, 160, 114])
    t_smart.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_smart)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.6 Authorized In-Scope Modules & Functional Capabilities", styles['DocH2']))
    story.append(Paragraph(
        "The project scope baseline authorizes seven comprehensive functional subsystems:<br/>"
        "1. <b>Multi-Tenant School Registry & Administration:</b> Full lifecycle school profile management, UDISE+ 11-digit code validation, infrastructure facility audits, and cluster linking.<br/>"
        "2. <b>Teacher Allocation & Service Rationalization:</b> Teacher subject qualifications, inter-school transfer logs, temporary duty postings, and pupil-teacher ratio optimization.<br/>"
        "3. <b>Student Enrollment & Bulk Class Promotion:</b> Student admissions, APAAR ID mapping, social category tracking, annual promotion engine, and high-performance bulk CSV data ingestion.<br/>"
        "4. <b>Mobile PWA Daily Attendance & Geofencing:</b> Offline-first Progressive Web App (PWA) with SQLite local storage, GPS 100-meter radius boundary enforcement, and anti-mock location spoofing.<br/>"
        "5. <b>School Inspection & Compliance Engine:</b> Standardized RTE 10-point inspection checklists, digital scoring algorithm, photo capture with timestamp metadata, and inspection logs.<br/>"
        "6. <b>Secure Document Vault & OCR Verification:</b> AWS S3 bucket storage with pre-signed upload URLs, server-side encryption, and Tesseract OCR for automated student birth certificate parsing.<br/>"
        "7. <b>District Analytics Dashboard & Alerting:</b> React 18 data visualizations, cluster performance heatmaps, and automated transactional SMS alerts to parents for student absenteeism.",
        styles['DocBody']
    ))

    story.append(Paragraph("1.7 Scope Boundaries & Explicit Out-of-Scope Exclusions", styles['DocH2']))
    story.append(Paragraph(
        "To prevent scope creep and maintain financial discipline, the following boundaries are explicitly excluded from the charter baseline:",
        styles['DocBody']
    ))

    scope_ex_data = [
        [Paragraph("Excluded Boundary Domain", styles['TableHeader']), Paragraph("Operational Description", styles['TableHeader']), Paragraph("Strategic Justification for Exclusion", styles['TableHeader']), Paragraph("Future Phase Roadmap", styles['TableHeader'])],
        [Paragraph("Hardware Procurement", styles['TableCellBold']), Paragraph("Supplying tablets, laptops, smartphones, or biometric units.", styles['TableCell']), Paragraph("Exceeds student project capital baseline; BYOD strategy used.", styles['TableCellBold']), Paragraph("Phase II Govt Grant", styles['TableCell'])],
        [Paragraph("Payment Gateway", styles['TableCellBold']), Paragraph("Processing student school fees or direct cash transfers.", styles['TableCell']), Paragraph("Eliminates RBI regulatory compliance audits and financial risks.", styles['TableCellBold']), Paragraph("Future Banking API", styles['TableCell'])],
        [Paragraph("Automated Payroll", styles['TableCellBold']), Paragraph("Teacher salary slips, provident fund, and income tax calculations.", styles['TableCell']), Paragraph("Handled by Maharashtra Sevaarth state financial portal.", styles['TableCellBold']), Paragraph("Sevaarth Export Adapter", styles['TableCell'])],
        [Paragraph("Pre-2020 Historical Digitization", styles['TableCellBold']), Paragraph("Retrospective scanning of physical student registers before 2020.", styles['TableCell']), Paragraph("Labor-intensive physical scanning exceeds current team capacity.", styles['TableCellBold']), Paragraph("District Archive Vendor", styles['TableCell'])],
        [Paragraph("On-Premise Physical Servers", styles['TableCellBold']), Paragraph("Deploying physical server hardware inside school premises.", styles['TableCell']), Paragraph("Rural school power outages cause server downtime; cloud used.", styles['TableCellBold']), Paragraph("100% Cloud Native", styles['TableCell'])],
        [Paragraph("Bus GPS Fleet Tracking", styles['TableCellBold']), Paragraph("Real-time telemetry and transit tracking for school transport.", styles['TableCell']), Paragraph("Zilla Parishad primary students walk to cluster schools.", styles['TableCellBold']), Paragraph("Not Required in Cluster", styles['TableCell'])]
    ]
    t_scope_ex = Table(scope_ex_data, colWidths=[95, 135, 185, 89])
    t_scope_ex.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_scope_ex)

    # ==========================================
    # LANDSCAPE PAGE 1: SCOPE HIERARCHY DIAGRAM
    # ==========================================
    story.append(NextPageTemplate('Landscape'))
    story.append(PageBreak())
    story.append(Paragraph("Figure 1.1: Comprehensive Project Scope Hierarchy & Boundary Decomposition", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_1_WBS/Diagrams/scope_hierarchy.png", width=9.8*inch, height=5.5*inch))
    story.append(Paragraph("The Scope Hierarchy establishes the operational boundaries of ShalaConnect. In-scope items (left) are decomposed into 7 primary software modules. Out-of-scope exclusions (right) are formally separated to protect the Cost Baseline (BAC = INR 4,10,000) and prevent scope creep during execution.", styles['DocCallout']))

    # ==========================================
    # RETURN TO PORTRAIT: GOVERNANCE & STAKEHOLDERS
    # ==========================================
    story.append(NextPageTemplate('Portrait'))
    story.append(PageBreak())

    story.append(Paragraph("1.8 Project Governance, Authority Limits & Change Control", styles['DocH1']))
    story.append(Paragraph("1.8.1 Project Manager's Delegated Authority Limits", styles['DocH2']))
    story.append(Paragraph(
        "The Project Manager (Yash Sabale) operates under formal authority granted by the MITAOE Project Sponsor:",
        styles['DocBody']
    ))

    auth_data = [
        [Paragraph("Governance Dimension", styles['TableHeader']), Paragraph("Delegated Authority Limit (PM Autonomy)", styles['TableHeader']), Paragraph("Escalation Trigger (CCB Approval Required)", styles['TableHeader'])],
        [Paragraph("<b>Financial Authority</b>", styles['TableCellBold']), Paragraph("Commitment of expenses within BAC (INR 4,10,000) and drawdown of Contingency Reserve up to INR 41,000.", styles['TableCell']), Paragraph("Any expense exceeding INR 41,000 contingency or touching Management Reserve (INR 34,000).", styles['TableCellBold'])],
        [Paragraph("<b>Schedule Authority</b>", styles['TableCellBold']), Paragraph("Resequencing non-critical activities and utilizing up to 5 days of the 26-day operational buffer.", styles['TableCell']), Paragraph("Any schedule delay greater than 5 days along the critical path threatening the Day 54 milestone.", styles['TableCellBold'])],
        [Paragraph("<b>Technical Baseline</b>", styles['TableCellBold']), Paragraph("Selection of open-source frameworks, database schemas, and AWS service configurations.", styles['TableCell']), Paragraph("Core architectural redesign replacing Java 21, Spring Boot, PostgreSQL, or AWS hosting.", styles['TableCellBold'])],
        [Paragraph("<b>Scope Modifications</b>", styles['TableCellBold']), Paragraph("Minor UI refinements, report field adjustments, and non-functional usability tweaks.", styles['TableCell']), Paragraph("Addition or deletion of any of the 7 core authorized functional modules.", styles['TableCellBold'])],
        [Paragraph("<b>Staffing & Resources</b>", styles['TableCellBold']), Paragraph("Reallocation of engineering tasks across team members to maintain Kanban flow.", styles['TableCell']), Paragraph("Addition of external paid contractors or permanent team restructuring.", styles['TableCellBold'])]
    ]
    t_auth = Table(auth_data, colWidths=[90, 205, 209])
    t_auth.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_auth)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.9 Environmental Factors (EEF) & Organizational Process Assets (OPA)", styles['DocH2']))
    story.append(Paragraph(
        "<b>Enterprise Environmental Factors (EEF):</b><br/>"
        "&bull; <i>Network Heterogeneity:</i> Remote schools operate on erratic 2G/3G connectivity, requiring offline SQLite storage and background synchronization.<br/>"
        "&bull; <i>Device Fragmentation:</i> School headmasters utilize diverse hardware spanning low-cost Android phones and legacy desktop PCs.<br/>"
        "&bull; <i>Data Privacy Regulations:</i> Strict compliance with the Digital Personal Data Protection Act (DPDPA 2023) regarding minor students' personal data.<br/>"
        "<b>Organizational Process Assets (OPA):</b><br/>"
        "&bull; <i>Standard Inspection Formats:</i> Maharashtra State Education Department 10-point RTE compliance evaluation rubrics.<br/>"
        "&bull; <i>Master Data Schemas:</i> Unified District Information System for Education (UDISE+) standardized data structures.<br/>"
        "&bull; <i>Institutional Repositories:</i> MITAOE Computer Engineering GitLab templates, CI/CD pipeline definitions, and academic coding rubrics.",
        styles['DocBody']
    ))

    story.append(Paragraph("1.10 Comprehensive 8-Stakeholder Salience & Engagement Strategy", styles['DocH2']))
    stakeholder_data = [
        [Paragraph("Stakeholder Name", styles['TableHeader']), Paragraph("Role / Affiliation", styles['TableHeader']), Paragraph("Salience", styles['TableHeader']), Paragraph("Current / Target", styles['TableHeader']), Paragraph("Communication Channel", styles['TableHeader']), Paragraph("Key Engagement Strategy", styles['TableHeader'])],
        [Paragraph("MITAOE Sponsor", styles['TableCellBold']), Paragraph("Dean & Academic Board", styles['TableCell']), Paragraph("Definitive (P,L,U)", styles['TableCellBold']), Paragraph("Supportive -> Leading", styles['TableCellBold']), Paragraph("Bi-weekly Executive Briefings", styles['TableCell']), Paragraph("Present verified EVM audits & budget tracking.", styles['TableCell'])],
        [Paragraph("District DEO", styles['TableCellBold']), Paragraph("Zilla Parishad Education Dept", styles['TableCell']), Paragraph("Dominant (P,L)", styles['TableCellBold']), Paragraph("Neutral -> Supportive", styles['TableCellBold']), Paragraph("Monthly Formal Review Meetings", styles['TableCell']), Paragraph("Demonstrate compliance reporting time savings.", styles['TableCell'])],
        [Paragraph("Cluster Headmasters", styles['TableCellBold']), Paragraph("20 Pilot Cluster Schools", styles['TableCell']), Paragraph("Core User (L,U)", styles['TableCellBold']), Paragraph("Resistant -> Supportive", styles['TableCellBold']), Paragraph("Hands-on Marathi Workshops", styles['TableCell']), Paragraph("Deliver offline PWA with zero typing overhead.", styles['TableCell'])],
        [Paragraph("Primary Teachers", styles['TableCellBold']), Paragraph("150+ Rural School Educators", styles['TableCell']), Paragraph("Dependent (L,U)", styles['TableCellBold']), Paragraph("Resistant -> Neutral", styles['TableCellBold']), Paragraph("Interactive PWA Help Guides", styles['TableCell']), Paragraph("Eliminate physical registers; protect privacy.", styles['TableCell'])],
        [Paragraph("Parents & Students", styles['TableCellBold']), Paragraph("4,500+ Cluster Pupils", styles['TableCell']), Paragraph("Beneficiary (L)", styles['TableCellBold']), Paragraph("Unaware -> Supportive", styles['TableCellBold']), Paragraph("Transactional SMS Notifications", styles['TableCell']), Paragraph("Deliver instant attendance alerts via SMS.", styles['TableCell'])],
        [Paragraph("Lead Architect (PM)", styles['TableCellBold']), Paragraph("Yash Sabale (MITAOE)", styles['TableCell']), Paragraph("Definitive (P,L,U)", styles['TableCellBold']), Paragraph("Leading -> Leading", styles['TableCellBold']), Paragraph("Daily Standups & Kanban Board", styles['TableCell']), Paragraph("Enforce technical rigor, CPM schedule, & quality.", styles['TableCell'])],
        [Paragraph("Development Team", styles['TableCellBold']), Paragraph("5 Functional Engineers", styles['TableCell']), Paragraph("Core (P,L)", styles['TableCellBold']), Paragraph("Supportive -> Leading", styles['TableCellBold']), Paragraph("GitLab CI/CD & Discord Ops", styles['TableCell']), Paragraph("Maintain Little's Law WIP discipline & code reviews.", styles['TableCell'])],
        [Paragraph("Faculty Evaluator", styles['TableCellBold']), Paragraph("Course Coordinator, PM-401", styles['TableCell']), Paragraph("Dominant (P,L)", styles['TableCellBold']), Paragraph("Supportive -> Supportive", styles['TableCellBold']), Paragraph("Moodle LMS Submissions & Viva", styles['TableCell']), Paragraph("Deliver 100% compliant academic engineering evidence.", styles['TableCell'])]
    ]
    t_sh = Table(stakeholder_data, colWidths=[74, 90, 72, 74, 90, 104])
    t_sh.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_sh)

    # ==========================================
    # LANDSCAPE PAGES 2 & 3: ORG STRUCTURE & STAKEHOLDER MATRIX
    # ==========================================
    story.append(NextPageTemplate('Landscape'))
    story.append(PageBreak())
    story.append(Paragraph("Figure 1.2: Project Governance & Institutional Team Organization Structure", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_1_WBS/Diagrams/project_organization_structure.png", width=9.8*inch, height=5.5*inch))
    story.append(Paragraph("The governance structure establishes clear reporting lines from the MITAOE Steering Committee down to the Project Manager and 5 functional engineering leads. District Working Groups provide structured weekly operational feedback.", styles['DocCallout']))

    story.append(PageBreak())
    story.append(Paragraph("Figure 1.3: Stakeholder Power-Interest Matrix (2x2 Grid with Profile Details)", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_1_WBS/Diagrams/stakeholder_matrix.png", width=9.5*inch, height=5.5*inch))
    story.append(Paragraph("Stakeholders are classified into four actionable quadrants. High-power, high-interest actors (MITAOE Sponsor, DEO, Project Manager) are managed closely with bi-weekly milestone reviews. Primary school teachers and parents are kept informed through intuitive PWA guides and transactional SMS notifications.", styles['DocCallout']))

    # ==========================================
    # RETURN TO PORTRAIT: CHAPTER 2 (WBS METHODOLOGY)
    # ==========================================
    story.append(NextPageTemplate('Portrait'))
    story.append(PageBreak())

    story.append(Paragraph("2. Work Breakdown Structure (WBS) Methodology & 100% Rule", styles['DocH1']))
    story.append(Paragraph("2.1 Theoretical Framework & 100% Rule Scope Closure", styles['DocH2']))
    story.append(Paragraph(
        "A Work Breakdown Structure (WBS) is a deliverable-oriented hierarchical decomposition of the total scope of work to be carried out by the project team. In accordance with PMBOK Guide 7th Edition and ISO 21500 standards, ShalaConnect applies the **100% Rule**: the sum of the work at child levels completely and exhaustively represents 100% of the work defined at the parent level. No work outside the scope is included, and no necessary work is omitted.",
        styles['DocBody']
    ))
    story.append(Paragraph(
        "Decomposition logic follows a 3-tier hierarchy:<br/>"
        "&bull; <b>Level 1 (Phases):</b> Major project lifecycle stages representing sequential control points (1.1 to 1.5).<br/>"
        "&bull; <b>Level 2 (Deliverables):</b> Verifiable architectural and business subsystems produced within each phase.<br/>"
        "&bull; <b>Level 3 (Work Packages):</b> Lowest-level independent, measurable units of work that can be scheduled, cost-estimated, monitored, and controlled (1.1.1 to 1.5.2).",
        styles['DocBody']
    ))

    story.append(Paragraph("2.2 MECE Decomposition & Boundary Integrity", styles['DocH2']))
    story.append(Paragraph(
        "To ensure managerial clarity and prevent double-counting of expenditures, all 21 work packages strictly adhere to the **MECE Principle** (Mutually Exclusive and Collectively Exhaustive):<br/>"
        "1. <b>Mutually Exclusive:</b> No two work packages overlap in scope, deliverables, or allocated labor hours. Each task has a distinct owner and single point of accountability.<br/>"
        "2. <b>Collectively Exhaustive:</b> When all 21 work packages are completed, 100% of the software platform is delivered, satisfying all functional and non-functional requirements.<br/>"
        "3. <b>Decomposition Granularity:</b> Work package sizes conform to the '8/80 Rule' (durations between 24 hours / 3 working days and 48 hours / 6 working days), ensuring manageable operational tracking.",
        styles['DocBody']
    ))

    # ==========================================
    # LANDSCAPE PAGES 4, 5, 6, 7: WBS MASTER & DETAILED SUB-TREES
    # ==========================================
    story.append(NextPageTemplate('Landscape'))
    story.append(PageBreak())
    story.append(Paragraph("Figure 1.4: Level 1 & Level 2 Master Work Breakdown Structure (100% Rule Architecture)", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_1_WBS/Diagrams/wbs_hierarchy.png", width=9.8*inch, height=5.5*inch))
    story.append(Paragraph("Master WBS hierarchy showing complete decomposition from root 1.0 down across 5 Level-1 phases and 10 Level-2 deliverables, capturing 100% of the authorized project baseline.", styles['DocCallout']))

    story.append(PageBreak())
    story.append(Paragraph("Figure 1.5: Detailed WBS Sub-Tree: Phases 1.0 (Inception) & 2.0 (Foundation Infrastructure)", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_1_WBS/Diagrams/wbs_phase1_2_detail.png", width=9.8*inch, height=5.5*inch))
    story.append(Paragraph("Detailed work package decomposition for Phase 1.0 (Requirements, Architecture, Compliance) and Phase 2.0 (Database Schema, Cloud VPC, Spring Boot, Docker Containerization) showing deliverables, durations, costs, and predecessors.", styles['DocCallout']))

    story.append(PageBreak())
    story.append(Paragraph("Figure 1.6: Detailed WBS Sub-Tree: Phase 3.0 (Core Educational Services Modules)", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_1_WBS/Diagrams/wbs_phase3_detail.png", width=9.8*inch, height=5.5*inch))
    story.append(Paragraph("Detailed work package decomposition for Phase 3.0 comprising 9 core functional modules (1.3.1 to 1.3.9), aggregating INR 1,49,000 in baseline budget and 40 working days of engineering effort.", styles['DocCallout']))

    story.append(PageBreak())
    story.append(Paragraph("Figure 1.7: Detailed WBS Sub-Tree: Phases 4.0 (Testing & QA) & 5.0 (Deployment & Handover)", styles['FigureCaption']))
    story.append(Image("Project_Management_Submissions/Assignment_1_WBS/Diagrams/wbs_phase4_5_detail.png", width=9.8*inch, height=5.5*inch))
    story.append(Paragraph("Detailed work package decomposition for Phase 4.0 (Playwright E2E, JMeter Load Testing, OWASP Pentest) and Phase 5.0 (Pilot District UAT, Production Handover) establishing final quality gates.", styles['DocCallout']))

    # ==========================================
    # RETURN TO PORTRAIT: CHAPTER 3 (WBS DICTIONARY)
    # ==========================================
    story.append(NextPageTemplate('Portrait'))
    story.append(PageBreak())

    story.append(Paragraph("3. Detailed Work Breakdown Structure (WBS) Dictionary", styles['DocH1']))
    story.append(Paragraph(
        "The WBS Dictionary provides detailed operational parameters, technical specifications, acceptance criteria, allocated budgets, and assigned resource roles for all 21 lowest-level work packages:",
        styles['DocBody']
    ))

    dict_headers = [Paragraph("WBS Code", styles['TableHeader']), Paragraph("Work Package Title", styles['TableHeader']),
                    Paragraph("Deliverable Description", styles['TableHeader']), Paragraph("Acceptance Criteria", styles['TableHeader']),
                    Paragraph("Assigned Role", styles['TableHeader']), Paragraph("Dur", styles['TableHeader']), Paragraph("Cost (INR)", styles['TableHeader'])]
    
    dict_rows = [
        ["1.1.1", "Requirements Gathering", "SRS v1.0, user persona catalog, cluster baseline data", "Signed off by DEO and MITAOE Sponsor", "Lead Analyst", "3d", "18,000"],
        ["1.1.2", "System Architecture & Specs", "C4 architecture blueprints, API specs, database ERD", "Peer-reviewed by Solutions Architect", "Architect", "4d", "24,000"],
        ["1.1.3", "Government Compliance", "DPDPA 2023 checklist, NEP 2020 alignment matrix", "Signed legal compliance checklist", "Compliance", "3d", "18,000"],
        ["1.2.1", "Database Schema & Multi-Tenant", "PostgreSQL 16 DDL, Liquibase migration scripts", "Passes SQL linting; zero circular keys", "DBA Lead", "4d", "30,000"],
        ["1.2.2", "Cloud VPC & Terraform", "Terraform IAC modules for VPC, subnets, ALB, S3", "Clean terraform apply in AWS sandbox", "DevOps Lead", "5d", "36,000"],
        ["1.2.3", "Spring Boot Core Services", "Spring Boot 3.2 scaffolding, JWT auth filter, JPA", "Clean Maven build; 0 high CVEs", "Backend Lead", "5d", "42,000"],
        ["1.2.4", "Docker & ECS Fargate", "Multi-stage Dockerfile, ECS Fargate task defs", "Image < 180MB; container starts <15s", "DevOps Lead", "4d", "24,000"],
        ["1.3.1", "Auth & RBAC Engine", "JWT token lifecycle, BCrypt hashing, role filters", "100% pass on OWASP auth test suite", "Security Lead", "4d", "30,000"],
        ["1.3.2", "School Registry Profile", "School profile CRUD APIs, UDISE+ validation", "API latency < 200ms p95 roundtrip", "Backend Dev", "5d", "26,500"],
        ["1.3.3", "Teacher Allocation Module", "Teacher deployment, subject mapping, transfer logs", "Prevents double booking across schools", "Full-Stack Dev", "5d", "29,000"],
        ["1.3.4", "Student Enrollment Bulk CSV", "Student admissions, bulk CSV parser, promotion", "Parses 500 records in < 5 seconds", "Full-Stack Dev", "6d", "34,000"],
        ["1.3.5", "Attendance & Geo-Fencing PWA", "PWA attendance capture, GPS 100m geofence radius", "Rejects mock GPS; offline sync works", "Mobile Lead", "5d", "26,500"],
        ["1.3.6", "School Inspection Audit", "RTE 10-point checklist, scoring algorithm, logs", "Generates verified cluster index score", "Backend Dev", "4d", "21,500"],
        ["1.3.7", "District Analytics BI", "React 18 analytics dashboard, Chart.js KPI graphs", "Loads in < 1.2s on 3G network", "UI/UX Lead", "4d", "24,000"],
        ["1.3.8", "Document Vault & OCR", "S3 document vault, Tesseract OCR certificate parse", ">85% OCR accuracy on scan samples", "AI/ML Lead", "4d", "19,500"],
        ["1.3.9", "Automated SMS Gateway", "Transactional SMS dispatch via Twilio / SMS route", "Delivery latency < 10s for alerts", "Full-Stack Dev", "3d", "18,000"],
        ["1.4.1", "Playwright Integration Test", "Automated Playwright end-to-end integration suite", "100% pass on critical business journeys", "QA Lead", "5d", "27,000"],
        ["1.4.2", "JMeter Load & Scalability", "Apache JMeter scripts simulating 1,000 users", "p95 latency < 500ms at 500 req/sec", "DevOps / QA", "4d", "22,000"],
        ["1.4.3", "OWASP Security Pentest", "OWASP ZAP scan, SonarQube static analysis", "Zero High/Critical bugs; Quality Gate A", "Security Lead", "3d", "18,500"],
        ["1.5.1", "Pilot District UAT", "UAT execution across 20 cluster school headmasters", "100% Sev-1/2 defects resolved; signed UAT", "QA Lead", "4d", "14,500"],
        ["1.5.2", "Production DNS Cutover", "Production release, Route 53 DNS cutover, manuals", "System live; handover runbook accepted", "DevOps / PM", "5d", "21,000"]
    ]

    table_data = [dict_headers]
    for r in dict_rows:
        table_data.append([
            Paragraph(r[0], styles['TableCellBold']),
            Paragraph(r[1], styles['TableCellBold']),
            Paragraph(r[2], styles['TableCell']),
            Paragraph(r[3], styles['TableCell']),
            Paragraph(r[4], styles['TableCell']),
            Paragraph(r[5], styles['TableCellBold']),
            Paragraph(r[6], styles['TableCellBold'])
        ])

    table_data.append([
        Paragraph("TOTAL", styles['TableHeader']),
        Paragraph("21 Work Packages Aggregated", styles['TableHeader']),
        Paragraph("100% Scope Baseline Decomposed", styles['TableHeader']),
        Paragraph("All Quality Acceptance Gates Passed", styles['TableHeader']),
        Paragraph("Unified Team", styles['TableHeader']),
        Paragraph("54d CP", styles['TableHeader']),
        Paragraph("4,10,000", styles['TableHeader'])
    ])

    t_dict = Table(table_data, colWidths=[38, 92, 135, 115, 60, 26, 38], repeatRows=1)
    t_dict.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BACKGROUND', (0,-1), (-1,-1), SECONDARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_dict)
    story.append(Spacer(1, 12))

    # Work Package Detailed Profile Cards
    story.append(Paragraph("3.2 Work Package Detailed Engineering Profile Cards (Control Accounts CA-01 to CA-05)", styles['DocH2']))
    story.append(Paragraph(
        "To provide rigorous engineering clarity, comprehensive profile cards detail the inputs, work performed, outputs, acceptance criteria, tools, and technical dependencies across the five project Control Accounts:",
        styles['DocBody']
    ))

    cards_data = [
        ("Control Account CA-01: Inception & Regulatory Compliance (WBS 1.1.1 to 1.1.3 | Budget: INR 60,000)",
         "<b>Scope Description:</b> Formal stakeholder elicitation across 20 cluster schools, production of C4 architectural blueprints, and legal auditing against DPDPA 2023 and NEP 2020 guidelines.<br/>"
         "<b>Technical Inputs:</b> Maharashtra State Education Department operational guidelines, UDISE+ master schemas, RTE 2009 statutory mandate.<br/>"
         "<b>Engineering Work Performed:</b> Conducted structured interviews with DEO and headmasters; drafted System Requirements Specification (SRS v1.0); constructed system C4 container and component diagrams; authored field encryption compliance protocol.<br/>"
         "<b>Verified Deliverables:</b> Signed SRS v1.0, C4 Architecture Blueprint Document, DPDPA 2023 Legal Compliance Matrix.<br/>"
         "<b>Quality Acceptance Criteria:</b> Formal written sign-off by District Education Officer and MITAOE Academic Sponsor.<br/>"
         "<b>Assigned Roles & Duration:</b> Lead Analyst (3d), Solutions Architect (4d), Compliance Officer (3d) | Total: 10 working days."),

        ("Control Account CA-02: Foundation Infrastructure & Architecture (WBS 1.2.1 to 1.2.4 | Budget: INR 1,32,000)",
         "<b>Scope Description:</b> Provisioning cloud virtual private cloud (VPC), multi-tenant PostgreSQL 16 schema with row-level security, Spring Boot 3.2 backend scaffolding, and Docker containerization on AWS ECS Fargate.<br/>"
         "<b>Technical Inputs:</b> C4 Architecture Document, AWS Cloud Architecture best practices, PostgreSQL 16 official multi-tenancy documentation.<br/>"
         "<b>Engineering Work Performed:</b> Authored Terraform 1.7 HCL infrastructure scripts; generated Liquibase incremental database migration scripts; configured Spring Boot 3.2 application context with JWT security filter chain; built multi-stage Dockerfile.<br/>"
         "<b>Verified Deliverables:</b> Tested Terraform AWS VPC, Liquibase migration scripts, Spring Boot core microservice, production Docker image on ECR.<br/>"
         "<b>Quality Acceptance Criteria:</b> Automated Terraform deployment succeeds with zero warnings; database migrations execute cleanly; Docker image < 180MB.<br/>"
         "<b>Assigned Roles & Duration:</b> DBA Lead (4d), DevOps Lead (5d), Backend Lead (5d), DevOps Lead (4d) | Total: 18 working days."),

        ("Control Account CA-03: Core Educational Service Modules (WBS 1.3.1 to 1.3.9 | Budget: INR 1,49,000)",
         "<b>Scope Description:</b> Development of nine core application modules: Auth & RBAC, School Registry, Teacher Allocation, Student Bulk Enrollment, Offline PWA Attendance with Geofencing, School Inspection, District Analytics BI, Document Vault OCR, and SMS Alerting.<br/>"
         "<b>Technical Inputs:</b> Liquibase database schema, Spring Boot microservices, Leaflet / OpenStreetMap GPS APIs, Tesseract 5.3 OCR binary, Twilio SMS API.<br/>"
         "<b>Engineering Work Performed:</b> Programmed React 18 PWA frontend; implemented offline SQLite caching with service workers; coded GPS Haversine distance algorithm enforcing 100-meter radius; trained Tesseract OCR on sample birth certificates; integrated SMS webhooks.<br/>"
         "<b>Verified Deliverables:</b> 9 functional software modules integrated with Spring Boot REST API and React 18 user interface.<br/>"
         "<b>Quality Acceptance Criteria:</b> p95 API response time < 500ms; GPS mock-location detection blocks spoofing; CSV parser processes 500 rows < 5 seconds.<br/>"
         "<b>Assigned Roles & Duration:</b> 5 Full-Stack, Mobile, and Backend Developers | Total: 40 aggregate working days."),

        ("Control Account CA-04: Quality Assurance, Security & Pentest (WBS 1.4.1 to 1.4.3 | Budget: INR 33,500)",
         "<b>Scope Description:</b> Rigorous verification spanning end-to-end Playwright functional testing, Apache JMeter load and scalability stress testing, and OWASP ZAP security penetration testing.<br/>"
         "<b>Technical Inputs:</b> Complete integrated staging environment, Playwright test framework, Apache JMeter 5.6, OWASP ZAP 2.14.<br/>"
         "<b>Engineering Work Performed:</b> Wrote 85 Playwright automated E2E browser tests; generated JMeter test plans simulating 1,000 concurrent headmasters; executed OWASP ZAP automated vulnerability scan and SonarQube static code analysis.<br/>"
         "<b>Verified Deliverables:</b> Automated Test Execution Suite, JMeter Load Test Report, OWASP Pentest Security Audit Certificate.<br/>"
         "<b>Quality Acceptance Criteria:</b> 100% pass on critical business workflows; p95 latency < 500ms at 500 req/sec; zero High/Critical security vulnerabilities.<br/>"
         "<b>Assigned Roles & Duration:</b> QA Lead (5d), DevOps/QA Specialist (4d), Security Lead (3d) | Total: 12 working days."),

        ("Control Account CA-05: Pilot Deployment, UAT & Handover (WBS 1.5.1 to 1.5.2 | Budget: INR 35,500)",
         "<b>Scope Description:</b> On-site user acceptance testing across 20 cluster schools, resolution of user feedback, production Route 53 DNS cutover, and comprehensive operational documentation handover.<br/>"
         "<b>Technical Inputs:</b> Staging platform, verified test certificates, user operational manual, AWS production account credentials.<br/>"
         "<b>Engineering Work Performed:</b> Conducted 3 regional UAT workshops with 20 headmasters; logged and resolved 14 minor UI usability tickets; executed production Route 53 DNS migration; authored Admin & User Runbooks.<br/>"
         "<b>Verified Deliverables:</b> Signed Pilot UAT Acceptance Certificate, Live Production URL (https://shalaconnect.mitaoe.ac.in), System Handover Documentation.<br/>"
         "<b>Quality Acceptance Criteria:</b> 100% of Sev-1 and Sev-2 UAT defect tickets closed; official production cutover approved by Sponsor.<br/>"
         "<b>Assigned Roles & Duration:</b> QA Lead (4d), DevOps Lead & Project Manager (5d) | Total: 9 working days.")
    ]

    for c_title, c_desc in cards_data:
        story.append(Paragraph(c_title, styles['DocH3']))
        story.append(Paragraph(c_desc, styles['DocBody']))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Scope Baseline Governance, Verification & Change Control", styles['DocH1']))
    story.append(Paragraph("4.1 Scope Baseline Definition & 6-Step Change Control Protocol", styles['DocH2']))
    story.append(Paragraph(
        "In accordance with PMBOK Guide 7th Edition, the approved Scope Baseline comprises three formal artifacts: the **Project Scope Statement**, the **Work Breakdown Structure (WBS)**, and the **WBS Dictionary**. Any requested scope modification must strictly follow the formal 6-stage Change Control Board (CCB) protocol:",
        styles['DocBody']
    ))

    ccb_steps_data = [
        [Paragraph("Stage", styles['TableHeader']), Paragraph("Process Stage Name", styles['TableHeader']), Paragraph("Operational Procedure & Action", styles['TableHeader']), Paragraph("Decision Gate & SLA", styles['TableHeader'])],
        [Paragraph("1", styles['TableCellBold']), Paragraph("Change Request Submission", styles['TableCellBold']), Paragraph("Stakeholder submits formal Change Request Form detailing requested modification.", styles['TableCell']), Paragraph("Logged in Register (24h)", styles['TableCell'])],
        [Paragraph("2", styles['TableCellBold']), Paragraph("Technical Impact Assessment", styles['TableCellBold']), Paragraph("PM & Lead Architect evaluate impact on triple constraints (Scope, Schedule, Budget).", styles['TableCell']), Paragraph("Impact Report (48h)", styles['TableCell'])],
        [Paragraph("3", styles['TableCellBold']), Paragraph("CCB Formal Review", styles['TableCellBold']), Paragraph("Change Control Board convenes to review business justification vs project risk.", styles['TableCell']), Paragraph("CCB Meeting (72h)", styles['TableCell'])],
        [Paragraph("4", styles['TableCellBold']), Paragraph("Approval / Rejection Decision", styles['TableCellBold']), Paragraph("Formal decision signed: Approved, Rejected, or Deferred to Phase II.", styles['TableCell']), Paragraph("Written Notice (24h)", styles['TableCell'])],
        [Paragraph("5", styles['TableCellBold']), Paragraph("Baseline & Schedule Update", styles['TableCellBold']), Paragraph("PM updates WBS, WBS Dictionary, CPM schedule, and budget allocations.", styles['TableCell']), Paragraph("Baseline v1.x (24h)", styles['TableCell'])],
        [Paragraph("6", styles['TableCellBold']), Paragraph("Implementation & Verification", styles['TableCellBold']), Paragraph("Engineering team implements change; QA verifies against acceptance criteria.", styles['TableCell']), Paragraph("QA Gate Sign-Off", styles['TableCell'])]
    ]
    t_ccb = Table(ccb_steps_data, colWidths=[36, 120, 230, 98])
    t_ccb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_ccb)

    story.append(Spacer(1, 10))
    story.append(Paragraph("4.2 Scope Creep Prevention Strategy", styles['DocH2']))
    story.append(Paragraph(
        "To protect the project from unmanaged feature expansion, ShalaConnect implements four strict preventive safeguards:<br/>"
        "1. <b>Strict Requirements Traceability Matrix (RTM):</b> Every implemented feature must trace directly back to an authorized WBS Dictionary package.<br/>"
        "2. <b>Zero Unapproved Work:</b> Developers are strictly prohibited from implementing user stories not present in the current approved sprint backlog.<br/>"
        "3. <b>Scope Deferral Protocol:</b> Non-essential feature requests from school headmasters are formally documented and categorized into 'Phase II Enhancements'.<br/>"
        "4. <b>Variance Gate Audits:</b> Bi-weekly sprint reviews compare delivered software against the signed WBS Dictionary acceptance criteria.",
        styles['DocBody']
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Academic References & IEEE Bibliography", styles['DocH1']))
    refs = [
        "[1] Project Management Institute, *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*, 7th ed. Newtown Square, PA: PMI, 2021.",
        "[2] International Organization for Standardization, *ISO 21500:2021 Project, programme and portfolio management - Context and concepts*, Geneva: ISO, 2021.",
        "[3] Ministry of Education, Government of India, *National Education Policy 2020 (NEP 2020)*, New Delhi: MHRD, 2020.",
        "[4] Ministry of Law and Justice, *The Right of Children to Free and Compulsory Education Act, 2009*, Gazette of India, New Delhi, 2009.",
        "[5] Ministry of Electronics and Information Technology, *Digital Personal Data Protection Act, 2023 (DPDPA 2023)*, Gazette of India, New Delhi, 2023.",
        "[6] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Boston: Addison-Wesley, 1994.",
        "[7] M. Fowler, *Patterns of Enterprise Application Architecture*, Boston: Addison-Wesley, 2002.",
        "[8] R. C. Martin, *Clean Architecture: A Craftsman's Guide to Software Structure and Design*, Prentice Hall, 2017."
    ]
    for ref in refs:
        story.append(Paragraph(ref, styles['DocBullet']))

    doc.build(story, canvasmaker=DynamicCanvas)
    print(f"Masterpiece Expanded Assignment 1 Report successfully generated: {pdf_path}")

if __name__ == "__main__":
    build_assignment_1()
