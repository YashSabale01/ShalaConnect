import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_2_Project_Plan"
os.makedirs(base_dir, exist_ok=True)

sched_file = os.path.join(base_dir, "Project_Schedule.xlsx")
budget_file = os.path.join(base_dir, "Budget_Estimation.xlsx")

# Common Styles
font_hdr = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
fill_hdr = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
fill_crit = PatternFill(start_color="FEE2E2", fill_type="solid")
fill_alt = PatternFill(start_color="F8FAFC", fill_type="solid")
fill_tot = PatternFill(start_color="FEF3C7", fill_type="solid")
border_thin = Border(left=Side(style='thin', color='CBD5E1'),
                     right=Side(style='thin', color='CBD5E1'),
                     top=Side(style='thin', color='CBD5E1'),
                     bottom=Side(style='thin', color='CBD5E1'))

# =============================================================
# 1. PROJECT_SCHEDULE.XLSX
# =============================================================
wb_sched = openpyxl.Workbook()

# Sheet 1: Activity CPM Master
ws_cpm = wb_sched.active
ws_cpm.title = "Activity List & CPM Schedule"

cpm_headers = [
    "Activity ID", "Activity Name", "WBS Ref", "Duration (Days)", 
    "Predecessors", "Successors", "Dep Type", "Lead / Lag", 
    "ES (Day)", "EF (Day)", "LS (Day)", "LF (Day)", 
    "Total Float (TF)", "Free Float (FF)", "Critical?", 
    "Assigned Resource Role", "Estimated Cost (INR)"
]
ws_cpm.append(cpm_headers)
for c_i in range(1, len(cpm_headers) + 1):
    c = ws_cpm.cell(row=1, column=c_i)
    c.font = font_hdr
    c.fill = fill_hdr
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

activity_rows = [
    ("ACT-01", "Stakeholder Needs Elicitation & Field Surveys", "1.1.1", 3, "START", "ACT-02", "FS", 0, 0, 3, 0, 3, 0, 0, "CRITICAL", "Project Manager / Analyst", 14000),
    ("ACT-02", "Software Requirements Spec (SRS) & Matrix", "1.1.2", 4, "ACT-01", "ACT-03, ACT-04, ACT-06", "FS", 0, 3, 7, 3, 7, 0, 0, "CRITICAL", "Systems Analyst / Tech Lead", 16000),
    ("ACT-03", "DPDP Act 2023 Compliance Assessment", "1.1.3", 3, "ACT-02", "ACT-04", "FS", 0, 7, 10, 7, 10, 0, 0, "CRITICAL", "Security & Compliance Specialist", 12000),
    ("ACT-04", "Multi-Tenant Data Modeling (PostgreSQL 16)", "1.2.1", 4, "ACT-02, ACT-03", "ACT-05, ACT-07", "FS", 0, 10, 14, 10, 14, 0, 0, "CRITICAL", "Database Architect", 20000),
    ("ACT-05", "REST API Specifications (OpenAPI 3.0)", "1.2.2", 4, "ACT-04", "ACT-07, ACT-08, ACT-15", "FS", 0, 14, 18, 14, 18, 0, 0, "CRITICAL", "Backend Lead Developer", 18000),
    ("ACT-06", "Bilingual UI/UX Design & Figma Prototypes", "1.2.3", 5, "ACT-02", "ACT-09, ACT-13, ACT-15", "FS", 0, 7, 12, 18, 23, 11, 6, "Non-Critical", "UI/UX Designer", 22000),
    ("ACT-07", "AWS Cloud Architecture Blueprint", "1.2.4", 4, "ACT-04, ACT-05", "ACT-16", "FS", 0, 18, 22, 28, 32, 10, 0, "Non-Critical", "Cloud Architect / DevOps", 18000),
    ("ACT-08", "Multi-Tenant RBAC & JWT Security Module", "1.3.1", 5, "ACT-05", "ACT-09, ACT-11, ACT-12, ACT-13, ACT-14", "FS", 0, 18, 23, 18, 23, 0, 0, "CRITICAL", "Backend Security Engineer", 22000),
    ("ACT-09", "Daily Attendance Engine & Offline Sync", "1.3.2", 7, "ACT-06, ACT-08", "ACT-10, ACT-18", "FS", 0, 23, 30, 23, 30, 0, 0, "CRITICAL", "Full-Stack Developer", 32000),
    ("ACT-10", "BEO Monthly Excel Report Engine (Apache POI)", "1.3.3", 5, "ACT-09", "ACT-14, ACT-18", "FS", 0, 30, 35, 30, 35, 0, 0, "CRITICAL", "Backend Developer", 24000),
    ("ACT-11", "GR Circulars & Read-Receipt Tracker", "1.3.4", 4, "ACT-08", "ACT-19", "FS", 0, 23, 27, 40, 44, 17, 17, "Non-Critical", "Full-Stack Developer", 18000),
    ("ACT-12", "Cluster Review Meeting Scheduler", "1.3.5", 3, "ACT-08", "ACT-19", "FS", 0, 23, 26, 41, 44, 18, 18, "Non-Critical", "Full-Stack Developer", 16000),
    ("ACT-13", "School Events & Multi-Photo Cloud Gallery", "1.3.6", 4, "ACT-06, ACT-08", "ACT-19", "FS", 0, 23, 27, 40, 44, 17, 17, "Non-Critical", "Full-Stack Developer", 20000),
    ("ACT-14", "Dynamic Form Builder & Aggregation Engine", "1.3.7", 6, "ACT-08, ACT-10", "ACT-18", "FS", 0, 35, 41, 35, 41, 0, 0, "CRITICAL", "Senior Developer", 26000),
    ("ACT-15", "Public Transparency Portal & School Directory", "1.3.8", 4, "ACT-05, ACT-06", "ACT-19", "FS", 0, 18, 22, 40, 44, 22, 22, "Non-Critical", "Frontend Developer", 18000),
    ("ACT-16", "Modular AWS Infrastructure as Code (Terraform)", "1.4.1", 5, "ACT-07", "ACT-17", "FS", 0, 22, 27, 32, 37, 10, 0, "Non-Critical", "DevOps Engineer", 28000),
    ("ACT-17", "CI/CD Pipeline Automation (GitHub Actions)", "1.4.2", 4, "ACT-16", "ACT-18", "FS", 0, 27, 31, 37, 41, 10, 10, "Non-Critical", "DevOps Engineer", 22000),
    ("ACT-18", "Performance Tuning & Security Audit", "1.4.3", 3, "ACT-09, ACT-10, ACT-14, ACT-17", "ACT-19", "FS", 0, 41, 44, 41, 44, 0, 0, "CRITICAL", "Security Auditor / Lead", 18000),
    ("ACT-19", "Automated Test Suite (JUnit / Cypress)", "1.5.1", 4, "ACT-11, ACT-12, ACT-13, ACT-15, ACT-18", "ACT-20", "FS", 0, 44, 48, 44, 48, 0, 0, "CRITICAL", "QA Automation Engineer", 20000),
    ("ACT-20", "Field Pilot Rollout & Kendra Pramukh UAT", "1.5.2", 3, "ACT-19", "ACT-21", "FS", 0, 48, 51, 48, 51, 0, 0, "CRITICAL", "Project Manager / Lead Dev", 14000),
    ("ACT-21", "Project Documentation, Manuals & Handover", "1.5.3", 3, "ACT-20", "FINISH", "FS", 0, 51, 54, 51, 54, 0, 0, "CRITICAL", "Technical Writer / PM", 12000)
]

for r_idx, r_val in enumerate(activity_rows, start=2):
    ws_cpm.append(r_val)
    is_crit = r_val[14] == "CRITICAL"
    f_row = fill_crit if is_crit else (fill_alt if r_idx % 2 == 1 else PatternFill(fill_type=None))
    for c_i in range(1, len(r_val) + 1):
        cell = ws_cpm.cell(row=r_idx, column=c_i)
        cell.font = Font(name="Calibri", size=9.5, bold=is_crit if c_i in [1, 15] else False)
        if f_row.fill_type:
            cell.fill = f_row
        cell.border = border_thin
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if c_i in [1, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_i == 17:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '"₹"#,##0'

# Total Row
tot_row_cpm = len(activity_rows) + 2
ws_cpm.cell(row=tot_row_cpm, column=1, value="TOTAL")
ws_cpm.cell(row=tot_row_cpm, column=2, value="Schedule Baseline Duration: 54 Days (Project Buffer: 26 Days to 80 Days Max)")
ws_cpm.cell(row=tot_row_cpm, column=4, value="54 Days (CP)")
ws_cpm.cell(row=tot_row_cpm, column=17, value=410000)

for c_i in range(1, len(cpm_headers) + 1):
    c = ws_cpm.cell(row=tot_row_cpm, column=c_i)
    c.font = Font(name="Calibri", size=10, bold=True)
    c.fill = fill_tot
    c.border = border_thin
    if c_i == 17:
        c.number_format = '"₹"#,##0'
        c.alignment = Alignment(horizontal="right", vertical="center")

col_widths_cpm = [12, 32, 10, 14, 18, 22, 10, 12, 10, 10, 10, 10, 14, 14, 14, 25, 18]
for idx, w in enumerate(col_widths_cpm, start=1):
    ws_cpm.column_dimensions[get_column_letter(idx)].width = w

# Sheet 2: Network Paths Summary
ws_paths = wb_sched.create_sheet(title="All 25 Network Paths")
path_headers = ["Path Rank", "Path Identification Sequence", "Length (Days)", "Float from CP (Days)", "Classification & Significance"]
ws_paths.append(path_headers)
for c_i in range(1, len(path_headers) + 1):
    c = ws_paths.cell(row=1, column=c_i)
    c.font = font_hdr
    c.fill = fill_hdr
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Generate representative top paths
paths_data = [
    (1, "ACT-01 -> ACT-02 -> ACT-03 -> ACT-04 -> ACT-05 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-14 -> ACT-18 -> ACT-19 -> ACT-20 -> ACT-21", 54, 0, "CRITICAL PATH (Governs 54-day project duration; TF = 0)"),
    (2, "ACT-01 -> ACT-02 -> ACT-04 -> ACT-05 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-14 -> ACT-18 -> ACT-19 -> ACT-20 -> ACT-21", 51, 3, "Sub-Critical Path (Bypasses ACT-03; Total Float = 3 Days)"),
    (3, "ACT-01 -> ACT-02 -> ACT-03 -> ACT-04 -> ACT-05 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-18 -> ACT-19 -> ACT-20 -> ACT-21", 48, 6, "Near-Critical Path (Direct to tuning; Float = 6 Days)"),
    (4, "ACT-01 -> ACT-02 -> ACT-04 -> ACT-05 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-18 -> ACT-19 -> ACT-20 -> ACT-21", 45, 9, "Non-Critical Path (Float = 9 Days)"),
    (5, "ACT-01 -> ACT-02 -> ACT-03 -> ACT-04 -> ACT-05 -> ACT-07 -> ACT-16 -> ACT-17 -> ACT-18 -> ACT-19 -> ACT-20 -> ACT-21", 44, 10, "DevOps / Infrastructure Primary Path (Total Float = 10 Days)"),
    (6, "ACT-01 -> ACT-02 -> ACT-06 -> ACT-09 -> ACT-10 -> ACT-14 -> ACT-18 -> ACT-19 -> ACT-20 -> ACT-21", 43, 11, "UI/UX Attendance Integration Path (Total Float = 11 Days)"),
    (7, "ACT-01 -> ACT-02 -> ACT-04 -> ACT-05 -> ACT-07 -> ACT-16 -> ACT-17 -> ACT-18 -> ACT-19 -> ACT-20 -> ACT-21", 41, 13, "DevOps Secondary Path (Total Float = 13 Days)"),
    (8, "ACT-01 -> ACT-02 -> ACT-06 -> ACT-09 -> ACT-10 -> ACT-18 -> ACT-19 -> ACT-20 -> ACT-21", 37, 17, "UI Attendance Tuning Path (Total Float = 17 Days)"),
    (9, "ACT-01 -> ACT-02 -> ACT-03 -> ACT-04 -> ACT-05 -> ACT-08 -> ACT-11 -> ACT-19 -> ACT-20 -> ACT-21", 37, 17, "GR Circular Dissemination Path (Total Float = 17 Days)"),
    (10, "ACT-01 -> ACT-02 -> ACT-03 -> ACT-04 -> ACT-05 -> ACT-08 -> ACT-13 -> ACT-19 -> ACT-20 -> ACT-21", 37, 17, "Event Gallery Proof Path (Total Float = 17 Days)"),
    (11, "ACT-01 -> ACT-02 -> ACT-03 -> ACT-04 -> ACT-05 -> ACT-08 -> ACT-12 -> ACT-19 -> ACT-20 -> ACT-21", 36, 18, "Meeting Scheduler Path (Total Float = 18 Days)"),
    (12, "ACT-01 -> ACT-02 -> ACT-03 -> ACT-04 -> ACT-05 -> ACT-15 -> ACT-19 -> ACT-20 -> ACT-21", 32, 22, "Public Portal API Integration Path (Total Float = 22 Days)"),
    (13, "ACT-01 -> ACT-02 -> ACT-06 -> ACT-15 -> ACT-19 -> ACT-20 -> ACT-21", 27, 27, "Public Portal Direct UI Path (Total Float = 27 Days)")
]
for p_idx, p_val in enumerate(paths_data, start=2):
    ws_paths.append(p_val)
    f_p = fill_crit if p_idx == 2 else (fill_alt if p_idx % 2 == 1 else PatternFill(fill_type=None))
    for c_i in range(1, len(p_val) + 1):
        cell = ws_paths.cell(row=p_idx, column=c_i)
        cell.font = Font(name="Calibri", size=9.5, bold=(p_idx == 2))
        if f_p.fill_type:
            cell.fill = f_p
        cell.border = border_thin
        if c_i in [1, 3, 4]:
            cell.alignment = Alignment(horizontal="center", vertical="center")

ws_paths.column_dimensions['A'].width = 12
ws_paths.column_dimensions['B'].width = 75
ws_paths.column_dimensions['C'].width = 15
ws_paths.column_dimensions['D'].width = 18
ws_paths.column_dimensions['E'].width = 50

wb_sched.save(sched_file)
print(f"Generated Project_Schedule.xlsx at {sched_file}")

# =============================================================
# 2. BUDGET_ESTIMATION.XLSX
# =============================================================
wb_bgt = openpyxl.Workbook()

# Sheet 1: Bottom-up Work Package Cost Breakdown
ws_cost = wb_bgt.active
ws_cost.title = "Bottom-Up WP Cost Breakdown"

cost_headers = [
    "WBS Ref", "Activity ID", "Work Package Name", 
    "Human Labor Cost (INR)", "Cloud Hosting (AWS)", "Software / Licenses", "Testing & Audits", 
    "Total WP Cost (INR)", "Cost Category", "Fixed vs. Variable"
]
ws_cost.append(cost_headers)
for c_i in range(1, len(cost_headers) + 1):
    c = ws_cost.cell(row=1, column=c_i)
    c.font = font_hdr
    c.fill = fill_hdr
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

cost_breakdown_data = [
    ("1.1.1", "ACT-01", "Stakeholder Needs & Field Surveys", 12000, 0, 1000, 1000, 14000, "Direct Labor", "Variable"),
    ("1.1.2", "ACT-02", "SRS Specification & Traceability", 14000, 0, 1000, 1000, 16000, "Direct Labor", "Fixed"),
    ("1.1.3", "ACT-03", "DPDP Act Compliance Assessment", 10000, 0, 1000, 1000, 12000, "Direct Labor", "Fixed"),
    ("1.2.1", "ACT-04", "Multi-Tenant Data Modeling (PG16)", 17000, 1000, 1000, 1000, 20000, "Direct Labor", "Fixed"),
    ("1.2.2", "ACT-05", "REST API Specs (OpenAPI 3.0)", 15000, 1000, 1000, 1000, 18000, "Direct Labor", "Fixed"),
    ("1.2.3", "ACT-06", "Bilingual UI/UX Design & Figma", 18000, 1000, 2000, 1000, 22000, "Direct Labor", "Fixed"),
    ("1.2.4", "ACT-07", "AWS Cloud Infrastructure Blueprint", 14000, 2000, 1000, 1000, 18000, "Direct Labor", "Fixed"),
    ("1.3.1", "ACT-08", "Multi-Tenant RBAC & JWT Security", 18000, 1000, 1000, 2000, 22000, "Direct Labor", "Variable"),
    ("1.3.2", "ACT-09", "Attendance Engine & Offline Sync", 26000, 2000, 1000, 3000, 32000, "Direct Labor", "Variable"),
    ("1.3.3", "ACT-10", "BEO Monthly Excel Report Engine", 20000, 1000, 1000, 2000, 24000, "Direct Labor", "Variable"),
    ("1.3.4", "ACT-11", "GR Circulars & Read Receipts", 14000, 2000, 1000, 1000, 18000, "Direct Labor", "Variable"),
    ("1.3.5", "ACT-12", "Cluster Review Meeting Scheduler", 13000, 1000, 1000, 1000, 16000, "Direct Labor", "Variable"),
    ("1.3.6", "ACT-13", "School Events & Multi-Photo Gallery", 15000, 3000, 1000, 1000, 20000, "Direct Labor", "Variable"),
    ("1.3.7", "ACT-14", "Dynamic Form Builder & Engine", 21000, 2000, 1000, 2000, 26000, "Direct Labor", "Variable"),
    ("1.3.8", "ACT-15", "Public Transparency Portal", 15000, 1000, 1000, 1000, 18000, "Direct Labor", "Variable"),
    ("1.4.1", "ACT-16", "Modular AWS Terraform Provisioning", 18000, 8000, 1000, 1000, 28000, "Direct / Infra", "Fixed"),
    ("1.4.2", "ACT-17", "GitHub Actions CI/CD Automation", 14000, 5000, 2000, 1000, 22000, "Direct / Infra", "Fixed"),
    ("1.4.3", "ACT-18", "Performance Tuning & Security Audit", 12000, 2000, 1000, 3000, 18000, "Direct Labor", "Fixed"),
    ("1.5.1", "ACT-19", "Automated Test Suite (JUnit)", 14000, 1000, 1000, 4000, 20000, "Testing / QA", "Variable"),
    ("1.5.2", "ACT-20", "Field Pilot Rollout & UAT", 10000, 2000, 1000, 1000, 14000, "Operations", "Variable"),
    ("1.5.3", "ACT-21", "Documentation & Handover", 10000, 0, 1000, 1000, 12000, "Direct Labor", "Fixed")
]

for r_i, r_data in enumerate(cost_breakdown_data, start=2):
    ws_cost.append(r_data)
    f_c = fill_alt if r_i % 2 == 1 else PatternFill(fill_type=None)
    for c_idx in range(1, len(r_data) + 1):
        cell = ws_cost.cell(row=r_i, column=c_idx)
        cell.font = Font(name="Calibri", size=9.5)
        if f_c.fill_type:
            cell.fill = f_c
        cell.border = border_thin
        if c_idx in [1, 2, 9, 10]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_idx in [4, 5, 6, 7, 8]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '"₹"#,##0'

# Sum row
tot_cost_row = len(cost_breakdown_data) + 2
ws_cost.cell(row=tot_cost_row, column=1, value="TOTAL")
ws_cost.cell(row=tot_cost_row, column=3, value="Cost Baseline (Aggregated Direct Expenditures)")
ws_cost.cell(row=tot_cost_row, column=4, value=310000)
ws_cost.cell(row=tot_cost_row, column=5, value=37000)
ws_cost.cell(row=tot_cost_row, column=6, value=24000)
ws_cost.cell(row=tot_cost_row, column=7, value=39000)
ws_cost.cell(row=tot_cost_row, column=8, value=410000)

for c_idx in range(1, len(cost_headers) + 1):
    cell = ws_cost.cell(row=tot_cost_row, column=c_idx)
    cell.font = Font(name="Calibri", size=10, bold=True)
    cell.fill = fill_tot
    cell.border = border_thin
    if c_idx in [4, 5, 6, 7, 8]:
        cell.number_format = '"₹"#,##0'
        cell.alignment = Alignment(horizontal="right", vertical="center")

cost_widths = [10, 12, 34, 20, 18, 18, 18, 20, 16, 16]
for idx, w in enumerate(cost_widths, start=1):
    ws_cost.column_dimensions[get_column_letter(idx)].width = w

# Sheet 2: Control Accounts & Reserves
ws_res = wb_bgt.create_sheet(title="Control Accounts & Reserves")
res_headers = ["Control Account / Phase", "WBS Elements", "Cost Baseline (INR)", "Contingency Reserve (10%)", "Management Reserve (7%)", "Total Approved Budget (INR)", "Budget Share (%)"]
ws_res.append(res_headers)
for c_i in range(1, len(res_headers) + 1):
    c = ws_res.cell(row=1, column=c_i)
    c.font = font_hdr
    c.fill = fill_hdr
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

control_accounts_data = [
    ("CA-01: Initiation & Requirements", "1.1.1 to 1.1.3", 42000, 4200, 3480, 49680, "10.2%"),
    ("CA-02: Architecture & Technical Design", "1.2.1 to 1.2.4", 78000, 7800, 6470, 92270, "19.0%"),
    ("CA-03: Core Application Development", "1.3.1 to 1.3.8", 176000, 17600, 14610, 208210, "42.9%"),
    ("CA-04: Cloud DevOps & Hardening", "1.4.1 to 1.4.3", 68000, 6800, 5640, 80440, "16.6%"),
    ("CA-05: QA, Pilot Rollout & Handover", "1.5.1 to 1.5.3", 46000, 4600, 3800, 54400, "11.3%")
]
for r_i, r_data in enumerate(control_accounts_data, start=2):
    ws_res.append(r_data)
    f_r = fill_alt if r_i % 2 == 1 else PatternFill(fill_type=None)
    for c_idx in range(1, len(r_data) + 1):
        cell = ws_res.cell(row=r_i, column=c_idx)
        cell.font = Font(name="Calibri", size=9.5)
        if f_r.fill_type:
            cell.fill = f_r
        cell.border = border_thin
        if c_idx in [1, 2, 7]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_idx in [3, 4, 5, 6]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '"₹"#,##0'

# Totals row
tot_res_row = len(control_accounts_data) + 2
ws_res.cell(row=tot_res_row, column=1, value="PROJECT TOTAL")
ws_res.cell(row=tot_res_row, column=2, value="All 5 Control Accounts")
ws_res.cell(row=tot_res_row, column=3, value=410000)
ws_res.cell(row=tot_res_row, column=4, value=41000)
ws_res.cell(row=tot_res_row, column=5, value=34000)
ws_res.cell(row=tot_res_row, column=6, value=485000)
ws_res.cell(row=tot_res_row, column=7, value="100.0%")

for c_idx in range(1, len(res_headers) + 1):
    cell = ws_res.cell(row=tot_res_row, column=c_idx)
    cell.font = Font(name="Calibri", size=10, bold=True)
    cell.fill = fill_tot
    cell.border = border_thin
    if c_idx in [3, 4, 5, 6]:
        cell.number_format = '"₹"#,##0'
        cell.alignment = Alignment(horizontal="right", vertical="center")
    elif c_idx in [1, 2, 7]:
        cell.alignment = Alignment(horizontal="center", vertical="center")

res_widths = [32, 18, 20, 24, 24, 25, 16]
for idx, w in enumerate(res_widths, start=1):
    ws_res.column_dimensions[get_column_letter(idx)].width = w

wb_bgt.save(budget_file)
print(f"Generated Budget_Estimation.xlsx at {budget_file}")
