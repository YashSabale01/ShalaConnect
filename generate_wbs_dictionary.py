import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

output_file = r"d:\java\New folder\ShalaConnect\Project_Management_Submissions\Assignment_1_WBS\WBS_Dictionary.xlsx"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "WBS Dictionary (PMBOK 7th)"

# Styles
font_hdr = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
fill_hdr = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
border_thin = Border(left=Side(style='thin', color='CBD5E1'),
                     right=Side(style='thin', color='CBD5E1'),
                     top=Side(style='thin', color='CBD5E1'),
                     bottom=Side(style='thin', color='CBD5E1'))

headers = [
    "WBS ID", "Work Package Name", "Description & Objectives", 
    "Scope Boundaries", "Deliverable(s)", "Acceptance Criteria", 
    "Responsible Role / Team", "Required Resources", 
    "Duration (Days)", "Dependencies", "Cost (INR)", "Key Assumptions"
]

ws.append(headers)
for col_idx in range(1, len(headers) + 1):
    c = ws.cell(row=1, column=col_idx)
    c.font = font_hdr
    c.fill = fill_hdr
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# 21 Work Packages
wbs_data = [
    (
        "1.1.1", "Stakeholder Needs Elicitation & Field Surveys",
        "Conduct structured interviews and surveys with CRC Kendra Pramukhs and rural School Headmasters across Pune/Haveli cluster to gather operational workflows and pain points.",
        "Covers Maharashtra Zilla Parishad school admin workflows; excludes urban private international school systems.",
        "Stakeholder Survey Report & Voice of Customer (VoC) Matrix.",
        "Sign-off from at least 1 CRC Kendra Pramukh and 3 School Headmasters on documented operational gaps.",
        "Project Manager / Business Analyst", "Survey instruments, Google Forms, field visit kit",
        3, "None", 14000, "Headmasters are accessible during regular administrative hours."
    ),
    (
        "1.1.2", "Software Requirements Specification (SRS) & Traceability",
        "Synthesize field findings into formal IEEE 830-compliant SRS defining functional, non-functional, and data requirements along with traceability matrix.",
        "Covers complete software functional scope; excludes hardware procurement specifications.",
        "Approved SRS Document v1.0 and Initial Requirements Traceability Matrix.",
        "Formal sign-off by Faculty Project Guide and evaluation committee; 100% coverage of core user stories.",
        "Systems Analyst / Technical Lead", "IEEE 830 templates, Confluence/Markdown tools",
        4, "1.1.1", 16000, "Requirements remain stable throughout implementation baseline."
    ),
    (
        "1.1.3", "Regulatory Governance & DPDP Act 2023 Compliance",
        "Map architectural data flows against Indian Digital Personal Data Protection (DPDP) Act 2023 and RTE Act mandates regarding student privacy.",
        "Covers student and teacher PII data protection; excludes cross-border data transfer protocols.",
        "DPDP Compliance Matrix & Data Privacy Governance Policy.",
        "Zero unencrypted PII in transit or rest; mandatory AWS Asia Pacific (Mumbai) region hosting verified.",
        "Security & Compliance Specialist", "Legal compliance checklists, DPDP 2023 statutory guidelines",
        3, "1.1.2", 12000, "Statutory compliance guidelines remain unchanged during project cycle."
    ),
    (
        "1.2.1", "Multi-Tenant Relational Data Modeling (PostgreSQL 16)",
        "Design 3NF relational schema supporting multi-tenancy, school UDISE indexing, cascading integrity, and dynamic JSON schema storage.",
        "Covers 13 application tables (users, schools, attendance, GR, meetings, events, forms); excludes analytics warehouse.",
        "ER Diagram, SQL Schema DDL (init.sql), and JPA Entity Mapping specifications.",
        "Clean migration script execution in PostgreSQL 16; foreign key enforcement and query execution < 50ms.",
        "Database Architect / Lead Backend Dev", "dbdiagram.io, PostgreSQL 16 local runtime, pgAdmin",
        4, "1.1.2, 1.1.3", 20000, "PostgreSQL 16 JSONB/TEXT capabilities suffice for dynamic form schemas."
    ),
    (
        "1.2.2", "RESTful API Specifications & Contracts (OpenAPI 3.0)",
        "Formulate standardized REST API contracts across 10 controllers including auth, attendance, GR, meetings, and forms.",
        "Covers all backend JSON API interfaces; excludes third-party payment or SMS gateway APIs.",
        "OpenAPI 3.0 (Swagger) Specification and Postman Collection.",
        "100% API endpoints defined with request validation schemas, HTTP status codes, and mock responses.",
        "Backend Lead", "Stoplight / Swagger Editor, Postman",
        4, "1.2.1", 18000, "REST architecture satisfies all client-server communication requirements."
    ),
    (
        "1.2.3", "Bilingual Marathi/English UI/UX Design & Offline Prototypes",
        "Design wireframes and interactive Figma prototypes featuring bilingual Marathi/English switcher and responsive mobile-first views.",
        "Covers Headmaster portal, Admin dashboard, and Public transparency views; excludes desktop-only layouts.",
        "Figma Interactive Prototype & Design Component Library.",
        "Usability validation with 90%+ navigation success rate among non-technical Marathi-speaking users.",
        "UI/UX Designer & Frontend Lead", "Figma, Tailwind UI kits, Devanagari web font sets",
        5, "1.1.2", 22000, "Devanagari typography renders uniformly across Android Chrome and desktop."
    ),
    (
        "1.2.4", "AWS Cloud Architecture & Infrastructure Blueprint",
        "Design cloud-native architecture blueprint spanning VPC, multi-AZ RDS, ECS Fargate, ALB, S3, and CloudFront CDN.",
        "Covers AWS production deployment architecture; excludes on-premise physical server hosting.",
        "Architecture Diagram (architecture.drawio) and Cloud Cost Model.",
        "Zero single point of failure for database; monthly AWS operational cost < $50 USD during pilot.",
        "Cloud Architect / DevOps Engineer", "AWS Architecture Center, draw.io, AWS Pricing Calculator",
        4, "1.2.1, 1.2.2", 18000, "AWS Free Tier and educational credits apply to eligible services."
    ),
    (
        "1.3.1", "Multi-Tenant RBAC & JWT Security Module",
        "Implement Spring Security filter chain with stateless HMAC-SHA256 JWT tokens, BCrypt password hashing, and role checks (ADMIN, HEADMASTER).",
        "Covers API authentication, session validation, and tenant context binding; excludes OAuth2 social logins.",
        "SecurityConfig.java, JwtAuthFilter.java, JwtUtil.java, and auth REST endpoints.",
        "Rejection of unauthorized API calls with 401/403 status; tamper-proof token signature verification.",
        "Backend Security Engineer", "Java 21, JJWT 0.12.3, Spring Security 6.x",
        5, "1.2.1, 1.2.2", 22000, "Stateless JWT handles horizontal scaling without sticky sessions."
    ),
    (
        "1.3.2", "Daily Attendance Engine, Tenancy Validation & Offline Sync",
        "Develop daily student/teacher attendance logging with multi-tenant tenancy checks, offline localStorage queue, auto-sync, and 30-day graphs.",
        "Covers school-level daily logging and cluster aggregate views; excludes individual biometric attendance hardware.",
        "AttendanceController, AttendanceService, and SubmitAttendancePage.jsx.",
        "Attendance submitted successfully in < 1 sec; offline submissions cached locally and auto-pushed upon reconnection.",
        "Full-Stack Developer", "Spring Data JPA, React Hook Form, Recharts, LocalStorage API",
        7, "1.3.1, 1.2.3", 32000, "Mobile browsers support HTML5 LocalStorage and offline online events."
    ),
    (
        "1.3.3", "BEO Monthly Excel Compliance Report Engine (Apache POI)",
        "Build server-side Excel generation engine formatting school-wise attendance percentages, compliance flags (Regular, Partial, Defaulter), and totals.",
        "Covers official BEO monthly cluster report card format; excludes arbitrary ad-hoc CSV exports.",
        "AttendanceExportService using Apache POI and Admin Attendance Export endpoint.",
        "Generates multi-sheet .xlsx file with formulas and styling in < 3 seconds for 50+ schools.",
        "Backend Developer", "Apache POI 5.2.5, OpenXML schemas",
        5, "1.3.2", 24000, "Cluster size is typically 20 to 60 schools per Kendra Pramukh."
    ),
    (
        "1.3.4", "Government Resolutions (GR) Circulars & Read-Receipt Tracker",
        "Implement PDF circular upload (up to 20MB), metadata tagging, Amazon S3 storage, and headmaster seen/read timestamp tracking.",
        "Covers PDF circular distribution and read acknowledgments; excludes in-app document PDF editing.",
        "GrController, GrService, and HeadmasterGrPage.jsx.",
        "Admins can upload 20MB PDFs; headmaster read-status updates instantaneously with audit timestamps.",
        "Full-Stack Developer", "Spring Multipart, AWS S3 SDK / FileStorageService, PDF.js",
        4, "1.3.1", 18000, "Circulars are distributed primarily as standardized PDF documents."
    ),
    (
        "1.3.5", "Cluster Review Meeting Scheduler & Attendance Acknowledgment",
        "Develop meeting scheduling system with venue details, video conference URLs, agenda topics, and headmaster attendance RSVP.",
        "Covers meeting creation, notification broadcasting, and RSVP logging; excludes built-in video streaming server.",
        "MeetingController, MeetingService, and MeetingsPage.jsx.",
        "Upcoming meetings displayed in chronological order; headmasters can confirm attendance with one click.",
        "Full-Stack Developer", "Spring Data JPA, React Modal, Lucide Icons",
        3, "1.3.1", 16000, "Online meetings use external links (Google Meet / Zoom)."
    ),
    (
        "1.3.6", "School Celebration Events & Multi-Photo Cloud Proof Gallery",
        "Implement cluster event announcements, school implementation submissions, multi-photo file uploads, and public celebration gallery.",
        "Covers photo upload, deduplication, thumbnail generation, and public viewing; excludes video media uploads.",
        "EventController, EventImplementationService, and PublicPortal event cards.",
        "Headmasters can upload multiple event photos; images render cleanly in responsive grid on public portal.",
        "Full-Stack Developer", "Spring Multipart, S3 / Local storage adapter, Tailwind Grid",
        4, "1.3.1, 1.2.3", 20000, "Average event photo payload is compressed to < 3MB per photo."
    ),
    (
        "1.3.7", "Dynamic Form Builder & Aggregation Engine",
        "Build administrative form builder supporting TEXT, NUMBER, SELECT, DATE, CHECKBOX, multi-row repeated entries, and tabular Excel export.",
        "Covers custom ad-hoc survey data collection from schools; excludes complex conditional branch logic.",
        "DynamicFormController, FormResponseService, FormsPage.jsx, and HeadmasterFormsPage.jsx.",
        "Admins can dynamically publish new survey questionnaires; school responses aggregated into tabular Excel download.",
        "Senior Full-Stack Developer", "PostgreSQL JSON text type, React dynamic form renderers, Apache POI",
        6, "1.3.1, 1.3.3", 26000, "Dynamic survey formats change frequently based on DIET/BEO directives."
    ),
    (
        "1.3.8", "Public Transparency Portal & School Directory",
        "Develop unauthenticated public portal featuring UDISE code search, village filters, school facilities, student count, and topper highlights.",
        "Covers public read-only views; excludes citizen feedback forms or forum comments.",
        "PublicController, PublicPortal.jsx, and PublicSchoolDetail.jsx.",
        "Instant school search filtering; public access requires zero authentication or login prompts.",
        "Frontend Developer", "React Router, Tailwind CSS, Lucide Icons",
        4, "1.2.3", 18000, "UDISE directory data is public government information under RTI Act."
    ),
    (
        "1.4.1", "Modular AWS Infrastructure as Code (Terraform Provisioning)",
        "Write declarative Terraform modules for VPC, public/private subnets, Security Groups, ALB, ECS Fargate, ECR, RDS PostgreSQL, and S3.",
        "Covers AWS production cloud environment; excludes multi-cloud Azure/GCP provisioning.",
        "Terraform suite (vpc.tf, alb.tf, ecs.tf, rds.tf, s3.tf, cloudfront.tf, outputs.tf).",
        "terraform apply executes with zero errors, outputting CloudFront URL and active ECS service status.",
        "DevOps Engineer", "Terraform CLI >= 1.5.0, AWS Provider >= 5.0, AWS CLI",
        5, "1.2.4", 28000, "Target AWS account has sufficient service quotas for VPC and ECS Fargate."
    ),
    (
        "1.4.2", "CI/CD Pipeline Automation (GitHub Actions to ECR & ECS Fargate)",
        "Configure automated GitHub Actions workflow (.github/workflows/deploy.yml) building Docker images, pushing to ECR, and syncing S3/CloudFront.",
        "Covers continuous integration and deployment for main branch; excludes staging blue-green router.",
        ".github/workflows/deploy.yml and Dockerfile configurations.",
        "git push origin main triggers parallel builds completing successfully in under 6 minutes.",
        "DevOps Engineer", "GitHub Actions runner, Docker, AWS ECR, AWS ECS CLI",
        4, "1.4.1", 22000, "Repository secrets (AWS credentials) are pre-configured."
    ),
    (
        "1.4.3", "Performance Optimization, Database Indexing & Security Audit",
        "Profile API response times, add composite indexes on school_id and attendance_date, tune JVM memory parameters, and run OWASP vulnerability scan.",
        "Covers application and database performance tuning; excludes penetration testing of AWS core infrastructure.",
        "Database Index Migration Scripts and Security Audit Report.",
        "API p95 latency < 120ms under 100 concurrent requests; zero critical OWASP vulnerabilities detected.",
        "Backend Lead / Security Auditor", "JMeter, SonarQube, PostgreSQL EXPLAIN ANALYZE, OWASP ZAP",
        3, "1.4.2, 1.3.2", 18000, "Standard 2-core Fargate task provides adequate CPU/RAM throughput."
    ),
    (
        "1.5.1", "Automated Test Suite (JUnit, Mockito, Cypress / E2E)",
        "Develop comprehensive automated unit and integration tests verifying tenancy isolation, attendance submission, and Excel export validity.",
        "Covers automated backend and frontend regression tests; excludes manual exploratory testing.",
        "Automated Test Suite with > 80% code coverage report.",
        "All test cases pass green in CI/CD pipeline prior to deployment; zero tenancy bleed defects.",
        "QA / Test Automation Engineer", "JUnit 5, Mockito, Testcontainers, Postman Newman",
        4, "1.3.8, 1.4.2", 20000, "Test database instances spin up reliably in Docker containers."
    ),
    (
        "1.5.2", "Field Pilot Rollout & User Acceptance Testing (CRC UAT)",
        "Conduct pilot rollout across 5 test schools in Pune cluster; validate daily attendance logging, BEO export, and Marathi UI comprehension.",
        "Covers live field acceptance by designated Kendra Pramukh and headmasters; excludes statewide deployment.",
        "Signed UAT Acceptance Report and Feedback Log.",
        "Formal user sign-off confirming system suitability and zero showstopper defects.",
        "Project Manager & Lead Developer", "Test school credentials, demo mobile handsets, feedback forms",
        3, "1.5.1", 14000, "Pilot users are willing to test parallel to manual paper registers."
    ),
    (
        "1.5.3", "Project Documentation, User Manuals & Academic Submission",
        "Author comprehensive bilingual User Manual, System Administration Guide, Academic Project Report, and VIVA presentation deck.",
        "Covers complete academic project documentation; excludes commercial marketing brochures.",
        "Project Report, User Manuals (English/Marathi), and VIVA Defense Slide Deck.",
        "Full compliance with MITAOE formatting standards and approval by academic guide.",
        "Technical Writer / Project Lead", "MS Word, PowerPoint, LaTeX, Markdown tools",
        3, "1.5.2", 12000, "Academic committee requirements follow MITAOE B.Tech guidelines."
    )
]

for row_idx, r_data in enumerate(wbs_data, start=2):
    ws.append(r_data)
    fill_row = PatternFill(start_color="F8FAFC" if row_idx % 2 == 1 else "FFFFFF", fill_type="solid")
    for col_idx in range(1, len(r_data) + 1):
        cell = ws.cell(row=row_idx, column=col_idx)
        cell.font = Font(name="Calibri", size=9.5)
        cell.fill = fill_row
        cell.border = border_thin
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if col_idx in [1, 9, 10]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx == 11:
            cell.alignment = Alignment(horizontal="right", vertical="center")
            cell.number_format = '"₹"#,##0'

# Summary Row
tot_row = len(wbs_data) + 2
ws.cell(row=tot_row, column=1, value="TOTAL")
ws.cell(row=tot_row, column=2, value="Aggregated Project Baseline (21 Work Packages)")
ws.cell(row=tot_row, column=9, value="80 Days (16 Wks)")
ws.cell(row=tot_row, column=11, value=410000)

font_bold = Font(name="Calibri", size=10, bold=True, color="000000")
fill_tot = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
for c_idx in range(1, len(headers) + 1):
    c = ws.cell(row=tot_row, column=c_idx)
    c.font = font_bold
    c.fill = fill_tot
    c.border = border_thin
    if c_idx == 11:
        c.number_format = '"₹"#,##0'
        c.alignment = Alignment(horizontal="right", vertical="center")
    elif c_idx in [1, 9]:
        c.alignment = Alignment(horizontal="center", vertical="center")

col_widths = [10, 26, 38, 28, 26, 32, 22, 24, 14, 14, 15, 30]
for idx, w in enumerate(col_widths, start=1):
    ws.column_dimensions[get_column_letter(idx)].width = w

wb.save(output_file)
print(f"Generated WBS_Dictionary.xlsx successfully at {output_file}")
