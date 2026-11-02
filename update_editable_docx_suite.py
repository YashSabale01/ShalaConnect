import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

NAVY_HEX = "1B365D"
SLATE_HEX = "2C5282"
BORDER_HEX = "CBD5E0"
LIGHT_BG = "FFFFFF"

def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=60, right=60):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_header_footer(doc, asg_title):
    section = doc.sections[0]
    header = section.header
    hp = header.paragraphs[0]
    hp.text = f"MITAOE | PM-401 Project Management | {asg_title}"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.style.font.name = 'Calibri'
    hp.style.font.size = Pt(8.5)
    hp.style.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.text = "Author: Yash Janardan Sabale | Confidential & Academic Baseline"
    fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    fp.style.font.name = 'Calibri'
    fp.style.font.size = Pt(8.5)
    fp.style.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

def add_cover(doc, asg_num, asg_title_clean):
    for _ in range(5):
        doc.add_paragraph()

    # Subject & Assignment Title
    p_subj = doc.add_paragraph()
    p_subj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_subj = p_subj.add_run("PROJECT MANAGEMENT\n\n")
    r_subj.font.name = 'Calibri'
    r_subj.font.size = Pt(22)
    r_subj.font.bold = True
    r_subj.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    r_asg = p_subj.add_run(f"Assignment {asg_num}: {asg_title_clean}\n")
    r_asg.font.name = 'Calibri'
    r_asg.font.size = Pt(13)
    r_asg.font.bold = True
    r_asg.font.color.rgb = RGBColor(0x2C, 0x52, 0x82)

    for _ in range(5):
        doc.add_paragraph()

    # Student Details
    meta = [
        ("Name:", "Yash Janardan Sabale"),
        ("PRN:", "202301040087"),
        ("Branch:", "Computer Engineering"),
        ("Academic Year:", "2026-27"),
        ("College:", "MIT Academy of Engineering, Alandi, Pune")
    ]
    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row_idx, (lbl, val) in enumerate(meta):
        c0 = table.cell(row_idx, 0)
        c0.width = Inches(1.8)
        p0 = c0.paragraphs[0]
        p0.text = lbl
        p0.style.font.name = 'Calibri'
        p0.style.font.size = Pt(10)
        p0.style.font.bold = True
        p0.style.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

        c1 = table.cell(row_idx, 1)
        c1.width = Inches(3.8)
        p1 = c1.paragraphs[0]
        p1.text = val
        p1.style.font.name = 'Calibri'
        p1.style.font.size = Pt(10)
        p1.style.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)

        set_cell_background(c0, "FFFFFF")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 50, 50, 50, 50)
        set_cell_margins(c1, 50, 50, 50, 50)

    doc.add_page_break()

def update_asg1_docx():
    path = "Project_Management_Submissions/Assignment_1_WBS/Assignment_1_Editable.docx"
    doc = docx.Document()
    add_header_footer(doc, "Assignment 1: Project Charter, WBS & WBS Dictionary")
    add_cover(doc, "1", "Project Charter, WBS and WBS Dictionary")

    # Body
    doc.add_heading("1. Comprehensive Project Charter (PMBOK 7th Edition Standard)", level=1)
    doc.add_paragraph("ShalaConnect establishes a cloud-native educational administration backbone for rural school clusters in Maharashtra. The charter authorizes Yash Sabale as Project Manager to execute the 54-day deterministic critical path baseline within the approved INR 4,10,000 cost baseline.")

    doc.add_heading("1.1 Scope Boundaries & Exclusions", level=2)
    doc.add_paragraph("The scope baseline authorizes 7 core modules: School Registry, Teacher Allocation, Student Bulk Enrollment, Offline PWA Attendance with 100m Geofencing, School Inspection Auditing, S3 Document Vault with Tesseract OCR, and District Analytics BI Alerts.")

    img_scope = "Project_Management_Submissions/Assignment_1_WBS/Diagrams/scope_hierarchy.png"
    if os.path.exists(img_scope):
        doc.add_paragraph("Figure 1.1: ShalaConnect Scope Hierarchy & Project Boundaries")
        doc.add_picture(img_scope, width=Inches(6.5))

    doc.add_heading("1.2 Stakeholder Power-Interest Matrix", level=2)
    doc.add_paragraph("Stakeholders are classified across a 2x2 grid to enforce tailored communication frequencies:")
    img_stk = "Project_Management_Submissions/Assignment_1_WBS/Diagrams/stakeholder_matrix.png"
    if os.path.exists(img_stk):
        doc.add_paragraph("Figure 1.2: Stakeholder Power-Interest 2x2 Grid")
        doc.add_picture(img_stk, width=Inches(6.5))

    doc.add_heading("1.3 Project Governance & Organization Hierarchy", level=2)
    img_org = "Project_Management_Submissions/Assignment_1_WBS/Diagrams/project_organization_structure.png"
    if os.path.exists(img_org):
        doc.add_paragraph("Figure 1.3: Institutional Project Governance Structure")
        doc.add_picture(img_org, width=Inches(6.5))

    doc.add_heading("2. Deliverable-Oriented Work Breakdown Structure (100% Rule)", level=1)
    doc.add_paragraph("Decomposed across 5 Level-1 Phases, 10 Level-2 Deliverables, and 21 Level-3 Work Packages:")
    img_wbs = "Project_Management_Submissions/Assignment_1_WBS/Diagrams/wbs_hierarchy.png"
    if os.path.exists(img_wbs):
        doc.add_paragraph("Figure 1.4: Master Hierarchical Work Breakdown Structure (100% Rule)")
        doc.add_picture(img_wbs, width=Inches(6.5))

    doc.add_heading("3. Detailed WBS Dictionary (21 Work Packages)", level=1)
    doc.add_paragraph("Every lowest-level work package is measurable, bounded, cost-estimated, and assigned to a single accountable lead role. Detailed multi-column definitions are recorded in WBS_Dictionary.xlsx.")

    doc.save(path)
    print(f"Updated Word DOCX: {path}")

def update_asg2_docx():
    path = "Project_Management_Submissions/Assignment_2_Project_Plan/Assignment_2_Editable.docx"
    doc = docx.Document()
    add_header_footer(doc, "Assignment 2: Project Plan, Critical Path and Budget Estimation")
    add_cover(doc, "2", "Project Plan, Critical Path and Budget Estimation")

    doc.add_heading("1. Activity Definition & Critical Path Method (CPM)", level=1)
    doc.add_paragraph("The deterministic CPM schedule comprises 21 activities derived directly from the WBS Dictionary. Standard forward and backward passes establish an unyielding 54-working-day critical path across 13 zero-float activities.")

    img_aon = "Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/aon_network_diagram.png"
    if os.path.exists(img_aon):
        doc.add_paragraph("Figure 2.1: Activity-on-Node (AON) Network Diagram with Standard 7-Block CPM Nodes")
        doc.add_picture(img_aon, width=Inches(6.5))

    img_cp = "Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/critical_path_traversal.png"
    if os.path.exists(img_cp):
        doc.add_paragraph("Figure 2.2: Dedicated Critical Path Linear Traversal (Day 0 to Day 54)")
        doc.add_picture(img_cp, width=Inches(6.5))

    doc.add_heading("2. Schedule Baseline Gantt Chart & Resource Allocation", level=1)
    img_gantt = "Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/gantt_chart.png"
    if os.path.exists(img_gantt):
        doc.add_paragraph("Figure 2.3: 16-Week Schedule Baseline Gantt Chart (Critical Path in Red)")
        doc.add_picture(img_gantt, width=Inches(6.5))

    img_res = "Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/resource_allocation_chart.png"
    if os.path.exists(img_res):
        doc.add_paragraph("Figure 2.4: Resource Allocation & Weekly Staffing Workload Histogram")
        doc.add_picture(img_res, width=Inches(6.5))

    doc.add_heading("3. Bottom-Up Budget Aggregation & S-Curve Baseline", level=1)
    img_b = "Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/budget_breakdown_chart.png"
    if os.path.exists(img_b):
        doc.add_paragraph("Figure 2.5: Cost Baseline Aggregation & Budget Breakdown Charts")
        doc.add_picture(img_b, width=Inches(6.5))

    img_sc = "Project_Management_Submissions/Assignment_2_Project_Plan/Diagrams/scurve_chart.png"
    if os.path.exists(img_sc):
        doc.add_paragraph("Figure 2.6: Time-Phased Cumulative Expenditure S-Curve Baseline")
        doc.add_picture(img_sc, width=Inches(6.5))

    doc.save(path)
    print(f"Updated Word DOCX: {path}")

def update_asg3_docx():
    path = "Project_Management_Submissions/Assignment_3_Kanban_Control/Assignment_3_Editable.docx"
    doc = docx.Document()
    add_header_footer(doc, "Assignment 3: Kanban Board and Execution Control Plan")
    add_cover(doc, "3", "Kanban Board and Execution Control Plan")

    doc.add_heading("1. Agile Kanban Execution Framework & Little's Law", level=1)
    doc.add_paragraph("ShalaConnect applies a 5-column Kanban pull system. Little's Law (WIP = Throughput x Cycle Time) mathematically proves that capping in-flight WIP to 6 tasks compresses cycle time from 34.3 days to 16.2 days (52.8% latency reduction).")

    img_k = "Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams/kanban_workflow_diagram.png"
    if os.path.exists(img_k):
        doc.add_paragraph("Figure 3.1: Agile Kanban 5-Column Workflow Architecture with Enforced WIP Limits")
        doc.add_picture(img_k, width=Inches(6.5))

    doc.add_heading("2. Responsibility Assignment Matrix (RACI)", level=1)
    img_r = "Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams/raci_matrix_diagram.png"
    if os.path.exists(img_r):
        doc.add_paragraph("Figure 3.2: Comprehensive RACI Responsibility Assignment Heatmap")
        doc.add_picture(img_r, width=Inches(6.5))

    doc.add_heading("3. Day 35 Earned Value Management (EVM) Performance Audit", level=1)
    doc.add_paragraph("Mid-project audit at Day 35 confirms favorable cost efficiency (CPI = 1.050, CV = +INR 14,143) and minor non-critical schedule lag (SPI = 0.928) absorbed by the 26-day operational buffer. Forecasted EAC is INR 3,90,476 (INR 19,524 surplus).")

    img_evm = "Project_Management_Submissions/Assignment_3_Kanban_Control/Diagrams/evm_scurve_analysis.png"
    if os.path.exists(img_evm):
        doc.add_paragraph("Figure 3.3: Day 35 EVM Performance S-Curve Analysis (PV, EV, AC, and EAC Forecast)")
        doc.add_picture(img_evm, width=Inches(6.5))

    doc.save(path)
    print(f"Updated Word DOCX: {path}")

def update_asg4_docx():
    path = "Project_Management_Submissions/Assignment_4_Risk_Management/Assignment_4_Editable.docx"
    doc = docx.Document()
    add_header_footer(doc, "Assignment 4: Risk Management Plan and Risk Register")
    add_cover(doc, "4", "Risk Management Plan and Risk Register")

    doc.add_heading("1. Risk Governance & Breakdown Structure (RBS)", level=1)
    doc.add_paragraph("Risk management follows PMBOK Guide 7th Edition and ISO 31000 standards. Risks are structured across 4 RBS categories: Technical, External, Organizational, and Project Management.")

    img_rbs = "Project_Management_Submissions/Assignment_4_Risk_Management/Diagrams/risk_breakdown_structure.png"
    if os.path.exists(img_rbs):
        doc.add_paragraph("Figure 4.1: Hierarchical Risk Breakdown Structure (RBS) Taxonomy")
        doc.add_picture(img_rbs, width=Inches(6.5))

    doc.add_heading("2. Quantitative 5x5 Probability-Impact Heatmap Matrix", level=1)
    img_pi = "Project_Management_Submissions/Assignment_4_Risk_Management/Diagrams/probability_impact_matrix.png"
    if os.path.exists(img_pi):
        doc.add_paragraph("Figure 4.2: 5x5 Probability-Impact Heatmap Matrix (All 20 Risks Plotted)")
        doc.add_picture(img_pi, width=Inches(6.5))

    doc.add_heading("3. Risk Response Playbooks & Residual Score Reduction", level=1)
    doc.add_paragraph("Playbooks for top threats (RSK-01 to RSK-05) compress financial exposure by 69.6% from INR 67,200 down to INR 20,400, fully covered by the INR 41,000 Contingency Reserve.")

    img_resp = "Project_Management_Submissions/Assignment_4_Risk_Management/Diagrams/risk_response_dashboard.png"
    if os.path.exists(img_resp):
        doc.add_paragraph("Figure 4.3: Pre- vs. Post-Mitigation Risk Score Reduction Dashboard")
        doc.add_picture(img_resp, width=Inches(6.5))

    doc.save(path)
    print(f"Updated Word DOCX: {path}")

if __name__ == "__main__":
    update_asg1_docx()
    update_asg2_docx()
    update_asg3_docx()
    update_asg4_docx()
    print("All editable Word documents successfully updated with minimal cover page!")
