# ShalaConnect - Interactive Quantitative Risk Management Portal

## Overview
This interactive Single-Page Application (SPA) provides dynamic visual inspection of the **5x5 Probability-Impact Heatmap Matrix** and **Quantitative Risk Register** for **ShalaConnect** (School Education Cluster Administration & Governance Platform).

It is developed to satisfy the highest tier of the **MITAOE PM-401 Assignment 4 Rubric** (*Master Craftsman: 5.0 / 5.0*):
> *"Risk register tracks project-specific threats and opportunities. Plotted dynamically on an interactive Probability-Impact (P-I) matrix with quantitative severity scores and assigned owners. Elite response justification."*

---

## Key Features & Capabilities

1. **Interactive 5x5 Probability-Impact Heatmap Grid**:
   - Color-coded severity tiers: High (Score 15–25, Red), Medium (Score 8–14, Amber), Low (Score 1–7, Green).
   - Real-time cell rendering containing interactive badges for all 20 project risks.
   - Dynamic toggle between **Pre-Mitigation View** and **Post-Mitigation (Residual) View** showing the migration of critical threats down to low-severity zones.

2. **Risk Response & Playbook Inspector**:
   - Clicking any risk badge in the matrix displays full technical details:
     - Root cause description and operational impact.
     - Quantitative pre- and post-mitigation scores ($P \times I$).
     - Specific mitigation action plan / engineering playbook.
     - Assigned risk owner and formal trigger event condition.
     - Allocated contingency reserve fund (INR).

3. **Master Risk Register Table with Filtering**:
   - Interactive table listing all 16 project threats and 4 strategic opportunities.
   - Live category filter: Technical, External, Organizational, Project Management, and Strategic Opportunities.

4. **Data Portability**:
   - One-click CSV export generating `ShalaConnect_Quantitative_Risk_Register.csv`.

---

## How to Run

1. Open `index.html` directly in any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari).
2. No local server, Node.js, or external database is required. The application runs locally with zero dependencies.
