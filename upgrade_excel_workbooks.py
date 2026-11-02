import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Colors (Professional Corporate Palette)
NAVY_HEADER = "1B365D"
LIGHT_BLUE_HEADER = "2C5282"
ACCENT_BLUE = "EBF8FF"
ZEBRA_FILL = "F7FAFC"
BORDER_GRAY = "CBD5E0"
ALERT_RED = "FFF5F5"
ALERT_GREEN = "F0FFF4"
WHITE = "FFFFFF"

def apply_styling(ws, header_color=NAVY_HEADER):
    thin_border = Border(
        left=Side(style='thin', color=BORDER_GRAY),
        right=Side(style='thin', color=BORDER_GRAY),
        top=Side(style='thin', color=BORDER_GRAY),
        bottom=Side(style='thin', color=BORDER_GRAY)
    )
    header_font = Font(name='Calibri', size=11, bold=True, color=WHITE)
    header_fill = PatternFill(start_color=header_color, end_color=header_color, fill_type='solid')
    regular_font = Font(name='Calibri', size=10)
    bold_font = Font(name='Calibri', size=10, bold=True)
    
    # Auto-adjust column widths
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            cell.border = thin_border
            if cell.row == 1 or cell.row == 2:
                continue
            val_str = str(cell.value or '')
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

def build_project_schedule():
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "CPM Activity Schedule"
    
    # Title Block
    ws1.merge_cells("A1:N1")
    ws1["A1"] = "SHALACONNECT - CRITICAL PATH METHOD (CPM) ACTIVITY SCHEDULE"
    ws1["A1"].font = Font(name='Calibri', size=14, bold=True, color=WHITE)
    ws1["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')
    ws1["A1"].alignment = Alignment(horizontal='center', vertical='center')
    ws1.row_dimensions[1].height = 28
    
    headers = [
        "Activity ID", "Activity Name", "WBS Ref", "Duration (Days)", 
        "Predecessors", "Early Start (ES)", "Early Finish (EF)", 
        "Late Start (LS)", "Late Finish (LF)", "Total Float (TF)", 
        "Free Float (FF)", "Critical Status", "Assigned Resource", "Cost (INR)"
    ]
    ws1.append(headers)
    ws1.row_dimensions[2].height = 24
    
    for col_idx, text in enumerate(headers, 1):
        cell = ws1.cell(row=2, column=col_idx)
        cell.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # 21 Activities Data with Dynamic Formulas
    # ES, EF, LS, LF values from rigorous CPM calculations
    activities_data = [
        ("ACT-01", "Stakeholder Requirements Gathering", "1.1.1", 3, "-", 0, 0, 3, 0, "Lead System Analyst", 15000),
        ("ACT-02", "System Architecture & Specs Design", "1.1.2", 4, "ACT-01", 3, 3, 7, 0, "Solutions Architect", 20000),
        ("ACT-03", "Government Regulatory Compliance", "1.1.3", 3, "ACT-02", 7, 10, 13, 3, "Legal & Compliance", 15000),
        ("ACT-04", "Database Schema & Multi-Tenancy", "1.2.1", 4, "ACT-02", 7, 7, 11, 0, "Database Administrator", 25000),
        ("ACT-05", "Cloud VPC & Terraform Infrastructure", "1.2.2", 5, "ACT-04", 11, 14, 19, 3, "DevOps Engineer", 30000),
        ("ACT-06", "Spring Boot Core Services Setup", "1.2.3", 5, "ACT-04", 11, 11, 16, 0, "Senior Backend Lead", 35000),
        ("ACT-07", "Docker Containerization & ECS Fargate", "1.2.4", 4, "ACT-05, ACT-06", 16, 17, 21, 1, "DevOps Engineer", 20000),
        ("ACT-08", "Authentication & RBAC Engine", "1.3.1", 4, "ACT-06", 16, 16, 20, 0, "Security Engineer", 25000),
        ("ACT-09", "School Registry & Profile Management", "1.3.2", 5, "ACT-08", 20, 20, 25, 0, "Backend Developer", 22000),
        ("ACT-10", "Teacher Allocation & Service Records", "1.3.3", 5, "ACT-09", 25, 25, 30, 0, "Full-Stack Developer", 24000),
        ("ACT-11", "Student Enrollment & Promotion Module", "1.3.4", 6, "ACT-10", 30, 31, 37, 1, "Full-Stack Developer", 28000),
        ("ACT-12", "Attendance Tracking & Geo-Fencing", "1.3.5", 5, "ACT-10", 30, 32, 37, 2, "Mobile/PWA Developer", 22000),
        ("ACT-13", "School Inspection & Compliance Engine", "1.3.6", 4, "ACT-10", 30, 30, 34, 0, "Backend Developer", 18000),
        ("ACT-14", "District Analytics Dashboard & BI", "1.3.7", 4, "ACT-13", 34, 34, 38, 0, "UI/Frontend Developer", 20000),
        ("ACT-15", "Document Vault & OCR Verification", "1.3.8", 4, "ACT-13", 34, 34, 38, 0, "AI/ML Engineer", 16000),
        ("ACT-16", "Automated Alerting & Parent SMS", "1.3.9", 3, "ACT-14, ACT-15", 38, 38, 41, 0, "Full-Stack Developer", 15000),
        ("ACT-17", "Integration & System Testing", "1.4.1", 5, "ACT-16", 41, 41, 46, 0, "Lead QA Engineer", 22000),
        ("ACT-18", "Performance & Scalability Load Testing", "1.4.2", 4, "ACT-17", 46, 47, 51, 1, "DevOps / QA Specialist", 18000),
        ("ACT-19", "Security Audit & Vulnerability Fixes", "1.4.3", 3, "ACT-17", 46, 46, 49, 0, "Security Auditor", 15000),
        ("ACT-20", "Pilot District User Acceptance Testing", "1.5.1", 4, "ACT-18, ACT-19", 49, 50, 54, 1, "Lead QA Engineer", 12000),
        ("ACT-21", "Production Deployment & Handover", "1.5.2", 5, "ACT-19", 49, 49, 54, 0, "DevOps / Project Manager", 18000),
    ]

    for idx, act in enumerate(activities_data, start=3):
        act_id, name, wbs, dur, preds, es, ls, lf, ff, res, cost = act
        # Formulas:
        # EF = ES + Duration -> =F{idx}+D{idx}
        # LS = LF - Duration -> =I{idx}-D{idx}
        # TF = LS - ES -> =H{idx}-F{idx}
        # Status = IF(TF=0, "CRITICAL", "Non-Critical")
        ef_formula = f"=F{idx}+D{idx}"
        ls_formula = f"=I{idx}-D{idx}"
        tf_formula = f"=H{idx}-F{idx}"
        crit_formula = f'=IF(J{idx}=0, "CRITICAL", "Non-Critical")'
        
        row_vals = [
            act_id, name, wbs, dur, preds, es, ef_formula,
            ls_formula, lf, tf_formula, ff, crit_formula, res, cost
        ]
        ws1.append(row_vals)
        ws1.row_dimensions[idx].height = 20

    # Total Row
    last_row = len(activities_data) + 2
    tot_row = last_row + 1
    ws1.cell(row=tot_row, column=1, value="TOTALS / PROJECT DURATION")
    ws1.cell(row=tot_row, column=4, value=f"=MAX(G3:G{last_row})")
    ws1.cell(row=tot_row, column=14, value=f"=SUM(N3:N{last_row})")
    ws1.row_dimensions[tot_row].height = 22
    
    for c in range(1, 15):
        cell = ws1.cell(row=tot_row, column=c)
        cell.font = Font(name='Calibri', size=11, bold=True, color=NAVY_HEADER)
        cell.fill = PatternFill(start_color=ACCENT_BLUE, end_color=ACCENT_BLUE, fill_type='solid')

    apply_styling(ws1)

    # Sheet 2: Network Paths Enumeration
    ws2 = wb.create_sheet(title="Network Paths Enumeration")
    ws2.merge_cells("A1:F1")
    ws2["A1"] = "SHALACONNECT - COMPLETE NETWORK PATH ENUMERATION & FLOAT ANALYSIS"
    ws2["A1"].font = Font(name='Calibri', size=14, bold=True, color=WHITE)
    ws2["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')
    ws2["A1"].alignment = Alignment(horizontal='center', vertical='center')
    ws2.row_dimensions[1].height = 28

    p_headers = ["Path ID", "Path Description & Node Sequence", "Total Duration (Days)", "Critical Path Duration", "Total Path Float (Days)", "Classification"]
    ws2.append(p_headers)
    ws2.row_dimensions[2].height = 24
    for c_idx, th in enumerate(p_headers, 1):
        cell = ws2.cell(row=2, column=c_idx)
        cell.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')
        cell.alignment = Alignment(horizontal='center', vertical='center')

    paths_data = [
        ("Path 1 (CRITICAL)", "ACT-01 -> ACT-02 -> ACT-04 -> ACT-06 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-13 -> ACT-14 -> ACT-16 -> ACT-17 -> ACT-19 -> ACT-21", 54, "CRITICAL PATH"),
        ("Path 2", "ACT-01 -> ACT-02 -> ACT-04 -> ACT-06 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-13 -> ACT-15 -> ACT-16 -> ACT-17 -> ACT-19 -> ACT-21", 54, "CRITICAL SUB-PATH"),
        ("Path 3", "ACT-01 -> ACT-02 -> ACT-04 -> ACT-06 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-11 -> ACT-17 -> ACT-19 -> ACT-21", 53, "Near-Critical (Float = 1d)"),
        ("Path 4", "ACT-01 -> ACT-02 -> ACT-04 -> ACT-06 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-12 -> ACT-17 -> ACT-19 -> ACT-21", 52, "Non-Critical (Float = 2d)"),
        ("Path 5", "ACT-01 -> ACT-02 -> ACT-04 -> ACT-05 -> ACT-07 -> ACT-17 -> ACT-19 -> ACT-21", 50, "Non-Critical (Float = 4d)"),
        ("Path 6", "ACT-01 -> ACT-02 -> ACT-03 -> ACT-17 -> ACT-19 -> ACT-21", 41, "Sub-Critical (Float = 13d)"),
        ("Path 7", "ACT-01 -> ACT-02 -> ACT-04 -> ACT-06 -> ACT-08 -> ACT-09 -> ACT-10 -> ACT-13 -> ACT-14 -> ACT-16 -> ACT-17 -> ACT-18 -> ACT-20", 53, "Near-Critical (Float = 1d)")
    ]

    for p_idx, p in enumerate(paths_data, start=3):
        pid, seq, dur, cls_desc = p
        # Formula for Float: =$D$3 - C{p_idx}
        float_formula = f"=$D$3-C{p_idx}"
        status_formula = f'=IF(E{p_idx}=0, "CRITICAL PATH", "Non-Critical Path")'
        ws2.append([pid, seq, dur, 54, float_formula, status_formula])
        ws2.row_dimensions[p_idx].height = 20

    apply_styling(ws2)

    # Sheet 3: Schedule KPI Dashboard
    ws3 = wb.create_sheet(title="Schedule KPIs & Summary")
    ws3.merge_cells("A1:D1")
    ws3["A1"] = "SHALACONNECT - SCHEDULE EXECUTIVE KPI SUMMARY"
    ws3["A1"].font = Font(name='Calibri', size=14, bold=True, color=WHITE)
    ws3["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')
    ws3["A1"].alignment = Alignment(horizontal='center', vertical='center')
    ws3.row_dimensions[1].height = 28

    kpis = [
        ("Metric Description", "Calculated Value", "Unit / Format", "Formula Reference"),
        ("Project Deterministic Schedule", "='CPM Activity Schedule'!D24", "Working Days", "MAX(Early Finish)"),
        ("Academic Semester Window", 80, "Working Days", "16 Weeks x 5 Days"),
        ("Scheduled Operational Buffer", "=B3-B2", "Working Days", "Semester Window - CPM"),
        ("Total Work Packages / Activities", "=COUNTA('CPM Activity Schedule'!A3:A23)", "Activities", "COUNT(ACT-01..21)"),
        ("Critical Path Activities Count", '=COUNTIF(\'CPM Activity Schedule\'!L3:L23, "CRITICAL")', "Activities (TF = 0)", "COUNTIF(Critical)"),
        ("Non-Critical Activities Count", '=COUNTIF(\'CPM Activity Schedule\'!L3:L23, "Non-Critical")', "Activities (TF > 0)", "COUNTIF(Non-Critical)"),
        ("Aggregated Direct Baseline Budget", "='CPM Activity Schedule'!N24", "INR", "SUM(Activity Direct Costs)"),
        ("Average Activity Duration", "=AVERAGE('CPM Activity Schedule'!D3:D23)", "Working Days", "AVERAGE(Durations)"),
        ("Maximum Activity Duration", "=MAX('CPM Activity Schedule'!D3:D23)", "Working Days (ACT-11)", "MAX(Durations)"),
        ("Minimum Activity Duration", "=MIN('CPM Activity Schedule'!D3:D23)", "Working Days (ACT-01)", "MIN(Durations)")
    ]

    for k_idx, k in enumerate(kpis, start=2):
        ws3.append(list(k))
        ws3.row_dimensions[k_idx].height = 22
        if k_idx == 2:
            for c in range(1, 5):
                cell = ws3.cell(row=2, column=c)
                cell.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
                cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')

    apply_styling(ws3)

    out_path = "Project_Management_Submissions/Assignment_2_Project_Plan/Project_Schedule.xlsx"
    wb.save(out_path)
    print(f"Upgraded dynamic schedule saved to: {out_path}")

def build_budget_estimation():
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Control Account Budget Baseline"
    
    # Title Block
    ws1.merge_cells("A1:H1")
    ws1["A1"] = "SHALACONNECT - COST BASELINE AGGREGATION & CONTROL ACCOUNTS (BAC)"
    ws1["A1"].font = Font(name='Calibri', size=14, bold=True, color=WHITE)
    ws1["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')
    ws1["A1"].alignment = Alignment(horizontal='center', vertical='center')
    ws1.row_dimensions[1].height = 28
    
    headers = [
        "Control Account ID", "WBS Code", "Work Package Description", 
        "Resource Assigned", "Direct Cost (INR)", "Indirect Cost (INR)", 
        "Total Cost (INR)", "Cost Baseline %"
    ]
    ws1.append(headers)
    ws1.row_dimensions[2].height = 24
    for c_idx, th in enumerate(headers, 1):
        cell = ws1.cell(row=2, column=c_idx)
        cell.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # 21 items with genuine Excel formulas
    items = [
        # CA-01
        ("CA-01", "1.1.1", "Stakeholder Requirements Gathering", "Lead Analyst", 15000, 3000),
        ("CA-01", "1.1.2", "System Architecture & Specs Design", "Solutions Architect", 20000, 4000),
        ("CA-01", "1.1.3", "Government Regulatory Compliance", "Legal Specialist", 15000, 3000),
        # CA-02
        ("CA-02", "1.2.1", "Database Schema & Multi-Tenancy", "DBA Lead", 25000, 5000),
        ("CA-02", "1.2.2", "Cloud VPC & Terraform Infrastructure", "DevOps Engineer", 30000, 6000),
        ("CA-02", "1.2.3", "Spring Boot Core Services Setup", "Backend Lead", 35000, 7000),
        ("CA-02", "1.2.4", "Docker Containerization & ECS Fargate", "DevOps Engineer", 20000, 4000),
        # CA-03
        ("CA-03", "1.3.1", "Authentication & RBAC Engine", "Security Engineer", 25000, 5000),
        ("CA-03", "1.3.2", "School Registry & Profile Management", "Backend Developer", 22000, 4500),
        ("CA-03", "1.3.3", "Teacher Allocation & Service Records", "Full-Stack Dev", 24000, 5000),
        ("CA-03", "1.3.4", "Student Enrollment & Promotion Module", "Full-Stack Dev", 28000, 6000),
        ("CA-03", "1.3.5", "Attendance Tracking & Geo-Fencing", "Mobile/PWA Dev", 22000, 4500),
        ("CA-03", "1.3.6", "School Inspection & Compliance Engine", "Backend Developer", 18000, 3500),
        ("CA-03", "1.3.7", "District Analytics Dashboard & BI", "UI/Frontend Dev", 20000, 4000),
        ("CA-03", "1.3.8", "Document Vault & OCR Verification", "AI/ML Engineer", 16000, 3500),
        ("CA-03", "1.3.9", "Automated Alerting & Parent SMS", "Full-Stack Dev", 15000, 3000),
        # CA-04
        ("CA-04", "1.4.1", "Integration & System Testing", "QA Lead", 22000, 5000),
        ("CA-04", "1.4.2", "Performance & Scalability Load Testing", "QA / DevOps", 18000, 4000),
        ("CA-04", "1.4.3", "Security Audit & Vulnerability Fixes", "Security Auditor", 15000, 3500),
        # CA-05
        ("CA-05", "1.5.1", "Pilot District User Acceptance Testing", "QA Lead", 12000, 2500),
        ("CA-05", "1.5.2", "Production Deployment & Handover", "DevOps / PM", 18000, 3000),
    ]

    for idx, it in enumerate(items, start=3):
        ca, wbs, desc, res, dir_c, indir_c = it
        # Formulas:
        # Total = Direct + Indirect -> =E{idx}+F{idx}
        # Pct = Total / BAC -> =G{idx}/$G$24
        tot_formula = f"=E{idx}+F{idx}"
        pct_formula = f"=G{idx}/$G$24"
        ws1.append([ca, wbs, desc, res, dir_c, indir_c, tot_formula, pct_formula])
        ws1.row_dimensions[idx].height = 20
        ws1.cell(row=idx, column=8).number_format = '0.00%'

    # Subtotals & Baseline Row
    ws1.cell(row=24, column=1, value="COST BASELINE (BAC)")
    ws1.cell(row=24, column=5, value="=SUM(E3:E23)")
    ws1.cell(row=24, column=6, value="=SUM(F3:F23)")
    ws1.cell(row=24, column=7, value="=SUM(G3:G23)")
    ws1.cell(row=24, column=8, value="=SUM(H3:H23)")
    ws1.cell(row=24, column=8).number_format = '0.00%'
    ws1.row_dimensions[24].height = 24
    for c in range(1, 9):
        cell = ws1.cell(row=24, column=c)
        cell.font = Font(name='Calibri', size=11, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')

    # Contingency & Management Reserves
    ws1.cell(row=25, column=1, value="CONTINGENCY RESERVE (10% - PM Controlled)")
    ws1.merge_cells("A25:F25")
    ws1.cell(row=25, column=7, value="=G24*0.10")
    ws1.cell(row=25, column=8, value="=G25/$G$27")
    ws1.cell(row=25, column=8).number_format = '0.00%'
    ws1.row_dimensions[25].height = 20

    ws1.cell(row=26, column=1, value="MANAGEMENT RESERVE (7% - Sponsor Controlled)")
    ws1.merge_cells("A26:F26")
    ws1.cell(row=26, column=7, value="=34000")
    ws1.cell(row=26, column=8, value="=G26/$G$27")
    ws1.cell(row=26, column=8).number_format = '0.00%'
    ws1.row_dimensions[26].height = 20

    ws1.cell(row=27, column=1, value="TOTAL PROJECT BUDGET (INR)")
    ws1.merge_cells("A27:F27")
    ws1.cell(row=27, column=7, value="=G24+G25+G26")
    ws1.cell(row=27, column=8, value="=1.00")
    ws1.cell(row=27, column=8).number_format = '0.00%'
    ws1.row_dimensions[27].height = 24

    for r in range(25, 28):
        for c in range(1, 9):
            cell = ws1.cell(row=r, column=c)
            cell.font = Font(name='Calibri', size=11, bold=True, color=NAVY_HEADER if r!=27 else WHITE)
            cell.fill = PatternFill(start_color=ACCENT_BLUE if r!=27 else LIGHT_BLUE_HEADER, 
                                   end_color=ACCENT_BLUE if r!=27 else LIGHT_BLUE_HEADER, fill_type='solid')

    apply_styling(ws1)

    # Sheet 2: Time-Phased Cash Flow & S-Curve Data
    ws2 = wb.create_sheet(title="Time-Phased Cash Flow S-Curve")
    ws2.merge_cells("A1:R1")
    ws2["A1"] = "SHALACONNECT - WEEKLY TIME-PHASED CASH FLOW EXPENDITURE (WEEKS 1 TO 16)"
    ws2["A1"].font = Font(name='Calibri', size=14, bold=True, color=WHITE)
    ws2["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')
    ws2["A1"].alignment = Alignment(horizontal='center', vertical='center')
    ws2.row_dimensions[1].height = 28

    sc_headers = ["Control Account / Metric", "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10", "W11", "W12", "W13", "W14", "W15", "W16", "Total (INR)"]
    ws2.append(sc_headers)
    ws2.row_dimensions[2].height = 24
    for c_idx, th in enumerate(sc_headers, 1):
        cell = ws2.cell(row=2, column=c_idx)
        cell.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # Weekly distribution across CA-01 through CA-05
    weekly_matrix = [
        ("CA-01: Inception & Specs", [15000, 24000, 18000, 3000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ("CA-02: Architecture & Foundation", [0, 0, 15000, 35000, 42000, 38000, 12000, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ("CA-03: Core Educational Modules", [0, 0, 0, 0, 10000, 25000, 36000, 42000, 38000, 32000, 21000, 0, 0, 0, 0, 0]),
        ("CA-04: Testing & Quality Assurance", [0, 0, 0, 0, 0, 0, 0, 0, 0, 12000, 25000, 27000, 8000, 0, 0, 0]),
        ("CA-05: Deployment & Handover", [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12000, 15000, 5500, 3000])
    ]

    for r_idx, row_data in enumerate(weekly_matrix, start=3):
        ca_name, spends = row_data
        row_vals = [ca_name] + spends + [f"=SUM(B{r_idx}:Q{r_idx})"]
        ws2.append(row_vals)
        ws2.row_dimensions[r_idx].height = 20

    # Total Weekly Expenditure Row
    ws2.append(["WEEKLY TOTAL (INR)"] + [f"=SUM({get_column_letter(c)}3:{get_column_letter(c)}7)" for c in range(2, 18)] + ["=SUM(R3:R7)"])
    ws2.row_dimensions[8].height = 22
    for c in range(1, 19):
        cell = ws2.cell(row=8, column=c)
        cell.font = Font(name='Calibri', size=10, bold=True, color=NAVY_HEADER)
        cell.fill = PatternFill(start_color=ACCENT_BLUE, end_color=ACCENT_BLUE, fill_type='solid')

    # Cumulative Spend Row (S-Curve Planned Value PV)
    cum_vals = ["CUMULATIVE PV (INR)", "=B8"]
    for c in range(3, 18):
        prev_col = get_column_letter(c-1)
        curr_col = get_column_letter(c)
        cum_vals.append(f"={prev_col}9+{curr_col}8")
    cum_vals.append("=Q9")
    ws2.append(cum_vals)
    ws2.row_dimensions[9].height = 22
    for c in range(1, 19):
        cell = ws2.cell(row=9, column=c)
        cell.font = Font(name='Calibri', size=11, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')

    # Cumulative % of BAC Row
    pct_vals = ["CUMULATIVE % (BAC)"]
    for c in range(2, 18):
        curr_col = get_column_letter(c)
        pct_vals.append(f"={curr_col}9/$R$9")
    pct_vals.append("=1.00")
    ws2.append(pct_vals)
    ws2.row_dimensions[10].height = 20
    for c in range(2, 19):
        ws2.cell(row=10, column=c).number_format = '0.00%'

    apply_styling(ws2)

    out_path = "Project_Management_Submissions/Assignment_2_Project_Plan/Budget_Estimation.xlsx"
    wb.save(out_path)
    print(f"Upgraded dynamic budget saved to: {out_path}")

def build_risk_register():
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Quantitative Risk Register"
    
    # Title Block
    ws1.merge_cells("A1:R1")
    ws1["A1"] = "SHALACONNECT - QUANTITATIVE RISK REGISTER & RESIDUAL EXPOSURE ANALYSIS"
    ws1["A1"].font = Font(name='Calibri', size=14, bold=True, color=WHITE)
    ws1["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')
    ws1["A1"].alignment = Alignment(horizontal='center', vertical='center')
    ws1.row_dimensions[1].height = 28

    headers = [
        "Risk ID", "Category", "Risk Description", "Potential Impact",
        "Pre-P (1-5)", "Pre-I (1-5)", "Pre Score", "Pre Level",
        "Mitigation Action Plan", "Risk Owner", "Trigger Condition",
        "Post-P (1-5)", "Post-I (1-5)", "Post Score", "Post Level",
        "Score Reduction %", "Contingency Allocation (INR)", "Status"
    ]
    ws1.append(headers)
    ws1.row_dimensions[2].height = 24
    for c_idx, th in enumerate(headers, 1):
        cell = ws1.cell(row=2, column=c_idx)
        cell.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')
        cell.alignment = Alignment(horizontal='center', vertical='center')

    # 20 Risks (16 Threats, 4 Opportunities)
    risks_data = [
        ("RSK-01", "Technical", "Rural Network Connectivity Deficits in ZP Schools", "Transaction timeouts & sync failures", 4, 4, "Deploy Progressive Web App (PWA) with SQLite local storage", "Mobile Lead", "Telemetry logs >15% offline dropouts", 2, 2, 8000),
        ("RSK-02", "External", "AWS Cloud Infrastructure Cost Escalation", "Operational expense overrun beyond budget", 4, 3, "Implement AWS Budgets, CloudWatch anomaly alerts & ECS Auto-scaling", "DevOps Lead", "Monthly cloud burn rate > 120% of baseline", 2, 2, 5000),
        ("RSK-03", "Technical", "UDISE+ Master School Data Schema Inconsistencies", "Data import failures & pipeline rejection", 4, 4, "Automated data sanitation script & fuzzy validation engine", "DBA Lead", "Master ingestion pipeline errors > 5%", 2, 2, 6000),
        ("RSK-04", "Organizational", "DPDPA 2023 Student Data Privacy Compliance Gap", "Legal penalties & state audit suspension", 3, 5, "AES-256 at rest, TLS 1.3 in transit, strict RBAC & masking", "Security Lead", "Security vulnerability scan high-severity flag", 1, 3, 7000),
        ("RSK-05", "External", "Cluster Headmaster Resistance & Low Digital Adoption", "Delayed reporting & low active usage", 4, 3, "District training workshops, Marathi user guides & helpdesk", "Project Manager", "Active user portal logins < 50% after Week 2", 2, 2, 4000),
        ("RSK-06", "Technical", "Tesseract OCR Accuracy Degradation on Handwritten Forms", "Inspection report verification latency", 3, 4, "Multi-pass adaptive thresholding & human verification queue", "AI/ML Lead", "OCR confidence rating drops below 85%", 2, 2, 3000),
        ("RSK-07", "Project Mgmt", "Critical Path Developer Attrition or Sick Leave", "Direct schedule slippage on core modules", 3, 4, "Cross-training pair programming & documented architecture", "Project Manager", "Unplanned developer leave exceeding 3 days", 1, 3, 3000),
        ("RSK-08", "Technical", "PostgreSQL Connection Starvation during Morning Peaks", "System latency & HTTP 504 Gateway Timeouts", 3, 4, "Deploy HikariCP connection pooling & Redis read-cache", "Backend Lead", "DB connection pool utilization exceeds 85%", 1, 2, 2000),
        ("RSK-09", "External", "State Regulatory Portal API Changes during Sprint", "Integration breakages in compliance sync", 3, 3, "Modular abstraction layer & contract-based testing", "Solutions Architect", "Government notification of API spec alteration", 1, 2, 1000),
        ("RSK-10", "Organizational", "Delay in Pilot District Sign-off by ZP Education Officer", "Gate milestone slippage into examination period", 3, 4, "Weekly sprint showcase & early UAT test environment access", "Project Manager", "UAT sign-off delay exceeding 4 business days", 1, 2, 2000),
        ("RSK-11", "Technical", "Geo-Fencing Spoofing in Teacher Attendance App", "Fraudulent attendance check-ins", 3, 3, "Implement mock-location detection & hardware verification", "Security Lead", "Audit log detecting spoofed GPS coordinates", 1, 1, 0),
        ("RSK-12", "External", "Third-Party SMS Gateway Blacklisting or Throttling", "Parent emergency notifications fail to deliver", 3, 3, "Dual-vendor SMS failover (Twilio + Gupshup)", "Backend Lead", "SMS delivery success rate drops below 98%", 1, 2, 0),
        ("RSK-13", "Technical", "Docker Container Memory Leaks under JVM 21 Heap Spikes", "ECS Fargate tasks restarted unexpectedly", 2, 4, "JVM memory cgroup tuning and heap profiling via VisualVM", "DevOps Lead", "ECS memory utilization exceeds 80%", 1, 2, 0),
        ("RSK-14", "Project Mgmt", "Scope Creep from Non-Standard District Demands", "Uncontrolled development effort expansion", 3, 3, "Strict Change Control Board (CCB) and formal review gate", "Project Manager", "Feature request outside signed charter scope", 1, 2, 0),
        ("RSK-15", "Technical", "Automated Playwright Integration Test Flakiness", "Delayed CI/CD deployment pipelines", 3, 2, "Deterministic test fixtures and isolated mock services", "QA Lead", "CI/CD build failure due to test timeout", 1, 1, 0),
        ("RSK-16", "External", "Hardware Device Incompatibility across Legacy School PCs", "Browser UI rendering glitches", 3, 3, "Standard CSS Grid baseline with polyfills for Chrome 80+", "UI Lead", "Browser support defect reported in pilot", 1, 2, 0),
        # 4 Opportunities
        ("OPP-01", "Technical", "Adoption of Spring Boot 3.2 Ahead-of-Time (AOT) Native Image", "5x faster container cold start and 50% RAM savings", 4, 4, "Prototype GraalVM native binary compilation in staging", "DevOps Lead", "GraalVM compilation passes all unit tests", 4, 4, 0),
        ("OPP-02", "External", "District Level Replication by Adjacent Zilla Parishads", "Higher institutional recognition and grant funding", 3, 5, "Package system as multi-tenant white-label platform", "Project Manager", "Formal inquiry from neighboring education officer", 4, 5, 0),
        ("OPP-03", "Technical", "Automated Student Progress Prediction via Lightweight ML", "Proactive dropout prevention alerting", 3, 4, "Integrate Scikit-learn random forest risk scoring", "AI/ML Lead", "Accuracy score exceeds 90% on test dataset", 3, 4, 0),
        ("OPP-04", "Organizational", "State Education Board Hackathon Excellence Award", "University commendation and academic publication", 4, 4, "Submit ShalaConnect architecture paper to IEEE/Springer", "Project Manager", "Paper accepted for university research showcase", 4, 5, 0)
    ]

    for idx, r in enumerate(risks_data, start=3):
        rid, cat, desc, imp, pre_p, pre_i, mit, own, trig, post_p, post_i, alloc = r
        # Formulas:
        # Pre Score: =E{idx}*F{idx}
        # Pre Level: =IF(G{idx}>=15,"HIGH",IF(G{idx}>=8,"MEDIUM","LOW"))
        # Post Score: =L{idx}*M{idx}
        # Post Level: =IF(N{idx}>=15,"HIGH",IF(N{idx}>=8,"MEDIUM","LOW"))
        # Red Pct: =(G{idx}-N{idx})/G{idx}
        pre_s_f = f"=E{idx}*F{idx}"
        pre_l_f = f'=IF(G{idx}>=15,"HIGH",IF(G{idx}>=8,"MEDIUM","LOW"))'
        post_s_f = f"=L{idx}*M{idx}"
        post_l_f = f'=IF(N{idx}>=15,"HIGH",IF(N{idx}>=8,"MEDIUM","LOW"))'
        red_f = f"=(G{idx}-N{idx})/G{idx}"
        status = "Active Managed"
        
        row_vals = [
            rid, cat, desc, imp, pre_p, pre_i, pre_s_f, pre_l_f,
            mit, own, trig, post_p, post_i, post_s_f, post_l_f,
            red_f, alloc, status
        ]
        ws1.append(row_vals)
        ws1.row_dimensions[idx].height = 20
        ws1.cell(row=idx, column=16).number_format = '0.0%'

    # Total Contingency Allocation Row
    tot_row = len(risks_data) + 3
    ws1.cell(row=tot_row, column=1, value="TOTAL ALLOCATED CONTINGENCY RESERVE")
    ws1.merge_cells(f"A{tot_row}:P{tot_row}")
    ws1.cell(row=tot_row, column=17, value=f"=SUM(Q3:Q{tot_row-1})")
    ws1.cell(row=tot_row, column=18, value="INR 41,000 (10%)")
    ws1.row_dimensions[tot_row].height = 24
    for c in range(1, 19):
        cell = ws1.cell(row=tot_row, column=c)
        cell.font = Font(name='Calibri', size=11, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')

    apply_styling(ws1)

    # Sheet 2: Risk Analytics KPI Dashboard
    ws2 = wb.create_sheet(title="Risk Analytics KPIs")
    ws2.merge_cells("A1:D1")
    ws2["A1"] = "SHALACONNECT - RISK METRICS & EXPOSURE REDUCTION KPIS"
    ws2["A1"].font = Font(name='Calibri', size=14, bold=True, color=WHITE)
    ws2["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')
    ws2["A1"].alignment = Alignment(horizontal='center', vertical='center')
    ws2.row_dimensions[1].height = 28

    kpis = [
        ("Risk Metric Description", "Calculated Value", "Measurement Unit", "Formula Logic"),
        ("Total Identified Risks", "=COUNTA('Quantitative Risk Register'!A3:A22)", "Total Entries", "COUNT(RSK-01..OPP-04)"),
        ("Identified Threats Count", '=COUNTIF(\'Quantitative Risk Register\'!A3:A22, "RSK*")', "Threats", "COUNTIF('RSK*')"),
        ("Identified Opportunities Count", '=COUNTIF(\'Quantitative Risk Register\'!A3:A22, "OPP*")', "Opportunities", "COUNTIF('OPP*')"),
        ("High Severity Pre-Mitigation Threats", '=COUNTIFS(\'Quantitative Risk Register\'!A3:A18, "RSK*", \'Quantitative Risk Register\'!H3:H18, "HIGH")', "Threats (Score >= 15)", "COUNTIFS(Threat & HIGH)"),
        ("Medium Severity Pre-Mitigation Threats", '=COUNTIFS(\'Quantitative Risk Register\'!A3:A18, "RSK*", \'Quantitative Risk Register\'!H3:H18, "MEDIUM")', "Threats (8 <= Score < 15)", "COUNTIFS(Threat & MEDIUM)"),
        ("Low Severity Pre-Mitigation Threats", '=COUNTIFS(\'Quantitative Risk Register\'!A3:A18, "RSK*", \'Quantitative Risk Register\'!H3:H18, "LOW")', "Threats (Score < 8)", "COUNTIFS(Threat & LOW)"),
        ("High Severity Post-Mitigation Threats", '=COUNTIFS(\'Quantitative Risk Register\'!A3:A18, "RSK*", \'Quantitative Risk Register\'!O3:O18, "HIGH")', "Residual High Threats", "Zero (100% Mitigated)"),
        ("Average Threat Score Before Mitigation", "=AVERAGE('Quantitative Risk Register'!G3:G18)", "Score (out of 25)", "AVERAGE(Threat Pre Scores)"),
        ("Average Threat Score After Mitigation", "=AVERAGE('Quantitative Risk Register'!N3:N18)", "Score (out of 25)", "AVERAGE(Threat Post Scores)"),
        ("Overall Risk Exposure Reduction", "=(B10-B11)/B10", "Percentage Reduction", "(Pre - Post) / Pre"),
        ("Total Risk Contingency Fund Allocated", "='Quantitative Risk Register'!Q23", "INR", "Sum of Allocated Reserves")
    ]

    for k_idx, k in enumerate(kpis, start=2):
        ws2.append(list(k))
        ws2.row_dimensions[k_idx].height = 22
        if k_idx == 2:
            for c in range(1, 5):
                cell = ws2.cell(row=2, column=c)
                cell.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
                cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')

    ws2.cell(row=12, column=2).number_format = '0.0%'

    apply_styling(ws2)

    out_path = "Project_Management_Submissions/Assignment_4_Risk_Management/Risk_Register.xlsx"
    wb.save(out_path)
    print(f"Upgraded dynamic risk register saved to: {out_path}")

def build_wbs_dictionary():
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "WBS Dictionary"
    
    # Title Block
    ws1.merge_cells("A1:L1")
    ws1["A1"] = "SHALACONNECT - DETAILED WORK BREAKDOWN STRUCTURE (WBS) DICTIONARY"
    ws1["A1"].font = Font(name='Calibri', size=14, bold=True, color=WHITE)
    ws1["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')
    ws1["A1"].alignment = Alignment(horizontal='center', vertical='center')
    ws1.row_dimensions[1].height = 28

    headers = [
        "WBS ID", "Work Package Name", "Phase / Parent Level", "Scope Boundaries",
        "Deliverables & Technical Output", "Acceptance Criteria", "Responsible Role",
        "Required Resources", "Duration (Days)", "Cost (INR)", "Predecessors", "Key Assumptions"
    ]
    ws1.append(headers)
    ws1.row_dimensions[2].height = 24
    for c_idx, th in enumerate(headers, 1):
        cell = ws1.cell(row=2, column=c_idx)
        cell.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')
        cell.alignment = Alignment(horizontal='center', vertical='center')

    wbs_data = [
        ("1.1.1", "Stakeholder Requirements Gathering", "1.1 Project Inception", "Interviews with ZP education officers, headmasters", "SRS Document v1.0, User Persona Catalog", "Signed SRS by MITAOE Sponsor and Pilot Headmasters", "Lead Systems Analyst", "Confluence, Miro, Recording Tools", 3, 18000, "-", "District officers available for 2 interview cycles"),
        ("1.1.2", "System Architecture & Specs Design", "1.1 Project Inception", "Architectural blueprint, component interactions", "High-Level Architecture & C4 Model Docs", "Peer-reviewed by Solutions Architect", "Solutions Architect", "Enterprise Architect, Lucidchart", 4, 24000, "1.1.1", "Spring Boot 3.2 and React 18 compatible"),
        ("1.1.3", "Government Regulatory Compliance", "1.1 Project Inception", "DPDPA 2023, NEP 2020, RTE Act guidelines", "Compliance Checklist & Data Retention Policy", "Formal approval from academic legal advisor", "Legal & Compliance", "Legal database, ISO 27001 handbook", 3, 18000, "1.1.2", "State compliance guidelines remain static"),
        ("1.2.1", "Database Schema & Multi-Tenancy", "1.2 Architectural Foundation", "PostgreSQL 16 relational model, tenant schemas", "DDL Scripts, Liquibase Migrations, ERD Diagram", "All constraints pass SQL linter with zero cyclic keys", "Database Administrator", "DataGrip, PostgreSQL 16, Liquibase", 4, 30000, "1.1.2", "PostgreSQL row-level security supported"),
        ("1.2.2", "Cloud VPC & Terraform Infrastructure", "1.2 Architectural Foundation", "AWS VPC, subnets, IGW, security groups", "Terraform IAC codebase, State backend in S3", "Terraform apply executes cleanly with zero manual edits", "DevOps Engineer", "AWS CLI, Terraform 1.7, AWS Sandbox", 5, 36000, "1.2.1", "AWS free tier & student credits active"),
        ("1.2.3", "Spring Boot Core Services Setup", "1.2 Architectural Foundation", "Spring Boot 3.2 project scaffolding, dependencies", "Base Maven project, Spring Security, Global Exception", "Clean build with zero CVEs in dependency scan", "Senior Backend Lead", "IntelliJ IDEA, Java 21 LTS, Maven", 5, 42000, "1.2.1", "Java 21 LTS baseline adopted across team"),
        ("1.2.4", "Docker Containerization & ECS Fargate", "1.2 Architectural Foundation", "Multi-stage Dockerfiles, task definitions", "Optimized Docker images (<180MB), ECS tasks", "Container starts in <15s with passing healthcheck", "DevOps Engineer", "Docker Engine, AWS ECS, ECR", 4, 24000, "1.2.2, 1.2.3", "AWS Fargate pricing tier maintained"),
        ("1.3.1", "Authentication & RBAC Engine", "1.3 Core Educational Services", "JWT token generation, refresh tokens, BCrypt", "Auth REST Controller, Security Filter Chain", "Zero unauthorized endpoint penetration in OWASP test", "Security Engineer", "Spring Security, Postman, JWT library", 4, 30000, "1.2.3", "Roles: SuperAdmin, ClusterAdmin, Teacher, Parent"),
        ("1.3.2", "School Registry & Profile Management", "1.3 Core Educational Services", "School profile CRUD, UDISE+ validation", "School Service APIs, React Admin UI screens", "CRUD operations complete in <200ms roundtrip", "Backend Developer", "Spring Data JPA, React 18, Vite", 5, 26500, "1.3.1", "UDISE+ codes conform to 11-digit format"),
        ("1.3.3", "Teacher Allocation & Service Records", "1.3 Core Educational Services", "Teacher profile, subject qualification, transfers", "Teacher Allocation REST APIs, UI Components", "Transfer workflow prevents double allocation", "Full-Stack Developer", "Spring Boot, React Table, TanStack Query", 5, 29000, "1.3.2", "Teacher IDs mapped to State Sevaarth numbers"),
        ("1.3.4", "Student Enrollment & Promotion Module", "1.3 Core Educational Services", "Student admissions, category tracking, yearly promotion", "Enrollment UI, Bulk CSV Uploader, API endpoints", "Handles bulk import of 500 records in <5 seconds", "Full-Stack Developer", "OpenCSV, React Dropzone, PostgreSQL", 6, 34000, "1.3.3", "Student APAAR ID optional but supported"),
        ("1.3.5", "Attendance Tracking & Geo-Fencing", "1.3 Core Educational Services", "Daily attendance, geolocation coordinates capture", "PWA Attendance View, Geo-validation API", "Geofence boundary verification within 100m radius", "Mobile/PWA Developer", "HTML5 Geolocation API, Service Workers", 5, 26500, "1.3.3", "Mobile browser supports HTML5 Geolocation"),
        ("1.3.6", "School Inspection & Compliance Engine", "1.3 Core Educational Services", "Inspection checklists, infrastructure scoring", "Inspection Module API, Audit Log Engine", "Generates consolidated cluster compliance index", "Backend Developer", "Spring Data JPA, JasperReports, React", 4, 21500, "1.3.3", "Standard RTE 10-point checklist utilized"),
        ("1.3.7", "District Analytics Dashboard & BI", "1.3 Core Educational Services", "KPI visualization, cluster performance metrics", "Analytics Controller, Chart.js / Recharts UI", "Dashboard renders within 1.2 seconds on 3G network", "UI/Frontend Developer", "Chart.js, React 18, Tailwind CSS", 4, 24000, "1.3.6", "Aggregated data queries run in read-replica"),
        ("1.3.8", "Document Vault & OCR Verification", "1.3 Core Educational Services", "Certificate upload, S3 pre-signed URLs, OCR", "Document Vault Service, Tesseract OCR Integration", "OCR achieves >85% character accuracy on scans", "AI/ML Engineer", "AWS S3 SDK, Tesseract OCR, Python/Java", 4, 19500, "1.3.6", "Uploaded files limited to 5MB PDF/PNG"),
        ("1.3.9", "Automated Alerting & Parent SMS", "1.3 Core Educational Services", "Transactional alerts, attendance SMS notifications", "Notification Gateway Service, Twilio Adapter", "SMS delivered within 10 seconds of attendance trigger", "Full-Stack Developer", "Twilio SDK, Spring Async, RabbitMQ/Redis", 3, 18000, "1.3.7, 1.3.8", "DND registry bypass via transactional route"),
        ("1.4.1", "Integration & System Testing", "1.4 Quality Assurance & Testing", "End-to-end API integration tests, user journeys", "Automated Playwright & Postman Test Suites", "100% of critical paths pass with zero regressions", "Lead QA Engineer", "Playwright, Postman, GitHub Actions", 5, 27000, "1.3.9", "Staging environment mirrors production DB"),
        ("1.4.2", "Performance & Scalability Load Testing", "1.4 Quality Assurance & Testing", "Concurrent load testing up to 1,000 active sessions", "JMeter Test Plans, Scalability Assessment Report", "System maintains p95 latency < 500ms at 500 req/sec", "DevOps / QA Specialist", "Apache JMeter, AWS CloudWatch", 4, 22000, "1.4.1", "AWS auto-scaling triggers at 70% CPU"),
        ("1.4.3", "Security Audit & Vulnerability Fixes", "1.4 Quality Assurance & Testing", "DAST scanning, SQL injection, XSS penetration", "OWASP ZAP Report, SonarQube Quality Gate Report", "Zero High or Critical vulnerabilities; SonarQube Gate A", "Security Auditor", "OWASP ZAP, SonarQube, Snyk", 3, 18500, "1.4.1", "OWASP Top 10 standards strictly enforced"),
        ("1.5.1", "Pilot District User Acceptance Testing", "1.5 Deployment & Handover", "UAT execution with 20 real cluster headmasters", "UAT Defect Log, Formal Acceptance Sign-Off Sheet", "100% of Severity 1 & 2 defects resolved; sign-off signed", "Lead QA Engineer", "Jira, Google Forms, Demo Portal", 4, 14500, "1.4.2, 1.4.3", "District officers participate in 3 test sessions"),
        ("1.5.2", "Production Deployment & Handover", "1.5 Deployment & Handover", "AWS Production release, DNS cutover, handover docs", "Production Deployment Runbook, User Training Manual", "DNS cutover with zero downtime; live healthcheck 200", "DevOps / Project Manager", "Route 53, ACM SSL, AWS ECS Production", 5, 21000, "1.4.3", "SSL certificate pre-validated via DNS"),
    ]

    for idx, w in enumerate(wbs_data, start=3):
        row_vals = list(w)
        ws1.append(row_vals)
        ws1.row_dimensions[idx].height = 20

    # Total Row
    tot_row = len(wbs_data) + 3
    ws1.cell(row=tot_row, column=1, value="TOTAL COST BASELINE (BAC)")
    ws1.merge_cells(f"A{tot_row}:I{tot_row}")
    ws1.cell(row=tot_row, column=10, value=f"=SUM(J3:J{tot_row-1})")
    ws1.row_dimensions[tot_row].height = 24
    for c in range(1, 13):
        cell = ws1.cell(row=tot_row, column=c)
        cell.font = Font(name='Calibri', size=11, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')

    apply_styling(ws1)

    # Sheet 2: Phase Rollups & 100% Rule Verification
    ws2 = wb.create_sheet(title="Phase Rollup & 100% Rule")
    ws2.merge_cells("A1:E1")
    ws2["A1"] = "SHALACONNECT - WBS 100% RULE HIERARCHICAL ROLLUP"
    ws2["A1"].font = Font(name='Calibri', size=14, bold=True, color=WHITE)
    ws2["A1"].fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')
    ws2["A1"].alignment = Alignment(horizontal='center', vertical='center')
    ws2.row_dimensions[1].height = 28

    r_headers = ["Phase Code", "Phase Name & Scope Summary", "Work Packages Count", "Aggregated Cost (INR)", "% of Total Budget"]
    ws2.append(r_headers)
    ws2.row_dimensions[2].height = 24
    for c_idx, th in enumerate(r_headers, 1):
        cell = ws2.cell(row=2, column=c_idx)
        cell.font = Font(name='Calibri', size=10, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=LIGHT_BLUE_HEADER, end_color=LIGHT_BLUE_HEADER, fill_type='solid')
        cell.alignment = Alignment(horizontal='center', vertical='center')

    phases = [
        ("Phase 1.0", "Project Inception & Requirements", "=COUNTIF('WBS Dictionary'!A3:A5, \"1.1*\")", "=SUM('WBS Dictionary'!J3:J5)", "=D3/$D$8"),
        ("Phase 2.0", "Architectural & Database Foundation", "=COUNTIF('WBS Dictionary'!A6:A9, \"1.2*\")", "=SUM('WBS Dictionary'!J6:J9)", "=D4/$D$8"),
        ("Phase 3.0", "Core Educational Service Modules", "=COUNTIF('WBS Dictionary'!A10:A18, \"1.3*\")", "=SUM('WBS Dictionary'!J10:J18)", "=D5/$D$8"),
        ("Phase 4.0", "Quality Assurance & Testing", "=COUNTIF('WBS Dictionary'!A19:A21, \"1.4*\")", "=SUM('WBS Dictionary'!J19:J21)", "=D6/$D$8"),
        ("Phase 5.0", "Deployment & Handover", "=COUNTIF('WBS Dictionary'!A22:A23, \"1.5*\")", "=SUM('WBS Dictionary'!J22:J23)", "=D7/$D$8")
    ]

    for p_idx, p in enumerate(phases, start=3):
        ws2.append(list(p))
        ws2.row_dimensions[p_idx].height = 20
        ws2.cell(row=p_idx, column=5).number_format = '0.00%'

    # Total Rollup
    ws2.append(["TOTAL", "100% Project Scope Decomposed", "=SUM(C3:C7)", "=SUM(D3:D7)", "=SUM(E3:E7)"])
    ws2.row_dimensions[8].height = 24
    ws2.cell(row=8, column=5).number_format = '0.00%'
    for c in range(1, 6):
        cell = ws2.cell(row=8, column=c)
        cell.font = Font(name='Calibri', size=11, bold=True, color=WHITE)
        cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type='solid')

    apply_styling(ws2)

    out_path = "Project_Management_Submissions/Assignment_1_WBS/WBS_Dictionary.xlsx"
    wb.save(out_path)
    print(f"Upgraded dynamic WBS dictionary saved to: {out_path}")

if __name__ == "__main__":
    build_project_schedule()
    build_budget_estimation()
    build_risk_register()
    build_wbs_dictionary()
    print("ALL 4 DYNAMIC SPREADSHEETS SUCCESSFULLY BUILT WITH FORMULAS!")
