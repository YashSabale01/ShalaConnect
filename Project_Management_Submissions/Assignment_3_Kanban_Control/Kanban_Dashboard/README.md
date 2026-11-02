# ShalaConnect — Interactive Kanban & EVM Execution Dashboard

## Overview
This standalone, interactive web application provides a real-time project management dashboard customized for the **ShalaConnect** platform. Built in compliance with **PMI PMBOK Guide 7th Edition** and Agile Lean practices, it bridges tactical sprint execution with formal Earned Value Management (EVM) governance.

---

## Key Features

1. **5-Column Workflow**:
   - `Backlog`: All scope work packages awaiting initiation.
   - `To Do`: Sprint-ready items with cleared predecessors.
   - `In Progress`: Active software engineering with strict **WIP Limit: 3**.
   - `Testing / Review`: Quality gate and tenancy boundary testing with **WIP Limit: 3**.
   - `Done`: Fully validated deliverables deployed to AWS ECS Fargate.

2. **Drag-and-Drop Card Movement**:
   - Move cards across workflow stages with automatic status updates.
   - Dynamic visual warnings when WIP limits are exceeded.

3. **Dynamic Earned Value Management (EVM) Engine**:
   - **Planned Value (PV)**: Baseline target spending.
   - **Earned Value (EV)**: Value of work accomplished based on actual percentage completion.
   - **Actual Cost (AC)**: Direct expenditures consumed.
   - **Cost Variance (CV = EV - AC)** & **Schedule Variance (SV = EV - PV)**.
   - **Cost Performance Index (CPI = EV / AC)** & **Schedule Performance Index (SPI = EV / PV)**.
   - **Estimate At Completion (EAC = BAC / CPI)** & **Variance At Completion (VAC = BAC - EAC)**.
   - *Moving a card or adjusting completion percentage updates all EVM metrics instantly!*

4. **Lean Process Metrics**:
   - **Lead Time**: Time elapsed from customer request (Backlog) to delivery (Done).
   - **Cycle Time**: Time elapsed from active development (In Progress) to delivery (Done).
   - **Throughput**: Rate of completed work packages per week.
   - **Little's Law Validation**: $\text{WIP} = \text{Throughput} \times \text{Cycle Time}$.

5. **Persistence & Export**:
   - All state changes are automatically stored in browser `localStorage`.
   - Single-click **Reset Baseline** button to restore original WBS baseline.
   - **Export JSON** feature to back up task execution data.

---

## How to Run

1. Open `Source_Code/index.html` in any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Apple Safari).
2. No Node.js runtime, build step, or server installation is required.
3. Everything is client-side, self-contained, responsive, and works offline!
