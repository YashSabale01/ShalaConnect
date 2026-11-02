import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

base_dir = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_4_Risk_Management"
os.makedirs(base_dir, exist_ok=True)
output_file = os.path.join(base_dir, "Risk_Register.xlsx")

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Master Risk Register"

font_hdr = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
fill_hdr = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
border_thin = Border(left=Side(style='thin', color='CBD5E1'),
                     right=Side(style='thin', color='CBD5E1'),
                     top=Side(style='thin', color='CBD5E1'),
                     bottom=Side(style='thin', color='CBD5E1'))

headers = [
    "Risk ID", "Type", "Risk Title & Description", "RBS Category", 
    "Root Cause", "Risk Event", "Potential Consequence", 
    "Inherent P (1-5)", "Inherent I (1-5)", "Inherent Score", "Priority", 
    "Risk Owner", "Strategy", "Mitigation Action Plan", "Contingency Action", 
    "Trigger Condition", "Resid P", "Resid I", "Residual Score", "Status"
]

ws.append(headers)
for c_i in range(1, len(headers) + 1):
    c = ws.cell(row=1, column=c_i)
    c.font = font_hdr
    c.fill = fill_hdr
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# 20 Risks (16 Threats + 4 Opportunities)
risks_master = [
    (
        "RSK-01", "Threat", "Offline Attendance Sync Conflict", "Technical",
        "Multiple school staff editing attendance concurrently offline on separate phones.",
        "Conflicting student headcounts submitted simultaneously upon internet reconnection.",
        "Data inconsistency in daily attendance records and corrupt BEO monthly reporting.",
        4, 4, 16, "CRITICAL", "Full-Stack Lead", "Mitigate",
        "Implement server-side timestamp conflict resolution and deterministic database unique constraint on (school_id, attendance_date).",
        "Prompt headmaster to review conflict diff and force authoritative headmaster submission.",
        "HTTP 409 Conflict returned by /api/attendance endpoint during queue flush.",
        2, 2, 4, "Active Monitoring"
    ),
    (
        "RSK-02", "Threat", "AWS Cloud Infrastructure Cost Overrun", "Cost",
        "Unbudgeted compute scaling or forgotten idle resources in AWS dev environment.",
        "Monthly AWS hosting bill exceeds student capstone academic allocation (> INR 10,000/mo).",
        "Premature depletion of project contingency reserve and service suspension risk.",
        4, 3, 12, "HIGH", "DevOps Engineer", "Mitigate",
        "Codify 100% Terraform with serverless ECS Fargate, single-AZ RDS for non-prod, and strict AWS Budgets threshold alerts.",
        "Auto-shutdown non-essential containers outside school hours (6:00 PM to 7:00 AM) using AWS EventBridge.",
        "AWS billing alert reaches 80% of monthly allocated threshold ($40 USD).",
        2, 2, 4, "Active Monitoring"
    ),
    (
        "RSK-03", "Threat", "Dynamic Form Schema JSON Incompatibility", "Technical",
        "Admins altering field schemas while school responses are actively being collected.",
        "Existing JSON answers fail schema validation or cause rendering crashes on headmaster view.",
        "Inability to aggregate responses into Excel export and loss of survey compliance data.",
        3, 3, 9, "MEDIUM", "Backend Lead", "Mitigate",
        "Implement immutable semantic versioning for form schemas; alterations create a new version without mutating live schema.",
        "Fallback JSON lenient parser rendering raw responses even if schema definitions change.",
        "NullPointerException or JsonParseException during /api/forms/{id}/export execution.",
        1, 2, 2, "Active Monitoring"
    ),
    (
        "RSK-04", "Threat", "Apache POI JVM Memory Heap Exhaustion", "Technical",
        "Loading complete cluster attendance dataset for 50+ schools into memory for Excel workbook styling.",
        "Spring Boot JVM heap memory spike causing OutOfMemoryError (OOM) and ECS container crash.",
        "502 Bad Gateway error on BEO export endpoint and server-wide denial of service.",
        3, 4, 12, "HIGH", "Backend Developer", "Mitigate",
        "Implement streaming Apache POI SXSSFWorkbook engine with 100-row sliding window to keep memory footprint < 64MB.",
        "Offload report generation to asynchronous background worker thread returning download ticket.",
        "JVM heap memory usage exceeds 85% during /api/attendance/export-monthly call.",
        1, 3, 3, "Active Monitoring"
    ),
    (
        "RSK-05", "Threat", "Cross-Tenant Horizontal Privilege Escalation", "Security",
        "Missing tenancy check in path parameter IDs (e.g. /api/schools/{id} or /attendance/{id}).",
        "Malicious or curious user accesses/edits attendance or survey data belonging to foreign school.",
        "Severe data privacy breach, violation of Zilla Parishad trust, and project disqualification.",
        3, 5, 15, "CRITICAL", "Security Lead", "Avoid",
        "Enforce strict JWT bearer claims tenancy binding in Spring Security filter and custom @PreAuthorize annotations.",
        "Immediate session revocation, IP ban, and automated alert dispatch to Cluster Administrator.",
        "Mismatch between JWT token school_id claim and request payload school_id.",
        1, 3, 3, "Active Monitoring"
    ),
    (
        "RSK-06", "Threat", "CI/CD Deployment Pipeline Rolling Breakage", "Operational",
        "Broken unit test or bad Dockerfile dependency breaking automated GitHub Actions deploy.",
        "Deployment job fails mid-flight, leaving ECS cluster in inconsistent state.",
        "Downtime during school morning attendance window (9:00 AM to 11:00 AM).",
        3, 3, 9, "MEDIUM", "DevOps Engineer", "Mitigate",
        "Automated multi-stage Docker tests in CI before triggering ECS deployment; keep previous task definition active.",
        "One-click ECS task definition rollback to previous verified image tag via AWS CLI.",
        "GitHub Actions deploy job exits with non-zero exit code on main branch push.",
        1, 2, 2, "Active Monitoring"
    ),
    (
        "RSK-07", "Threat", "Unrestricted S3 Photo Storage Quota Spike", "Cost",
        "Headmasters uploading uncompressed 15MB camera photos for school celebration proofs.",
        "Rapid exhaustion of S3 storage tier and high CloudFront CDN egress bandwidth costs.",
        "Cloud budget exhaustion and slow page loading on mobile public transparency portal.",
        3, 3, 9, "MEDIUM", "Full-Stack Dev", "Mitigate",
        "Enforce client-side Canvas image compression (< 2MB) and server-side image resizer before S3 upload.",
        "Move older event photos (> 90 days) to Amazon S3 Glacier Instant Retrieval lifecycle rule.",
        "Individual multipart upload payload exceeds 5MB or S3 daily ingress exceeds 2GB.",
        1, 2, 2, "Active Monitoring"
    ),
    (
        "RSK-08", "Threat", "Meeting Non-Acknowledgment & Circular Ignorance", "Operational",
        "Headmasters failing to review published circulars or acknowledge cluster meetings.",
        "Critical regulatory deadlines missed across multiple cluster schools.",
        "CRC Administrator must spend hours placing manual telephone calls to field schools.",
        3, 2, 6, "MEDIUM", "Full-Stack Dev", "Mitigate",
        "Prominent in-app notification badge, defaulter summary card on admin dashboard, and 24h reminder push.",
        "Admin one-click automated status check displaying exact list of unacknowledged schools.",
        "Headmaster login without acknowledging pending circulars within 48 hours of publication.",
        2, 1, 2, "Active Monitoring"
    ),
    (
        "RSK-09", "Threat", "Mobile UI Layout Overflow on Budget Android Phones", "Quality",
        "Hardcoded pixel widths causing horizontal scrolling on narrow 360px Android screens.",
        "Headmasters unable to tap submit buttons or view complete attendance tables.",
        "User frustration leading to abandonment and refusal to adopt digital system.",
        3, 2, 6, "MEDIUM", "UI/UX Designer", "Mitigate",
        "Implement fluid responsive Tailwind CSS grid, card-based mobile collapse for tables, and physical mobile testing.",
        "Provide simplified mobile-only touch view with large tap targets and high-contrast typography.",
        "Viewport width < 375px triggers horizontal layout overflow during UI testing.",
        1, 1, 1, "Active Monitoring"
    ),
    (
        "RSK-10", "Threat", "Statutory Non-Compliance with Indian DPDP Act 2023", "Legal",
        "Storage of minor student PII data without appropriate encryption or legal safeguards.",
        "Statutory violation of Indian data protection laws incurring severe legal liability.",
        "Platform forced to shut down immediately by university authorities or regulatory officers.",
        3, 5, 15, "CRITICAL", "Lead Architect", "Avoid",
        "Mandatory data residency in AWS Asia Pacific (Mumbai) ap-south-1 region; AES-256 encryption at rest and TLS 1.3 in transit.",
        "Comprehensive Data Protection Impact Assessment (DPIA) and student data anonymization in public portal.",
        "Any unencrypted PII field detected in database logs or external network requests.",
        1, 3, 3, "Active Monitoring"
    ),
    (
        "RSK-11", "Threat", "Key Developer Single-Point-of-Failure (SPoF)", "Resource",
        "Illness or academic emergency affecting the primary full-stack developer.",
        "Critical path activities stalled during core implementation phase.",
        "Project schedule slip beyond 54-day baseline, consuming operational schedule buffer.",
        3, 4, 12, "HIGH", "Project Manager", "Mitigate",
        "Maintain modular decoupled code, exhaustive OpenAPI 3.0 documentation, and pair programming cross-training.",
        "Activate secondary team member to take over predefined work packages using documented task cards.",
        "Lead developer unavailable for more than 3 consecutive working days during sprint.",
        1, 2, 2, "Active Monitoring"
    ),
    (
        "RSK-12", "Threat", "Academic Semester Examination Schedule Crunch", "Schedule",
        "University mid-term or internal practical exams scheduled during testing phase.",
        "Development halts for 10-14 days during critical QA and pilot rollout window.",
        "Risk of rushed testing, compromised code quality, or delayed final project submission.",
        4, 2, 8, "MEDIUM", "Project Manager", "Mitigate",
        "Build 26-day operational buffer into 54-day schedule baseline (total academic window: 80 days).",
        "Crash critical path activities prior to exam week by pre-completing automated test suites.",
        "Announcement of institutional examination timetable overlapping with Phase 1.5.",
        2, 1, 2, "Active Monitoring"
    ),
    (
        "RSK-13", "Threat", "Rural Telecom Network Blackout Exceeding 48 Hours", "External",
        "Fibre optic cable cut or severe monsoon weather knocking out rural cellular towers.",
        "Headmasters unable to transmit cached attendance for 3 or more consecutive school days.",
        "Cluster attendance data lag and absence of daily mid-day meal monitoring data.",
        2, 3, 6, "MEDIUM", "Full-Stack Dev", "Accept",
        "Extend offline localStorage cache capacity to retain up to 30 days of daily attendance history.",
        "Headmaster can export encrypted local attendance backup file and sync via CRC office Wi-Fi during weekly visit.",
        "Device offline state persists continuously for > 48 hours without reconnect trigger.",
        2, 1, 2, "Active Monitoring"
    ),
    (
        "RSK-14", "Threat", "Brute-Force Credential Stuffing on Admin Login", "Security",
        "Automated bots attempting dictionary attacks against admin@shalaconnect.in endpoint.",
        "Potential compromise of cluster administrative account and unauthorized data access.",
        "Loss of data integrity and necessity for emergency database credential resets.",
        3, 3, 9, "MEDIUM", "Security Lead", "Mitigate",
        "Implement Spring Security rate limiting (5 failed attempts locks account for 15 minutes) and BCrypt work factor 12.",
        "Admin receives immediate email alert with IP address; mandatory password reset enforced.",
        "> 5 failed authentication attempts for single email within a 3-minute window.",
        1, 2, 2, "Active Monitoring"
    ),
    (
        "RSK-15", "Threat", "Database Connection Pool Starvation at 9:00 AM", "Technical",
        "All 50 headmasters logging in and submitting attendance simultaneously between 9:00 and 9:30 AM.",
        "PostgreSQL connection pool (HikariCP) exhausted, causing connection timeout exceptions.",
        "Headmasters experience HTTP 500 errors and failed attendance submissions.",
        3, 4, 12, "HIGH", "Database Architect", "Mitigate",
        "Configure HikariCP maximum pool size to 30, enable connection leak detection, and add connection timeout handling.",
        "Frontend queues requests and retries with exponential backoff; local cache preserves submission.",
        "HikariCP active connections exceed 85% of pool capacity.",
        1, 2, 2, "Active Monitoring"
    ),
    (
        "RSK-16", "Threat", "Corrupted Multipart PDF Upload Breaking Viewer", "Quality",
        "Admin uploading truncated or malformed PDF circular causing browser PDF.js rendering crash.",
        "Headmasters unable to open or read official policy resolution.",
        "Administrative confusion and communication breakdown across cluster schools.",
        2, 3, 6, "MEDIUM", "Backend Dev", "Mitigate",
        "Server-side PDF header validation and Apache PDFBox parsing check before saving to S3 document vault.",
        "Display download button allowing user to inspect file using native external PDF application.",
        "Uploaded document fails Apache PDFBox integrity check upon upload.",
        1, 1, 1, "Active Monitoring"
    ),
    (
        "OPP-17", "Opportunity", "PWA Offline Service Worker Zero-Data Caching", "Technical",
        "HTML5 progressive web app service worker caching static assets permanently.",
        "App loads instantly (< 300ms) with zero cellular data consumption for returning headmasters.",
        "Drastically enhanced rural user satisfaction and negligible CloudFront CDN transfer costs.",
        4, 3, 12, "HIGH", "Frontend Lead", "Exploit",
        "Implement aggressive Workbox cache-first caching strategy for static CSS/JS and school profile assets.",
        "Pre-cache cluster school directory during initial Wi-Fi connection.",
        "Service worker registration confirmed on client browser.",
        4, 4, 16, "Active Tracking"
    ),
    (
        "OPP-18", "Opportunity", "State Education Department PM-SHRI Accreditation", "Operational",
        "Demonstrated success of BEO Excel export and transparency portal during pilot.",
        "State educational authorities adopt ShalaConnect as official cluster compliance template.",
        "Institutional recognition for MITAOE engineering program and potential grant funding.",
        3, 4, 12, "HIGH", "Project Manager", "Enhance",
        "Present pilot results directly to Block Education Officer and prepare formal case study report.",
        "Submit platform documentation to Maharashtra State Council of Educational Research and Training (SCERT).",
        "BEO issues positive commendation letter on report export accuracy.",
        3, 4, 12, "Active Tracking"
    ),
    (
        "OPP-19", "Opportunity", "AWS Cloud Credit Academic Grant Approval", "Cost",
        "Eligibility for AWS Educate / Cloud Innovation project grant sponsorship.",
        "Receipt of $500 to $1,000 USD in AWS promotional cloud credits.",
        "Zero net infrastructure cost for production hosting; entire cloud budget saved as surplus.",
        4, 4, 16, "CRITICAL", "DevOps Engineer", "Exploit",
        "Submit formal AWS Educate project proposal detailing architectural topology and social education impact.",
        "Apply credits to production account to eliminate all hosting charges during academic evaluation.",
        "AWS sends credit code notification via email.",
        4, 4, 16, "Active Tracking"
    ),
    (
        "OPP-20", "Opportunity", "Open-Source Developer Community Contributions", "Operational",
        "Publishing modular Spring Boot and React components on GitHub under MIT license.",
        "Peer student developers contribute bug fixes, localized translations, and test suites.",
        "Accelerated development velocity and enhanced code quality at zero financial cost.",
        3, 3, 9, "MEDIUM", "Lead Developer", "Share",
        "Maintain clean public repository, detailed contribution guidelines (CONTRIBUTING.md), and automated CI testing.",
        "Review and merge qualified pull requests from MITAOE student open-source community.",
        "External pull requests submitted to main repository on GitHub.",
        3, 3, 9, "Active Tracking"
    )
]

fill_alt = PatternFill(start_color="F8FAFC", fill_type="solid")
fill_crit = PatternFill(start_color="FEE2E2", fill_type="solid")
fill_high = PatternFill(start_color="FFEDD5", fill_type="solid")
fill_opp = PatternFill(start_color="DCFCE7", fill_type="solid")

for r_idx, r_val in enumerate(risks_master, start=2):
    ws.append(r_val)
    prio = r_val[10]
    is_opp = r_val[1] == "Opportunity"
    f_row = fill_opp if is_opp else (fill_crit if prio == "CRITICAL" else (fill_high if prio == "HIGH" else (fill_alt if r_idx % 2 == 1 else PatternFill(fill_type=None))))
    
    for c_i in range(1, len(r_val) + 1):
        cell = ws.cell(row=r_idx, column=c_i)
        cell.font = Font(name="Calibri", size=9)
        if f_row.fill_type:
            cell.fill = f_row
        cell.border = border_thin
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if c_i in [1, 2, 4, 8, 9, 10, 11, 13, 17, 18, 19, 20]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if c_i in [1, 10, 11, 19]:
                cell.font = Font(name="Calibri", size=9, bold=True)

col_widths = [10, 12, 30, 16, 26, 26, 26, 10, 10, 12, 12, 18, 14, 34, 30, 26, 10, 10, 12, 16]
for idx, w in enumerate(col_widths, start=1):
    ws.column_dimensions[get_column_letter(idx)].width = w

wb.save(output_file)
print(f"Generated Risk_Register.xlsx at {output_file}")
