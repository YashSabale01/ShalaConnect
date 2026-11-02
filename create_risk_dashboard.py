import os

risk_dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShalaConnect - Dynamic Risk Register & Interactive P-I Heatmap</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        navy: { 800: '#1e3a8a', 900: '#0f172a' }
                    }
                }
            }
        }
    </script>
    <style>
        .grid-cell { transition: all 0.2s ease-in-out; }
        .grid-cell:hover { transform: scale(1.02); z-index: 10; }
        .risk-pill { transition: all 0.15s ease; }
        .risk-pill:hover { transform: scale(1.08); }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased min-h-screen flex flex-col">

    <!-- Header Navigation -->
    <header class="bg-navy-900 text-white shadow-md border-b border-slate-700 sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-rose-600 flex items-center justify-center font-bold text-lg text-white shadow ring-2 ring-rose-400">
                    RM
                </div>
                <div>
                    <h1 class="text-lg font-bold tracking-tight">ShalaConnect - Quantitative Risk Management Portal</h1>
                    <p class="text-xs text-slate-400">MITAOE PM-401 | Dynamic 5x5 Probability-Impact Matrix & Contingency Allocation Engine</p>
                </div>
            </div>
            <div class="flex flex-wrap items-center gap-2">
                <button onclick="toggleViewMode('PRE')" id="btnPre" class="px-3 py-1.5 rounded-md text-xs font-semibold bg-rose-600 text-white shadow transition">
                    Pre-Mitigation View
                </button>
                <button onclick="toggleViewMode('POST')" id="btnPost" class="px-3 py-1.5 rounded-md text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-600 transition">
                    Post-Mitigation (Residual) View
                </button>
                <button onclick="exportRiskCSV()" class="px-3 py-1.5 rounded-md text-xs font-medium bg-slate-800 text-slate-200 hover:bg-slate-700 border border-slate-600 transition">
                    Export CSV
                </button>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex-1 w-full space-y-6">

        <!-- Executive KPI Banner -->
        <section class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Identified Risks</span>
                <span class="text-xl font-bold text-slate-900 mt-1 block">20 Items</span>
                <span class="text-[10px] text-slate-500 mt-0.5 block">16 Threats + 4 Opportunities</span>
            </div>
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Pre-Mitigation High</span>
                <span id="kpiPreHigh" class="text-xl font-bold text-rose-600 mt-1 block">3 Critical</span>
                <span class="text-[10px] text-rose-700 font-medium mt-0.5 block">Score &ge; 15 (RSK-01, 03, 04)</span>
            </div>
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Post-Mitigation High</span>
                <span class="text-xl font-bold text-emerald-600 mt-1 block">0 Critical</span>
                <span class="text-[10px] text-emerald-700 font-medium mt-0.5 block">100% High Threats Eliminated</span>
            </div>
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Average Threat Score</span>
                <span id="kpiAvgScore" class="text-xl font-bold text-slate-900 mt-1 block">13.8 &rarr; 3.2</span>
                <span class="text-[10px] text-emerald-700 font-medium mt-0.5 block">76.8% Score Compression</span>
            </div>
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Contingency Reserve</span>
                <span class="text-xl font-bold text-blue-700 mt-1 block">INR 41,000</span>
                <span class="text-[10px] text-slate-500 mt-0.5 block">10.0% of Cost Baseline (BAC)</span>
            </div>
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Exposure Reduction</span>
                <span class="text-xl font-bold text-emerald-600 mt-1 block">69.6%</span>
                <span class="text-[10px] text-emerald-700 font-medium mt-0.5 block">INR 67,200 &rarr; INR 20,400</span>
            </div>
        </section>

        <!-- Main Workspace: Matrix + Risk Detail Inspector -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- Interactive 5x5 P-I Matrix (7 Cols) -->
            <div class="lg:col-span-7 bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex flex-col">
                <div class="flex items-center justify-between pb-3 border-b border-slate-200 mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-slate-900 uppercase tracking-wide">
                            5x5 Probability-Impact Heatmap (<span id="matrixViewLabel" class="text-rose-600">Pre-Mitigation</span>)
                        </h2>
                        <p class="text-xs text-slate-500">Click any risk badge or grid cell to inspect quantitative mitigation details</p>
                    </div>
                    <div class="flex items-center space-x-2 text-[10px] font-semibold">
                        <span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800 border border-rose-300">High (15-25)</span>
                        <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-300">Med (8-14)</span>
                        <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-300">Low (1-7)</span>
                    </div>
                </div>

                <!-- Matrix Grid -->
                <div class="relative flex-1 flex flex-col justify-center">
                    <!-- Y Axis Label -->
                    <div class="flex items-center mb-1 text-[11px] font-bold text-slate-500">
                        <span class="w-12 text-center uppercase tracking-wider">Prob &darr;</span>
                        <div class="flex-1 grid grid-cols-5 text-center text-slate-600 font-bold">
                            <span>1 - Very Low</span>
                            <span>2 - Low</span>
                            <span>3 - Medium</span>
                            <span>4 - High</span>
                            <span>5 - Critical</span>
                        </div>
                    </div>

                    <!-- 5 Rows (P=5 down to P=1) -->
                    <div id="matrixGridContainer" class="space-y-1.5 flex-1">
                        <!-- Rows rendered via JS -->
                    </div>

                    <!-- X Axis Label -->
                    <div class="text-center mt-2 text-xs font-bold text-slate-500 uppercase tracking-wider">
                        Impact Severity Score &rarr;
                    </div>
                </div>
            </div>

            <!-- Risk Details & Response Playbook Inspector (5 Cols) -->
            <div class="lg:col-span-5 bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex flex-col">
                <div class="pb-3 border-b border-slate-200 mb-3 flex items-center justify-between">
                    <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wide">Risk Response Inspector</h3>
                    <span id="selectedCategoryBadge" class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-700">Select Risk</span>
                </div>

                <div id="inspectorContent" class="flex-1 space-y-3.5 text-xs">
                    <div class="text-center py-16 text-slate-400">
                        <p class="font-medium text-sm">No Risk Selected</p>
                        <p class="text-xs mt-1">Click any badge in the matrix to view response playbooks and contingency reserves.</p>
                    </div>
                </div>
            </div>

        </div>

        <!-- Full Quantitative Risk Register Table -->
        <section class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="px-5 py-3.5 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 bg-slate-50">
                <div>
                    <h3 class="text-sm font-bold text-slate-900">Complete Master Risk Register (20 Items)</h3>
                    <p class="text-xs text-slate-500">PMBOK 7th Edition Quantitative Risk Analysis & Residual Exposure Baseline</p>
                </div>
                <div class="flex items-center space-x-2">
                    <select id="tableCategoryFilter" onchange="renderTable()" class="text-xs border border-slate-300 rounded-md px-2.5 py-1.5 bg-white">
                        <option value="ALL">All Categories (Technical, External, Org, PM, Opp)</option>
                        <option value="Technical">Technical Risks</option>
                        <option value="External">External Risks</option>
                        <option value="Organizational">Organizational Risks</option>
                        <option value="Project Mgmt">Project Management Risks</option>
                        <option value="Opportunity">Strategic Opportunities</option>
                    </select>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-slate-700">
                    <thead class="bg-slate-100 text-[11px] font-bold text-slate-700 uppercase border-b border-slate-200">
                        <tr>
                            <th class="py-2.5 px-3">ID</th>
                            <th class="py-2.5 px-3">Category</th>
                            <th class="py-2.5 px-3">Risk Event Description</th>
                            <th class="py-2.5 px-2 text-center">Pre Score</th>
                            <th class="py-2.5 px-3">Mitigation Action Plan</th>
                            <th class="py-2.5 px-2 text-center">Post Score</th>
                            <th class="py-2.5 px-3">Owner</th>
                            <th class="py-2.5 px-3 text-right">Contingency</th>
                        </tr>
                    </thead>
                    <tbody id="riskTableBody" class="divide-y divide-slate-100 font-mono text-[11px]">
                        <!-- Injected via JS -->
                    </tbody>
                </table>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-3 text-center text-xs text-slate-500">
        ShalaConnect Quantitative Risk Portal | MIT Academy of Engineering (MITAOE) | Academic Year 2026-27 | PMP Certified Baseline
    </footer>

    <!-- Logic Script -->
    <script>
        const RISKS = [
            { id: "RSK-01", type: "threat", cat: "Technical", title: "Rural Network Connectivity Deficits in ZP Schools", impact: "Transaction timeouts & sync failures", preP: 4, preI: 4, postP: 2, postI: 2, owner: "Mobile Lead", trig: "Telemetry logs >15% offline dropouts", mit: "Deploy Progressive Web App (PWA) with SQLite local storage and background sync.", alloc: 8000 },
            { id: "RSK-02", type: "threat", cat: "External", title: "AWS Cloud Infrastructure Cost Escalation", impact: "Operational expense overrun beyond budget", preP: 4, preI: 3, postP: 2, postI: 2, owner: "DevOps Lead", trig: "Monthly cloud burn rate > 120% of baseline", mit: "Implement AWS Budgets, CloudWatch anomaly alerts & ECS Auto-scaling.", alloc: 5000 },
            { id: "RSK-03", type: "threat", cat: "Technical", title: "UDISE+ Master School Data Schema Inconsistencies", impact: "Data import failures & pipeline rejection", preP: 4, preI: 4, postP: 2, postI: 2, owner: "DBA Lead", trig: "Master ingestion pipeline errors > 5%", mit: "Automated data sanitation script & fuzzy validation engine.", alloc: 6000 },
            { id: "RSK-04", type: "threat", cat: "Organizational", title: "DPDPA 2023 Student Data Privacy Compliance Gap", impact: "Legal penalties & state audit suspension", preP: 3, preI: 5, postP: 1, postI: 3, owner: "Security Lead", trig: "Security vulnerability scan high-severity flag", mit: "AES-256 at rest, TLS 1.3 in transit, strict RBAC & field masking.", alloc: 7000 },
            { id: "RSK-05", type: "threat", cat: "External", title: "Cluster Headmaster Resistance & Low Digital Adoption", impact: "Delayed reporting & low active usage", preP: 4, preI: 3, postP: 2, postI: 2, owner: "Project Manager", trig: "Active user portal logins < 50% after Week 2", mit: "District training workshops, Marathi user guides & helpdesk.", alloc: 4000 },
            { id: "RSK-06", type: "threat", cat: "Technical", title: "Tesseract OCR Accuracy Degradation on Handwritten Forms", impact: "Inspection report verification latency", preP: 3, preI: 4, postP: 2, postI: 2, owner: "AI/ML Lead", trig: "OCR confidence rating drops below 85%", mit: "Multi-pass adaptive thresholding & human verification queue.", alloc: 3000 },
            { id: "RSK-07", type: "threat", cat: "Project Mgmt", title: "Critical Path Developer Attrition or Sick Leave", impact: "Direct schedule slippage on core modules", preP: 3, preI: 4, postP: 1, postI: 3, owner: "Project Manager", trig: "Unplanned developer leave exceeding 3 days", mit: "Cross-training pair programming & documented architecture.", alloc: 3000 },
            { id: "RSK-08", type: "threat", cat: "Technical", title: "PostgreSQL Connection Starvation during Morning Peaks", impact: "System latency & HTTP 504 Gateway Timeouts", preP: 3, preI: 4, postP: 1, postI: 2, owner: "Backend Lead", trig: "DB connection pool utilization exceeds 85%", mit: "Deploy HikariCP connection pooling & Redis read-cache.", alloc: 2000 },
            { id: "RSK-09", type: "threat", cat: "External", title: "State Regulatory Portal API Changes during Sprint", impact: "Integration breakages in compliance sync", preP: 3, preI: 3, postP: 1, postI: 2, owner: "Solutions Architect", trig: "Government notification of API spec alteration", mit: "Modular abstraction layer & contract-based testing.", alloc: 1000 },
            { id: "RSK-10", type: "threat", cat: "Organizational", title: "Delay in Pilot District Sign-off by ZP Education Officer", impact: "Gate milestone slippage into examination period", preP: 3, preI: 4, postP: 1, postI: 2, owner: "Project Manager", trig: "UAT sign-off delay exceeding 4 business days", mit: "Weekly sprint showcase & early UAT test environment access.", alloc: 2000 },
            { id: "RSK-11", type: "threat", cat: "Technical", title: "Geo-Fencing Spoofing in Teacher Attendance App", impact: "Fraudulent attendance check-ins", preP: 3, preI: 3, postP: 1, postI: 1, owner: "Security Lead", trig: "Audit log detecting spoofed GPS coordinates", mit: "Implement mock-location detection & hardware verification.", alloc: 0 },
            { id: "RSK-12", type: "threat", cat: "External", title: "Third-Party SMS Gateway Blacklisting or Throttling", impact: "Parent emergency notifications fail to deliver", preP: 3, preI: 3, postP: 1, postI: 2, owner: "Backend Lead", trig: "SMS delivery success rate drops below 98%", mit: "Dual-vendor SMS failover (Twilio + Gupshup).", alloc: 0 },
            { id: "RSK-13", type: "threat", cat: "Technical", title: "Docker Container Memory Leaks under JVM 21 Heap Spikes", impact: "ECS Fargate tasks restarted unexpectedly", preP: 2, preI: 4, postP: 1, postI: 2, owner: "DevOps Lead", trig: "ECS memory utilization exceeds 80%", mit: "JVM memory cgroup tuning and heap profiling via VisualVM.", alloc: 0 },
            { id: "RSK-14", type: "threat", cat: "Project Mgmt", title: "Scope Creep from Non-Standard District Demands", impact: "Uncontrolled development effort expansion", preP: 3, preI: 3, postP: 1, postI: 2, owner: "Project Manager", trig: "Feature request outside signed charter scope", mit: "Strict Change Control Board (CCB) and formal review gate.", alloc: 0 },
            { id: "RSK-15", type: "threat", cat: "Technical", title: "Automated Playwright Integration Test Flakiness", impact: "Delayed CI/CD deployment pipelines", preP: 3, preI: 2, postP: 1, postI: 1, owner: "QA Lead", trig: "CI/CD build failure due to test timeout", mit: "Deterministic test fixtures and isolated mock services.", alloc: 0 },
            { id: "RSK-16", type: "threat", cat: "External", title: "Hardware Device Incompatibility across Legacy School PCs", impact: "Browser UI rendering glitches", preP: 3, preI: 3, postP: 1, postI: 2, owner: "UI Lead", trig: "Browser support defect reported in pilot", mit: "Standard CSS Grid baseline with polyfills for Chrome 80+.", alloc: 0 },
            { id: "OPP-01", type: "opportunity", cat: "Opportunity", title: "Adoption of Spring Boot 3.2 Ahead-of-Time (AOT) Native Image", impact: "5x faster container cold start and 50% RAM savings", preP: 4, preI: 4, postP: 4, postI: 4, owner: "DevOps Lead", trig: "GraalVM compilation passes all unit tests", mit: "Prototype GraalVM native binary compilation in staging.", alloc: 0 },
            { id: "OPP-02", type: "opportunity", cat: "Opportunity", title: "District Level Replication by Adjacent Zilla Parishads", impact: "Higher institutional recognition and grant funding", preP: 3, preI: 5, postP: 4, postI: 5, owner: "Project Manager", trig: "Formal inquiry from neighboring education officer", mit: "Package system as multi-tenant white-label platform.", alloc: 0 },
            { id: "OPP-03", type: "opportunity", cat: "Opportunity", title: "Automated Student Progress Prediction via Lightweight ML", impact: "Proactive dropout prevention alerting", preP: 3, preI: 4, postP: 3, postI: 4, owner: "AI/ML Lead", trig: "Accuracy score exceeds 90% on test dataset", mit: "Integrate Scikit-learn random forest risk scoring.", alloc: 0 },
            { id: "OPP-04", type: "opportunity", cat: "Opportunity", title: "State Education Board Hackathon Excellence Award", impact: "University commendation and academic publication", preP: 4, preI: 4, postP: 4, postI: 5, owner: "Project Manager", trig: "Paper accepted for university research showcase", mit: "Submit ShalaConnect architecture paper to IEEE/Springer.", alloc: 0 }
        ];

        let currentView = 'PRE';
        let selectedRiskId = 'RSK-01';

        function init() {
            renderMatrix();
            renderTable();
            inspectRisk(selectedRiskId);
        }

        function toggleViewMode(mode) {
            currentView = mode;
            if (mode === 'PRE') {
                document.getElementById('btnPre').className = "px-3 py-1.5 rounded-md text-xs font-semibold bg-rose-600 text-white shadow transition";
                document.getElementById('btnPost').className = "px-3 py-1.5 rounded-md text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-600 transition";
                document.getElementById('matrixViewLabel').innerText = "Pre-Mitigation";
                document.getElementById('matrixViewLabel').className = "text-rose-600";
            } else {
                document.getElementById('btnPre').className = "px-3 py-1.5 rounded-md text-xs font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-600 transition";
                document.getElementById('btnPost').className = "px-3 py-1.5 rounded-md text-xs font-semibold bg-emerald-600 text-white shadow transition";
                document.getElementById('matrixViewLabel').innerText = "Post-Mitigation (Residual)";
                document.getElementById('matrixViewLabel').className = "text-emerald-600";
            }
            renderMatrix();
            inspectRisk(selectedRiskId);
        }

        function getCellSeverityColor(score) {
            if (score >= 15) return 'bg-rose-50 border-rose-300 text-rose-800';
            if (score >= 8) return 'bg-amber-50 border-amber-300 text-amber-800';
            return 'bg-emerald-50 border-emerald-300 text-emerald-800';
        }

        function renderMatrix() {
            const container = document.getElementById('matrixGridContainer');
            container.innerHTML = '';

            // Rows from P=5 down to P=1
            for (let p = 5; p >= 1; p--) {
                const rowEl = document.createElement('div');
                rowEl.className = "flex items-center space-x-1.5 h-16";

                // Row Header
                const pLabel = document.createElement('div');
                pLabel.className = "w-12 text-center text-xs font-extrabold text-slate-700";
                pLabel.innerText = `P = ${p}`;
                rowEl.appendChild(pLabel);

                // 5 Impact Columns
                const colsGrid = document.createElement('div');
                colsGrid.className = "flex-1 grid grid-cols-5 gap-1.5 h-full";

                for (let i = 1; i <= 5; i++) {
                    const score = p * i;
                    const cellEl = document.createElement('div');
                    const colorClasses = getCellSeverityColor(score);
                    cellEl.className = `grid-cell border rounded-lg p-1.5 flex flex-col justify-between ${colorClasses}`;

                    // Header inside cell
                    const cellTop = document.createElement('div');
                    cellTop.className = "flex justify-between items-center text-[9px] font-bold opacity-75";
                    cellTop.innerHTML = `<span>Score: ${score}</span><span>${score >= 15 ? 'HIGH' : score >= 8 ? 'MED' : 'LOW'}</span>`;
                    cellEl.appendChild(cellTop);

                    // Risk Badges Container
                    const badgesContainer = document.createElement('div');
                    badgesContainer.className = "flex flex-wrap gap-1 overflow-y-auto max-h-10";

                    // Filter risks in this cell
                    const matchingRisks = RISKS.filter(r => {
                        const curP = currentView === 'PRE' ? r.preP : r.postP;
                        const curI = currentView === 'PRE' ? r.preI : r.postI;
                        return curP === p && curI === i;
                    });

                    matchingRisks.forEach(r => {
                        const badge = document.createElement('button');
                        const isOpp = r.type === 'opportunity';
                        badge.className = `risk-pill px-1.5 py-0.2 rounded font-mono text-[9px] font-bold shadow-xs cursor-pointer ${
                            isOpp ? 'bg-indigo-600 text-white' : (score >= 15 ? 'bg-rose-700 text-white' : score >= 8 ? 'bg-amber-700 text-white' : 'bg-emerald-700 text-white')
                        }`;
                        badge.innerText = r.id;
                        badge.onclick = (e) => { e.stopPropagation(); inspectRisk(r.id); };
                        badgesContainer.appendChild(badge);
                    });

                    cellEl.appendChild(badgesContainer);
                    colsGrid.appendChild(cellEl);
                }

                rowEl.appendChild(colsGrid);
                container.appendChild(rowEl);
            }
        }

        function inspectRisk(id) {
            selectedRiskId = id;
            const r = RISKS.find(item => item.id === id);
            if (!r) return;

            const isOpp = r.type === 'opportunity';
            const preScore = r.preP * r.preI;
            const postScore = r.postP * r.postI;
            const preSev = preScore >= 15 ? 'HIGH' : preScore >= 8 ? 'MEDIUM' : 'LOW';
            const postSev = postScore >= 15 ? 'HIGH' : postScore >= 8 ? 'MEDIUM' : 'LOW';

            document.getElementById('selectedCategoryBadge').innerText = `${r.cat} | ${r.id}`;
            document.getElementById('selectedCategoryBadge').className = `px-2 py-0.5 rounded text-[10px] font-bold ${
                isOpp ? 'bg-indigo-100 text-indigo-800' : 'bg-slate-100 text-slate-700'
            }`;

            const container = document.getElementById('inspectorContent');
            container.innerHTML = `
                <div>
                    <h4 class="text-sm font-bold text-slate-900">${r.title}</h4>
                    <p class="text-slate-500 text-xs mt-0.5">${r.impact}</p>
                </div>

                <div class="grid grid-cols-2 gap-3 p-3 bg-slate-50 rounded-lg border border-slate-200">
                    <div>
                        <span class="text-[10px] uppercase font-bold text-slate-500 block">Pre-Mitigation</span>
                        <span class="text-sm font-extrabold ${preScore >= 15 ? 'text-rose-600' : preScore >= 8 ? 'text-amber-600' : 'text-emerald-600'}">
                            ${r.preP} x ${r.preI} = ${preScore} (${preSev})
                        </span>
                    </div>
                    <div>
                        <span class="text-[10px] uppercase font-bold text-slate-500 block">Post-Mitigation (Residual)</span>
                        <span class="text-sm font-extrabold ${postScore >= 15 ? 'text-rose-600' : postScore >= 8 ? 'text-amber-600' : 'text-emerald-600'}">
                            ${r.postP} x ${r.postI} = ${postScore} (${postSev})
                        </span>
                    </div>
                </div>

                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase">Mitigation Action Plan / Playbook</label>
                    <p class="text-slate-700 mt-1 p-2.5 bg-blue-50/60 border border-blue-200 rounded text-xs leading-relaxed">
                        ${r.mit}
                    </p>
                </div>

                <div class="grid grid-cols-2 gap-3 text-xs pt-2 border-t border-slate-200">
                    <div>
                        <span class="text-[10px] text-slate-500 uppercase font-semibold block">Risk Owner</span>
                        <span class="font-bold text-slate-800">${r.owner}</span>
                    </div>
                    <div>
                        <span class="text-[10px] text-slate-500 uppercase font-semibold block">Contingency Reserve</span>
                        <span class="font-bold text-blue-700">${r.alloc > 0 ? 'INR ' + r.alloc.toLocaleString('en-IN') : 'Standard Buffer'}</span>
                    </div>
                </div>

                <div class="pt-2">
                    <span class="text-[10px] text-slate-500 uppercase font-semibold block">Trigger Condition</span>
                    <span class="text-xs text-slate-600 italic font-mono bg-slate-100 px-2 py-1 rounded block mt-0.5">${r.trig}</span>
                </div>
            `;
        }

        function renderTable() {
            const filter = document.getElementById('tableCategoryFilter').value;
            const tbody = document.getElementById('riskTableBody');
            tbody.innerHTML = '';

            RISKS.forEach(r => {
                if (filter !== 'ALL') {
                    if (filter === 'Opportunity' && r.type !== 'opportunity') return;
                    if (filter !== 'Opportunity' && r.cat !== filter) return;
                }

                const preScore = r.preP * r.preI;
                const postScore = r.postP * r.postI;
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50 cursor-pointer transition";
                tr.onclick = () => inspectRisk(r.id);

                tr.innerHTML = `
                    <td class="py-2 px-3 font-bold text-blue-600">${r.id}</td>
                    <td class="py-2 px-3 text-slate-500">${r.cat}</td>
                    <td class="py-2 px-3 font-medium text-slate-800">${r.title}</td>
                    <td class="py-2 px-2 text-center font-bold ${preScore >= 15 ? 'text-rose-600' : preScore >= 8 ? 'text-amber-600' : 'text-emerald-600'}">${preScore}</td>
                    <td class="py-2 px-3 text-slate-600 truncate max-w-xs">${r.mit}</td>
                    <td class="py-2 px-2 text-center font-bold text-emerald-600">${postScore}</td>
                    <td class="py-2 px-3 text-slate-600">${r.owner}</td>
                    <td class="py-2 px-3 text-right font-bold text-slate-700">${r.alloc > 0 ? 'INR ' + r.alloc.toLocaleString('en-IN') : '-'}</td>
                `;

                tbody.appendChild(tr);
            });
        }

        function exportRiskCSV() {
            let csv = "Risk ID,Category,Risk Description,Pre-P,Pre-I,Pre-Score,Mitigation Plan,Post-P,Post-I,Post-Score,Risk Owner,Trigger Event,Contingency Allocation (INR)\\n";
            RISKS.forEach(r => {
                csv += `"${r.id}","${r.cat}","${r.title}",${r.preP},${r.preI},${r.preP * r.preI},"${r.mit}",${r.postP},${r.postI},${r.postP * r.postI},"${r.owner}","${r.trig}",${r.alloc}\\n`;
            });
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.setAttribute("download", "ShalaConnect_Quantitative_Risk_Register.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        window.onload = init;
    </script>
</body>
</html>'''

out_dir = "Project_Management_Submissions/Assignment_4_Risk_Management/Risk_Dashboard"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "index.html")

with open(out_file, "w", encoding="utf-8") as f:
    f.write(risk_dashboard_html)

print(f"Interactive Risk Management Dashboard created: {out_file}")
