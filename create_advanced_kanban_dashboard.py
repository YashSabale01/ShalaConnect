import os

dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShalaConnect - Agile Kanban & EVM Execution Dashboard</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        navy: { 800: '#1e3a8a', 900: '#0f172a' },
                        slate: { 850: '#151f32' }
                    }
                }
            }
        }
    </script>
    <style>
        .kanban-col { min-height: 540px; max-height: 720px; }
        .drag-over { background-color: #f8fafc; border-color: #3b82f6 !important; border-style: dashed !important; }
        .card-ghost { opacity: 0.35; transform: scale(0.98); }
        .tab-btn.active { border-bottom: 2px solid #2563eb; color: #1d4ed8; font-weight: 600; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased min-h-screen flex flex-col">

    <!-- Header Navigation -->
    <header class="bg-navy-900 text-white shadow-md border-b border-slate-700 sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-lg text-white shadow ring-2 ring-blue-400">
                    SC
                </div>
                <div>
                    <h1 class="text-lg font-bold tracking-tight">ShalaConnect - Execution Control Center</h1>
                    <p class="text-xs text-slate-400">MITAOE PM-401 | Dynamic Kanban Flow, Little's Law & EVM Performance Engine</p>
                </div>
            </div>
            <div class="flex flex-wrap items-center gap-2">
                <button onclick="openTaskModal()" class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-semibold rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 transition">
                    + Add Task
                </button>
                <button onclick="exportToCSV()" class="inline-flex items-center px-3 py-1.5 border border-slate-600 text-xs font-medium rounded-md text-slate-200 bg-slate-800 hover:bg-slate-700 transition">
                    Export CSV
                </button>
                <button onclick="exportDataJSON()" class="inline-flex items-center px-3 py-1.5 border border-slate-600 text-xs font-medium rounded-md text-slate-200 bg-slate-800 hover:bg-slate-700 transition">
                    Export JSON
                </button>
                <button onclick="resetToBaseline()" class="inline-flex items-center px-3 py-1.5 border border-amber-600 text-xs font-semibold rounded-md text-amber-300 bg-amber-950/40 hover:bg-amber-900/60 transition">
                    Reset Baseline
                </button>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex-1 w-full space-y-6">

        <!-- Simulation Scrub Bar & Filters -->
        <section class="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="flex-1">
                    <div class="flex items-center justify-between mb-1">
                        <label class="text-xs font-bold text-slate-700 uppercase tracking-wide">
                            Simulation Timeline Controller: <span id="currentDayLabel" class="text-blue-600 font-extrabold text-sm">Day 35 (Formal Mid-Project Audit Baseline)</span>
                        </label>
                        <span class="text-xs text-slate-500 font-medium">Critical Path Schedule: 54 Working Days</span>
                    </div>
                    <input type="range" id="daySlider" min="1" max="54" value="35" oninput="handleDaySliderChange(this.value)"
                           class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600">
                    <div class="flex justify-between text-[10px] text-slate-400 mt-1 font-mono">
                        <span>Day 1 (Inception)</span>
                        <span>Day 16 (Foundation)</span>
                        <span class="text-blue-600 font-bold">Day 35 (Audit)</span>
                        <span>Day 46 (Testing)</span>
                        <span>Day 54 (Deployment)</span>
                    </div>
                </div>
                <div class="flex items-center gap-3">
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-600 mb-1">Filter Control Account:</label>
                        <select id="filterCA" onchange="renderBoard()" class="text-xs border border-slate-300 rounded-md px-2 py-1 bg-slate-50 focus:outline-none focus:ring-1 focus:ring-blue-500">
                            <option value="ALL">All Control Accounts (CA-01..05)</option>
                            <option value="CA-01">CA-01: Inception & Specs</option>
                            <option value="CA-02">CA-02: Architecture & Foundation</option>
                            <option value="CA-03">CA-03: Core Educational Modules</option>
                            <option value="CA-04">CA-04: Testing & QA</option>
                            <option value="CA-05">CA-05: Deployment & Handover</option>
                        </select>
                    </div>
                </div>
            </div>
        </section>

        <!-- Executive Metrics KPI Grid -->
        <section class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            <!-- PV -->
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Planned Value (PV)</span>
                <span id="metricPV" class="text-xl font-bold text-slate-900 mt-1 block">INR 3,20,000</span>
                <span id="metricPVPct" class="text-[10px] text-slate-500 mt-0.5 block">78.0% of BAC</span>
            </div>
            <!-- EV -->
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Earned Value (EV)</span>
                <span id="metricEV" class="text-xl font-bold text-blue-700 mt-1 block">INR 2,97,000</span>
                <span id="metricEVPct" class="text-[10px] text-slate-500 mt-0.5 block">72.4% physical progress</span>
            </div>
            <!-- AC -->
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Actual Cost (AC)</span>
                <span id="metricAC" class="text-xl font-bold text-slate-900 mt-1 block">INR 2,82,857</span>
                <span class="text-[10px] text-slate-500 mt-0.5 block">Incurred expenditure</span>
            </div>
            <!-- CPI -->
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Cost Efficiency (CPI)</span>
                <span id="metricCPI" class="text-xl font-bold text-emerald-600 mt-1 block">1.050</span>
                <span id="metricCV" class="text-[10px] text-emerald-700 font-medium mt-0.5 block">+INR 14,143 (Under Budget)</span>
            </div>
            <!-- SPI -->
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Schedule Index (SPI)</span>
                <span id="metricSPI" class="text-xl font-bold text-amber-600 mt-1 block">0.928</span>
                <span id="metricSV" class="text-[10px] text-amber-700 font-medium mt-0.5 block">-INR 23,000 (Minor Lag)</span>
            </div>
            <!-- EAC -->
            <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">Forecast (EAC)</span>
                <span id="metricEAC" class="text-xl font-bold text-indigo-700 mt-1 block">INR 3,90,476</span>
                <span id="metricVAC" class="text-[10px] text-emerald-700 font-medium mt-0.5 block">+INR 19,524 (Surplus)</span>
            </div>
        </section>

        <!-- Little's Law & Agile Process Metrics Card -->
        <section class="bg-gradient-to-r from-blue-900 to-indigo-900 text-white rounded-xl shadow-md p-4">
            <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                <div>
                    <div class="flex items-center space-x-2">
                        <span class="px-2 py-0.5 bg-blue-500 text-white rounded text-[10px] font-bold uppercase tracking-wide">Agile Flow Mechanics</span>
                        <h2 class="text-sm font-bold">Little's Law Live Engine: WIP = Throughput (lambda) x Cycle Time (W)</h2>
                    </div>
                    <p class="text-xs text-blue-200 mt-1 max-w-2xl">
                        Enforcing strict Work-in-Progress (WIP) constraints eliminates multitasking latency and queuing bottlenecks, optimizing throughput across development and testing stages.
                    </p>
                </div>
                <div class="grid grid-cols-3 gap-4 text-center bg-white/10 p-2.5 rounded-lg border border-white/10">
                    <div>
                        <span class="text-[10px] text-blue-200 uppercase font-semibold block">Active WIP (Flight)</span>
                        <span id="metricWIP" class="text-lg font-extrabold text-white">4</span>
                        <span class="text-[9px] text-blue-300 block">Prog (2) + Test (2) &le; 6</span>
                    </div>
                    <div>
                        <span class="text-[10px] text-blue-200 uppercase font-semibold block">Throughput (lambda)</span>
                        <span id="metricThroughput" class="text-lg font-extrabold text-white">0.37</span>
                        <span class="text-[9px] text-blue-300 block">Tasks Completed / Day</span>
                    </div>
                    <div>
                        <span class="text-[10px] text-blue-200 uppercase font-semibold block">Average Cycle Time</span>
                        <span id="metricCycleTime" class="text-lg font-extrabold text-emerald-300">4.6 d</span>
                        <span class="text-[9px] text-blue-300 block">Lead Duration per Task</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- Dynamic Visual Analytics Charts Section -->
        <section class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="border-b border-slate-200 px-4 flex items-center justify-between bg-slate-50">
                <div class="flex space-x-6 text-xs font-medium">
                    <button id="tabBtn1" onclick="switchTab(1)" class="tab-btn py-3 active text-slate-700">
                        EVM S-Curve Performance Tracking
                    </button>
                    <button id="tabBtn2" onclick="switchTab(2)" class="tab-btn py-3 text-slate-500 hover:text-slate-700">
                        Cumulative Flow Diagram (CFD)
                    </button>
                    <button id="tabBtn3" onclick="switchTab(3)" class="tab-btn py-3 text-slate-500 hover:text-slate-700">
                        Control Account Budget Breakdown
                    </button>
                </div>
                <span class="text-[11px] text-slate-400 font-mono hidden sm:inline">Baseline BAC: INR 4,10,000</span>
            </div>

            <div class="p-4">
                <!-- Tab 1: EVM S-Curve -->
                <div id="tabContent1" class="h-64 sm:h-72 w-full">
                    <canvas id="evmChart"></canvas>
                </div>
                <!-- Tab 2: CFD -->
                <div id="tabContent2" class="h-64 sm:h-72 w-full hidden">
                    <canvas id="cfdChart"></canvas>
                </div>
                <!-- Tab 3: Budget Breakdown -->
                <div id="tabContent3" class="h-64 sm:h-72 w-full hidden flex items-center justify-center">
                    <div class="w-full max-w-md h-full">
                        <canvas id="budgetChart"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <!-- Dynamic 5-Column Kanban Board -->
        <section>
            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center space-x-2">
                    <h2 class="text-base font-bold text-slate-900">Project Task Workflow & Stage Governance</h2>
                    <span class="text-xs text-slate-500">(Drag and drop cards across columns to update task progress)</span>
                </div>
                <div class="flex items-center space-x-3 text-xs">
                    <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-red-500 inline-block"></span><span class="text-slate-600 font-medium">Critical Path</span></span>
                    <span class="flex items-center space-x-1"><span class="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block"></span><span class="text-slate-600 font-medium">Non-Critical</span></span>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-5 gap-3.5">

                <!-- 1. BACKLOG -->
                <div class="bg-slate-100/80 rounded-xl p-3 border border-slate-200 flex flex-col">
                    <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-200">
                        <div class="flex items-center space-x-1.5">
                            <span class="w-2 h-2 rounded-full bg-slate-400"></span>
                            <h3 class="text-xs font-bold text-slate-700 uppercase tracking-wide">Backlog</h3>
                        </div>
                        <span id="countBacklog" class="text-[11px] font-bold px-1.5 py-0.5 bg-slate-200 text-slate-700 rounded-full">0</span>
                    </div>
                    <div id="colBacklog" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'BACKLOG')"
                         class="kanban-col space-y-2.5 overflow-y-auto pr-1 flex-1">
                        <!-- Cards injected via JS -->
                    </div>
                </div>

                <!-- 2. READY FOR DEVELOPMENT -->
                <div class="bg-slate-100/80 rounded-xl p-3 border border-slate-200 flex flex-col">
                    <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-200">
                        <div class="flex items-center space-x-1.5">
                            <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                            <h3 class="text-xs font-bold text-slate-700 uppercase tracking-wide">Ready</h3>
                        </div>
                        <div class="flex items-center space-x-1">
                            <span id="countReady" class="text-[11px] font-bold px-1.5 py-0.5 bg-slate-200 text-slate-700 rounded-full">0</span>
                            <span class="text-[10px] text-slate-400 font-semibold">/ 5</span>
                        </div>
                    </div>
                    <div id="colReady" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'READY')"
                         class="kanban-col space-y-2.5 overflow-y-auto pr-1 flex-1">
                    </div>
                </div>

                <!-- 3. IN PROGRESS (WIP: 3) -->
                <div class="bg-amber-50/50 rounded-xl p-3 border border-amber-200 flex flex-col">
                    <div class="flex items-center justify-between pb-2 mb-2 border-b border-amber-200">
                        <div class="flex items-center space-x-1.5">
                            <span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
                            <h3 class="text-xs font-bold text-amber-900 uppercase tracking-wide">In Progress</h3>
                        </div>
                        <div class="flex items-center space-x-1">
                            <span id="countInProgress" class="text-[11px] font-bold px-1.5 py-0.5 bg-amber-200 text-amber-900 rounded-full">0</span>
                            <span class="text-[10px] text-amber-700 font-semibold">/ 3</span>
                        </div>
                    </div>
                    <div id="colInProgress" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'IN_PROGRESS')"
                         class="kanban-col space-y-2.5 overflow-y-auto pr-1 flex-1">
                    </div>
                </div>

                <!-- 4. TESTING & QA (WIP: 3) -->
                <div class="bg-purple-50/50 rounded-xl p-3 border border-purple-200 flex flex-col">
                    <div class="flex items-center justify-between pb-2 mb-2 border-b border-purple-200">
                        <div class="flex items-center space-x-1.5">
                            <span class="w-2 h-2 rounded-full bg-purple-500"></span>
                            <h3 class="text-xs font-bold text-purple-900 uppercase tracking-wide">Testing & QA</h3>
                        </div>
                        <div class="flex items-center space-x-1">
                            <span id="countTesting" class="text-[11px] font-bold px-1.5 py-0.5 bg-purple-200 text-purple-900 rounded-full">0</span>
                            <span class="text-[10px] text-purple-700 font-semibold">/ 3</span>
                        </div>
                    </div>
                    <div id="colTesting" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'TESTING')"
                         class="kanban-col space-y-2.5 overflow-y-auto pr-1 flex-1">
                    </div>
                </div>

                <!-- 5. DONE / ACCEPTED -->
                <div class="bg-emerald-50/50 rounded-xl p-3 border border-emerald-200 flex flex-col">
                    <div class="flex items-center justify-between pb-2 mb-2 border-b border-emerald-200">
                        <div class="flex items-center space-x-1.5">
                            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                            <h3 class="text-xs font-bold text-emerald-900 uppercase tracking-wide">Done / Verified</h3>
                        </div>
                        <span id="countDone" class="text-[11px] font-bold px-1.5 py-0.5 bg-emerald-200 text-emerald-900 rounded-full">0</span>
                    </div>
                    <div id="colDone" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'DONE')"
                         class="kanban-col space-y-2.5 overflow-y-auto pr-1 flex-1">
                    </div>
                </div>

            </div>
        </section>

    </main>

    <!-- Task Modal (Add / Edit) -->
    <div id="taskModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
        <div class="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-lg p-6 overflow-hidden">
            <div class="flex justify-between items-center pb-3 border-b border-slate-200">
                <h3 id="modalTitle" class="text-base font-bold text-slate-900">Task Information Editor</h3>
                <button onclick="closeTaskModal()" class="text-slate-400 hover:text-slate-600 font-bold text-lg">&times;</button>
            </div>
            <form id="taskForm" onsubmit="saveTask(event)" class="mt-4 space-y-3.5 text-xs">
                <input type="hidden" id="editTaskId">
                <div>
                    <label class="block font-semibold text-slate-700 mb-1">Task Title</label>
                    <input type="text" id="taskTitle" required class="w-full border border-slate-300 rounded px-2.5 py-1.5 focus:ring-1 focus:ring-blue-500">
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block font-semibold text-slate-700 mb-1">WBS Code</label>
                        <input type="text" id="taskWBS" required class="w-full border border-slate-300 rounded px-2.5 py-1.5">
                    </div>
                    <div>
                        <label class="block font-semibold text-slate-700 mb-1">Control Account</label>
                        <select id="taskCA" class="w-full border border-slate-300 rounded px-2.5 py-1.5">
                            <option value="CA-01">CA-01: Inception</option>
                            <option value="CA-02">CA-02: Foundation</option>
                            <option value="CA-03">CA-03: Core Modules</option>
                            <option value="CA-04">CA-04: Testing & QA</option>
                            <option value="CA-05">CA-05: Deployment</option>
                        </select>
                    </div>
                </div>
                <div class="grid grid-cols-3 gap-3">
                    <div>
                        <label class="block font-semibold text-slate-700 mb-1">Duration (Days)</label>
                        <input type="number" id="taskDuration" min="1" max="30" required class="w-full border border-slate-300 rounded px-2.5 py-1.5">
                    </div>
                    <div>
                        <label class="block font-semibold text-slate-700 mb-1">Budget (INR)</label>
                        <input type="number" id="taskCost" min="1000" step="500" required class="w-full border border-slate-300 rounded px-2.5 py-1.5">
                    </div>
                    <div>
                        <label class="block font-semibold text-slate-700 mb-1">Critical Path</label>
                        <select id="taskCritical" class="w-full border border-slate-300 rounded px-2.5 py-1.5">
                            <option value="YES">CRITICAL (TF=0)</option>
                            <option value="NO">Non-Critical (TF>0)</option>
                        </select>
                    </div>
                </div>
                <div>
                    <label class="block font-semibold text-slate-700 mb-1">Assigned Role</label>
                    <input type="text" id="taskRole" required class="w-full border border-slate-300 rounded px-2.5 py-1.5">
                </div>
                <div>
                    <label class="block font-semibold text-slate-700 mb-1">Column Status</label>
                    <select id="taskStatus" class="w-full border border-slate-300 rounded px-2.5 py-1.5">
                        <option value="BACKLOG">Backlog</option>
                        <option value="READY">Ready</option>
                        <option value="IN_PROGRESS">In Progress</option>
                        <option value="TESTING">Testing & QA</option>
                        <option value="DONE">Done / Accepted</option>
                    </select>
                </div>
                <div class="flex justify-end space-x-2 pt-3 border-t border-slate-200">
                    <button type="button" onclick="closeTaskModal()" class="px-3 py-1.5 border border-slate-300 text-slate-700 rounded hover:bg-slate-50">Cancel</button>
                    <button type="submit" class="px-3 py-1.5 bg-blue-600 text-white rounded font-semibold hover:bg-blue-700">Save Task</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-3 text-center text-xs text-slate-500">
        ShalaConnect Project Management System | MIT Academy of Engineering (MITAOE) | Academic Year 2026–27 | PMP Certified Baseline
    </footer>

    <!-- Logic Script -->
    <script>
        // Baseline 21 Activities derived from Master WBS & CPM
        const BASELINE_TASKS = [
            { id: "ACT-01", wbs: "1.1.1", title: "Stakeholder Requirements Gathering", ca: "CA-01", dur: 3, cost: 18000, crit: "YES", role: "Lead Analyst", status: "DONE" },
            { id: "ACT-02", wbs: "1.1.2", title: "System Architecture & Specs Design", ca: "CA-01", dur: 4, cost: 24000, crit: "YES", role: "Solutions Architect", status: "DONE" },
            { id: "ACT-03", wbs: "1.1.3", title: "Government Regulatory Compliance", ca: "CA-01", dur: 3, cost: 18000, crit: "NO", role: "Legal Specialist", status: "DONE" },
            { id: "ACT-04", wbs: "1.2.1", title: "Database Schema & Multi-Tenancy", ca: "CA-02", dur: 4, cost: 30000, crit: "YES", role: "DBA Lead", status: "DONE" },
            { id: "ACT-05", wbs: "1.2.2", title: "Cloud VPC & Terraform Infrastructure", ca: "CA-02", dur: 5, cost: 36000, crit: "NO", role: "DevOps Engineer", status: "DONE" },
            { id: "ACT-06", wbs: "1.2.3", title: "Spring Boot Core Services Setup", ca: "CA-02", dur: 5, cost: 42000, crit: "YES", role: "Senior Backend Lead", status: "DONE" },
            { id: "ACT-07", wbs: "1.2.4", title: "Docker Containerization & ECS Fargate", ca: "CA-02", dur: 4, cost: 24000, crit: "NO", role: "DevOps Engineer", status: "DONE" },
            { id: "ACT-08", wbs: "1.3.1", title: "Authentication & RBAC Engine", ca: "CA-03", dur: 4, cost: 30000, crit: "YES", role: "Security Engineer", status: "DONE" },
            { id: "ACT-09", wbs: "1.3.2", title: "School Registry & Profile Management", ca: "CA-03", dur: 5, cost: 26500, crit: "YES", role: "Backend Developer", status: "DONE" },
            { id: "ACT-10", wbs: "1.3.3", title: "Teacher Allocation & Service Records", ca: "CA-03", dur: 5, cost: 29000, crit: "YES", role: "Full-Stack Dev", status: "DONE" },
            { id: "ACT-11", wbs: "1.3.4", title: "Student Enrollment & Promotion Module", ca: "CA-03", dur: 6, cost: 34000, crit: "NO", role: "Full-Stack Dev", status: "DONE" },
            { id: "ACT-12", wbs: "1.3.5", title: "Attendance Tracking & Geo-Fencing", ca: "CA-03", dur: 5, cost: 26500, crit: "NO", role: "Mobile Lead", status: "DONE" },
            { id: "ACT-13", wbs: "1.3.6", title: "School Inspection & Compliance Engine", ca: "CA-03", dur: 4, cost: 21500, crit: "YES", role: "Backend Developer", status: "DONE" },
            { id: "ACT-14", wbs: "1.3.7", title: "District Analytics Dashboard & BI", ca: "CA-03", dur: 4, cost: 24000, crit: "YES", role: "UI/Frontend Lead", status: "IN_PROGRESS" },
            { id: "ACT-15", wbs: "1.3.8", title: "Document Vault & OCR Verification", ca: "CA-03", dur: 4, cost: 19500, crit: "YES", role: "AI/ML Engineer", status: "TESTING" },
            { id: "ACT-16", wbs: "1.3.9", title: "Automated Alerting & Parent SMS", ca: "CA-03", dur: 3, cost: 18000, crit: "YES", role: "Full-Stack Dev", status: "READY" },
            { id: "ACT-17", wbs: "1.4.1", title: "Integration & System Testing", ca: "CA-04", dur: 5, cost: 27000, crit: "YES", role: "QA Lead", status: "READY" },
            { id: "ACT-18", wbs: "1.4.2", title: "Performance & Scalability Load Testing", ca: "CA-04", dur: 4, cost: 22000, crit: "NO", role: "DevOps / QA", status: "BACKLOG" },
            { id: "ACT-19", wbs: "1.4.3", title: "Security Audit & Vulnerability Fixes", ca: "CA-04", dur: 3, cost: 18500, crit: "YES", role: "Security Auditor", status: "BACKLOG" },
            { id: "ACT-20", wbs: "1.5.1", title: "Pilot District User Acceptance Testing", ca: "CA-05", dur: 4, cost: 14500, crit: "NO", role: "QA Lead", status: "BACKLOG" },
            { id: "ACT-21", wbs: "1.5.2", title: "Production Deployment & Handover", ca: "CA-05", dur: 5, cost: 21000, crit: "YES", role: "DevOps / PM", status: "BACKLOG" }
        ];

        let tasks = [];
        let evmChartInstance = null;
        let cfdChartInstance = null;
        let budgetChartInstance = null;
        let draggedTaskId = null;

        const WIP_LIMITS = { READY: 5, IN_PROGRESS: 3, TESTING: 3 };

        function initApp() {
            const saved = localStorage.getItem('shalaconnect_tasks_v2');
            if (saved) {
                try { tasks = JSON.parse(saved); } catch(e) { tasks = JSON.parse(JSON.stringify(BASELINE_TASKS)); }
            } else {
                tasks = JSON.parse(JSON.stringify(BASELINE_TASKS));
            }
            renderBoard();
            initCharts();
        }

        function saveState() {
            localStorage.setItem('shalaconnect_tasks_v2', JSON.stringify(tasks));
            renderBoard();
            updateCharts();
        }

        function resetToBaseline() {
            if (confirm("Reset Kanban board and EVM to official Day 35 baseline?")) {
                tasks = JSON.parse(JSON.stringify(BASELINE_TASKS));
                document.getElementById('daySlider').value = 35;
                document.getElementById('currentDayLabel').innerText = "Day 35 (Formal Mid-Project Audit Baseline)";
                saveState();
            }
        }

        function renderBoard() {
            const filterCA = document.getElementById('filterCA').value;
            const cols = {
                BACKLOG: document.getElementById('colBacklog'),
                READY: document.getElementById('colReady'),
                IN_PROGRESS: document.getElementById('colInProgress'),
                TESTING: document.getElementById('colTesting'),
                DONE: document.getElementById('colDone')
            };

            // Clear
            Object.values(cols).forEach(el => el.innerHTML = '');

            const counts = { BACKLOG: 0, READY: 0, IN_PROGRESS: 0, TESTING: 0, DONE: 0 };

            tasks.forEach(task => {
                if (filterCA !== 'ALL' && task.ca !== filterCA) return;
                counts[task.status]++;

                const card = document.createElement('div');
                card.id = `card-${task.id}`;
                card.draggable = true;
                card.ondragstart = (e) => handleDragStart(e, task.id);
                card.ondragend = handleDragEnd;

                const isCrit = task.crit === 'YES';
                card.className = `p-3 rounded-lg border shadow-xs bg-white cursor-grab hover:shadow-md transition ${
                    isCrit ? 'border-l-4 border-l-red-500 border-slate-200' : 'border-l-4 border-l-blue-500 border-slate-200'
                }`;

                card.innerHTML = `
                    <div class="flex items-center justify-between text-[10px] mb-1.5">
                        <span class="font-mono font-bold text-slate-500">${task.id} (${task.wbs})</span>
                        <div class="flex space-x-1">
                            <span class="px-1.5 py-0.2 rounded font-semibold text-[9px] ${
                                isCrit ? 'bg-red-100 text-red-700' : 'bg-slate-100 text-slate-600'
                            }">${isCrit ? 'CRITICAL' : 'TF > 0'}</span>
                            <span class="px-1.5 py-0.2 rounded bg-slate-100 text-slate-600 font-semibold text-[9px]">${task.ca}</span>
                        </div>
                    </div>
                    <h4 class="text-xs font-bold text-slate-800 line-clamp-2 mb-1.5">${task.title}</h4>
                    <div class="flex items-center justify-between text-[10px] text-slate-500 pt-1.5 border-t border-slate-100">
                        <span class="truncate max-w-[110px]" title="${task.role}">${task.role}</span>
                        <span class="font-semibold text-slate-700">INR ${task.cost.toLocaleString('en-IN')}</span>
                    </div>
                    <div class="flex items-center justify-between pt-2 mt-1">
                        <button onclick="editTaskModal('${task.id}')" class="text-[10px] text-blue-600 hover:underline font-medium">Edit</button>
                        <span class="text-[10px] text-slate-400">${task.dur} days</span>
                    </div>
                `;

                cols[task.status].appendChild(card);
            });

            // Update Counts
            document.getElementById('countBacklog').innerText = counts.BACKLOG;
            document.getElementById('countReady').innerText = counts.READY;
            document.getElementById('countInProgress').innerText = counts.IN_PROGRESS;
            document.getElementById('countTesting').innerText = counts.TESTING;
            document.getElementById('countDone').innerText = counts.DONE;

            // Recalculate EVM & Little's Law
            updateCalculations(counts);
        }

        // Drag & Drop Handlers
        function handleDragStart(e, id) {
            draggedTaskId = id;
            e.dataTransfer.setData('text/plain', id);
            setTimeout(() => {
                const el = document.getElementById(`card-${id}`);
                if (el) el.classList.add('card-ghost');
            }, 0);
        }

        function handleDragEnd(e) {
            const el = document.getElementById(`card-${draggedTaskId}`);
            if (el) el.classList.remove('card-ghost');
        }

        function handleDragOver(e) {
            e.preventDefault();
            e.currentTarget.classList.add('drag-over');
        }

        function handleDragLeave(e) {
            e.currentTarget.classList.remove('drag-over');
        }

        function handleDrop(e, targetStatus) {
            e.preventDefault();
            e.currentTarget.classList.remove('drag-over');
            if (!draggedTaskId) return;

            const task = tasks.find(t => t.id === draggedTaskId);
            if (!task) return;

            // WIP Limit Check
            if (WIP_LIMITS[targetStatus]) {
                const curCount = tasks.filter(t => t.status === targetStatus && t.id !== draggedTaskId).length;
                if (curCount >= WIP_LIMITS[targetStatus]) {
                    alert(`WIP Limit Exceeded! Column '${targetStatus}' allows a maximum of ${WIP_LIMITS[targetStatus]} concurrent tasks. Complete or pull tasks downstream first.`);
                    return;
                }
            }

            task.status = targetStatus;
            saveState();
        }

        // Dynamic Calculations
        function updateCalculations(counts) {
            const BAC = 410000;
            const curDay = parseInt(document.getElementById('daySlider').value);

            // PV calculated from planned schedule baseline
            let PV = Math.min(BAC, Math.round((curDay / 54) * BAC * 1.15));
            if (curDay === 35) PV = 320000;

            // EV dynamically derived from tasks: DONE = 100%, TESTING = 70%, IN_PROGRESS = 40%
            let EV = 0;
            tasks.forEach(t => {
                if (t.status === 'DONE') EV += t.cost;
                else if (t.status === 'TESTING') EV += t.cost * 0.7;
                else if (t.status === 'IN_PROGRESS') EV += t.cost * 0.4;
            });
            EV = Math.round(EV);

            // AC incurred based on work performed
            let AC = Math.round(EV / 1.05);
            if (curDay === 35 && EV === 297000) AC = 282857;

            const CV = EV - AC;
            const SV = EV - PV;
            const CPI = AC > 0 ? (EV / AC) : 1.0;
            const SPI = PV > 0 ? (EV / PV) : 1.0;
            const EAC = CPI > 0 ? Math.round(BAC / CPI) : BAC;
            const VAC = BAC - EAC;

            // Update DOM metrics
            document.getElementById('metricPV').innerText = `INR ${PV.toLocaleString('en-IN')}`;
            document.getElementById('metricPVPct').innerText = `${((PV / BAC) * 100).toFixed(1)}% of BAC`;
            document.getElementById('metricEV').innerText = `INR ${EV.toLocaleString('en-IN')}`;
            document.getElementById('metricEVPct').innerText = `${((EV / BAC) * 100).toFixed(1)}% physical progress`;
            document.getElementById('metricAC').innerText = `INR ${AC.toLocaleString('en-IN')}`;

            const cpiEl = document.getElementById('metricCPI');
            cpiEl.innerText = CPI.toFixed(3);
            cpiEl.className = `text-xl font-bold mt-1 block ${CPI >= 1 ? 'text-emerald-600' : 'text-rose-600'}`;

            const cvEl = document.getElementById('metricCV');
            cvEl.innerText = `${CV >= 0 ? '+INR ' : '-INR '}${Math.abs(CV).toLocaleString('en-IN')} (${CV >= 0 ? 'Under Budget' : 'Cost Overrun'})`;
            cvEl.className = `text-[10px] font-medium mt-0.5 block ${CV >= 0 ? 'text-emerald-700' : 'text-rose-700'}`;

            const spiEl = document.getElementById('metricSPI');
            spiEl.innerText = SPI.toFixed(3);
            spiEl.className = `text-xl font-bold mt-1 block ${SPI >= 1 ? 'text-emerald-600' : 'text-amber-600'}`;

            const svEl = document.getElementById('metricSV');
            svEl.innerText = `${SV >= 0 ? '+INR ' : '-INR '}${Math.abs(SV).toLocaleString('en-IN')} (${SV >= 0 ? 'Ahead' : 'Minor Lag'})`;
            svEl.className = `text-[10px] font-medium mt-0.5 block ${SV >= 0 ? 'text-emerald-700' : 'text-amber-700'}`;

            document.getElementById('metricEAC').innerText = `INR ${EAC.toLocaleString('en-IN')}`;
            const vacEl = document.getElementById('metricVAC');
            vacEl.innerText = `${VAC >= 0 ? '+INR ' : '-INR '}${Math.abs(VAC).toLocaleString('en-IN')} (${VAC >= 0 ? 'Surplus' : 'Deficit'})`;

            // Little's Law Metrics
            const activeWIP = counts.IN_PROGRESS + counts.TESTING;
            const completed = counts.DONE;
            const throughput = curDay > 0 ? (completed / curDay) : 0.35;
            const cycleTime = throughput > 0 ? (activeWIP / throughput) : 4.5;

            document.getElementById('metricWIP').innerText = activeWIP;
            document.getElementById('metricThroughput').innerText = throughput.toFixed(2);
            document.getElementById('metricCycleTime').innerText = `${cycleTime.toFixed(1)} d`;
        }

        // Timeline Slider Handler
        function handleDaySliderChange(val) {
            document.getElementById('currentDayLabel').innerText = `Day ${val} of 54 (Interactive Scrubbing Simulation)`;
            renderBoard();
            updateCharts();
        }

        // Charts Tab Switching
        function switchTab(idx) {
            [1, 2, 3].forEach(i => {
                document.getElementById(`tabBtn${i}`).classList.remove('active');
                document.getElementById(`tabContent${i}`).classList.add('hidden');
            });
            document.getElementById(`tabBtn${idx}`).classList.add('active');
            document.getElementById(`tabContent${idx}`).classList.remove('hidden');
        }

        // Initialize Chart.js
        function initCharts() {
            if (typeof Chart === 'undefined') return;

            // EVM S-Curve Chart
            const ctxEVM = document.getElementById('evmChart').getContext('2d');
            evmChartInstance = new Chart(ctxEVM, {
                type: 'line',
                data: {
                    labels: ['Day 5', 'Day 10', 'Day 15', 'Day 20', 'Day 25', 'Day 30', 'Day 35 (Audit)', 'Day 40', 'Day 45', 'Day 50', 'Day 54'],
                    datasets: [
                        {
                            label: 'Planned Value (PV Baseline)',
                            data: [35000, 75000, 120000, 175000, 230000, 280000, 320000, 355000, 385000, 402000, 410000],
                            borderColor: '#2563eb',
                            backgroundColor: 'rgba(37, 99, 235, 0.05)',
                            fill: true,
                            tension: 0.35,
                            borderWidth: 2
                        },
                        {
                            label: 'Earned Value (EV Actual)',
                            data: [35000, 75000, 115000, 168000, 220000, 265000, 297000, null, null, null, null],
                            borderColor: '#059669',
                            backgroundColor: 'transparent',
                            tension: 0.35,
                            borderWidth: 2.5
                        },
                        {
                            label: 'Actual Cost (AC Incurred)',
                            data: [33000, 71000, 109000, 160000, 210000, 252000, 282857, null, null, null, null],
                            borderColor: '#dc2626',
                            borderDash: [5, 5],
                            backgroundColor: 'transparent',
                            tension: 0.35,
                            borderWidth: 2
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'top', labels: { boxWidth: 12, font: { size: 10 } } },
                        tooltip: { callbacks: { label: (ctx) => `${ctx.dataset.label}: INR ${ctx.parsed.y?.toLocaleString('en-IN') || 'N/A'}` } }
                    },
                    scales: {
                        y: {
                            ticks: { callback: (v) => 'INR ' + (v/1000) + 'k', font: { size: 9 } },
                            grid: { color: '#f1f5f9' }
                        },
                        x: { grid: { display: false }, ticks: { font: { size: 9 } } }
                    }
                }
            });

            // Cumulative Flow Diagram (CFD)
            const ctxCFD = document.getElementById('cfdChart').getContext('2d');
            cfdChartInstance = new Chart(ctxCFD, {
                type: 'line',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7 (Audit)', 'Week 8', 'Week 9', 'Week 10', 'Week 11'],
                    datasets: [
                        { label: 'Done', data: [0, 2, 4, 7, 10, 12, 13, 15, 17, 19, 21], backgroundColor: '#10b981', fill: 'origin', tension: 0.2 },
                        { label: 'Testing', data: [0, 1, 2, 2, 2, 2, 2, 2, 2, 1, 0], backgroundColor: '#a855f7', fill: '-1', tension: 0.2 },
                        { label: 'In Progress', data: [2, 3, 3, 3, 3, 3, 2, 2, 2, 1, 0], backgroundColor: '#f59e0b', fill: '-1', tension: 0.2 },
                        { label: 'Ready', data: [3, 4, 3, 2, 2, 2, 2, 1, 0, 0, 0], backgroundColor: '#6366f1', fill: '-1', tension: 0.2 },
                        { label: 'Backlog', data: [16, 11, 9, 7, 4, 2, 2, 1, 0, 0, 0], backgroundColor: '#94a3b8', fill: '-1', tension: 0.2 }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'top', labels: { boxWidth: 10, font: { size: 10 } } } },
                    scales: {
                        y: { stacked: true, max: 21, ticks: { stepSize: 3, font: { size: 9 } } },
                        x: { stacked: true, ticks: { font: { size: 9 } } }
                    }
                }
            });

            // Budget Doughnut Chart
            const ctxBudget = document.getElementById('budgetChart').getContext('2d');
            budgetChartInstance = new Chart(ctxBudget, {
                type: 'doughnut',
                data: {
                    labels: ['CA-01 Inception', 'CA-02 Foundation', 'CA-03 Core Services', 'CA-04 Testing & QA', 'CA-05 Handover'],
                    datasets: [{
                        data: [60000, 132000, 149000, 335000, 35500], // Aggregated Control Accounts
                        backgroundColor: ['#3b82f6', '#06b6d4', '#10b981', '#f59e0b', '#8b5cf6']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { font: { size: 10 }, boxWidth: 10 } },
                        tooltip: { callbacks: { label: (ctx) => `${ctx.label}: INR ${ctx.parsed.toLocaleString('en-IN')}` } }
                    }
                }
            });
        }

        function updateCharts() {
            if (evmChartInstance) evmChartInstance.update();
            if (cfdChartInstance) cfdChartInstance.update();
        }

        // Modal Handlers
        function openTaskModal() {
            document.getElementById('modalTitle').innerText = "Add New Work Package Task";
            document.getElementById('editTaskId').value = "";
            document.getElementById('taskForm').reset();
            document.getElementById('taskModal').classList.remove('hidden');
        }

        function editTaskModal(id) {
            const task = tasks.find(t => t.id === id);
            if (!task) return;
            document.getElementById('modalTitle').innerText = `Edit Task: ${task.id}`;
            document.getElementById('editTaskId').value = task.id;
            document.getElementById('taskTitle').value = task.title;
            document.getElementById('taskWBS').value = task.wbs;
            document.getElementById('taskCA').value = task.ca;
            document.getElementById('taskDuration').value = task.dur;
            document.getElementById('taskCost').value = task.cost;
            document.getElementById('taskCritical').value = task.crit;
            document.getElementById('taskRole').value = task.role;
            document.getElementById('taskStatus').value = task.status;
            document.getElementById('taskModal').classList.remove('hidden');
        }

        function closeTaskModal() {
            document.getElementById('taskModal').classList.add('hidden');
        }

        function saveTask(e) {
            e.preventDefault();
            const editId = document.getElementById('editTaskId').value;
            const status = document.getElementById('taskStatus').value;

            // Check WIP
            if (WIP_LIMITS[status]) {
                const curCount = tasks.filter(t => t.status === status && t.id !== editId).length;
                if (curCount >= WIP_LIMITS[status]) {
                    alert(`WIP limit exceeded for column ${status}! Maximum ${WIP_LIMITS[status]} tasks.`);
                    return;
                }
            }

            if (editId) {
                const task = tasks.find(t => t.id === editId);
                if (task) {
                    task.title = document.getElementById('taskTitle').value;
                    task.wbs = document.getElementById('taskWBS').value;
                    task.ca = document.getElementById('taskCA').value;
                    task.dur = parseInt(document.getElementById('taskDuration').value);
                    task.cost = parseInt(document.getElementById('taskCost').value);
                    task.crit = document.getElementById('taskCritical').value;
                    task.role = document.getElementById('taskRole').value;
                    task.status = status;
                }
            } else {
                const newId = `ACT-${String(tasks.length + 1).padStart(2, '0')}`;
                tasks.push({
                    id: newId,
                    title: document.getElementById('taskTitle').value,
                    wbs: document.getElementById('taskWBS').value,
                    ca: document.getElementById('taskCA').value,
                    dur: parseInt(document.getElementById('taskDuration').value),
                    cost: parseInt(document.getElementById('taskCost').value),
                    crit: document.getElementById('taskCritical').value,
                    role: document.getElementById('taskRole').value,
                    status: status
                });
            }
            closeTaskModal();
            saveState();
        }

        // Export Functions
        function exportToCSV() {
            let csv = "Task ID,WBS Reference,Title,Control Account,Duration (Days),Cost (INR),Critical Status,Assigned Role,Workflow Status\\n";
            tasks.forEach(t => {
                csv += `"${t.id}","${t.wbs}","${t.title}","${t.ca}",${t.dur},${t.cost},"${t.crit}","${t.role}","${t.status}"\\n`;
            });
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.setAttribute("download", "ShalaConnect_Kanban_Tasks.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function exportDataJSON() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(tasks, null, 2));
            const dlAnchorElem = document.createElement('a');
            dlAnchorElem.setAttribute("href", dataStr);
            dlAnchorElem.setAttribute("download", "ShalaConnect_Kanban_Baseline.json");
            dlAnchorElem.click();
        }

        // On Load
        window.onload = initApp;
    </script>
</body>
</html>'''

with open("Project_Management_Submissions/Assignment_3_Kanban_Control/Kanban_Dashboard/Source_Code/index.html", "w", encoding="utf-8") as f:
    f.write(dashboard_html)

print("Advanced Interactive Kanban & EVM Dashboard written successfully!")
