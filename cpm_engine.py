import networkx as nx

# Define the 21 activities directly derived from Assignment 1 WBS
activities = {
    "ACT-01": {"name": "Stakeholder Needs & Surveys", "wbs": "1.1.1", "dur": 3, "cost": 14000, "preds": []},
    "ACT-02": {"name": "SRS & Requirements Matrix", "wbs": "1.1.2", "dur": 4, "cost": 16000, "preds": ["ACT-01"]},
    "ACT-03": {"name": "DPDP Act Compliance", "wbs": "1.1.3", "dur": 3, "cost": 12000, "preds": ["ACT-02"]},
    "ACT-04": {"name": "Multi-Tenant Data Modeling", "wbs": "1.2.1", "dur": 4, "cost": 20000, "preds": ["ACT-02", "ACT-03"]},
    "ACT-05": {"name": "REST API Specs (OpenAPI)", "wbs": "1.2.2", "dur": 4, "cost": 18000, "preds": ["ACT-04"]},
    "ACT-06": {"name": "Bilingual UI/UX & Prototypes", "wbs": "1.2.3", "dur": 5, "cost": 22000, "preds": ["ACT-02"]},
    "ACT-07": {"name": "AWS Cloud Blueprint", "wbs": "1.2.4", "dur": 4, "cost": 18000, "preds": ["ACT-04", "ACT-05"]},
    "ACT-08": {"name": "Multi-Tenant RBAC & Security", "wbs": "1.3.1", "dur": 5, "cost": 22000, "preds": ["ACT-05"]},
    "ACT-09": {"name": "Attendance Engine & Offline Sync", "wbs": "1.3.2", "dur": 7, "cost": 32000, "preds": ["ACT-06", "ACT-08"]},
    "ACT-10": {"name": "BEO Monthly Excel Report Engine", "wbs": "1.3.3", "dur": 5, "cost": 24000, "preds": ["ACT-09"]},
    "ACT-11": {"name": "GR Circulars & Read Receipts", "wbs": "1.3.4", "dur": 4, "cost": 18000, "preds": ["ACT-08"]},
    "ACT-12": {"name": "Cluster Meeting Scheduler", "wbs": "1.3.5", "dur": 3, "cost": 16000, "preds": ["ACT-08"]},
    "ACT-13": {"name": "Events & Multi-Photo Gallery", "wbs": "1.3.6", "dur": 4, "cost": 20000, "preds": ["ACT-06", "ACT-08"]},
    "ACT-14": {"name": "Dynamic Form Builder & Engine", "wbs": "1.3.7", "dur": 6, "cost": 26000, "preds": ["ACT-08", "ACT-10"]},
    "ACT-15": {"name": "Public Transparency Portal", "wbs": "1.3.8", "dur": 4, "cost": 18000, "preds": ["ACT-05", "ACT-06"]},
    "ACT-16": {"name": "Modular Terraform Provisioning", "wbs": "1.4.1", "dur": 5, "cost": 28000, "preds": ["ACT-07"]},
    "ACT-17": {"name": "GitHub Actions CI/CD", "wbs": "1.4.2", "dur": 4, "cost": 22000, "preds": ["ACT-16"]},
    "ACT-18": {"name": "Performance Tuning & Audit", "wbs": "1.4.3", "dur": 3, "cost": 18000, "preds": ["ACT-09", "ACT-10", "ACT-14", "ACT-17"]},
    "ACT-19": {"name": "Automated Test Suite (JUnit)", "wbs": "1.5.1", "dur": 4, "cost": 20000, "preds": ["ACT-11", "ACT-12", "ACT-13", "ACT-15", "ACT-18"]},
    "ACT-20": {"name": "Field Pilot Rollout & UAT", "wbs": "1.5.2", "dur": 3, "cost": 14000, "preds": ["ACT-19"]},
    "ACT-21": {"name": "Documentation & Handover", "wbs": "1.5.3", "dur": 3, "cost": 12000, "preds": ["ACT-20"]}
}

# Build DAG
G = nx.DiGraph()
for act_id, d in activities.items():
    G.add_node(act_id, name=d["name"], dur=d["dur"], cost=d["cost"])
    for p in d["preds"]:
        G.add_edge(p, act_id)

# Successors mapping
succs = {act: list(G.successors(act)) for act in activities}

# Forward Pass (ES & EF) using 0-based time index
es = {}
ef = {}
for act in nx.topological_sort(G):
    preds = activities[act]["preds"]
    if not preds:
        es[act] = 0
    else:
        es[act] = max(ef[p] for p in preds)
    ef[act] = es[act] + activities[act]["dur"]

project_duration = max(ef.values())

# Backward Pass (LS & LF)
ls = {}
lf = {}
for act in reversed(list(nx.topological_sort(G))):
    s_list = succs[act]
    if not s_list:
        lf[act] = project_duration
    else:
        lf[act] = min(ls[s] for s in s_list)
    ls[act] = lf[act] - activities[act]["dur"]

# Total Float & Free Float
tf = {}
ff = {}
critical_acts = []
for act in activities:
    tf[act] = ls[act] - es[act]
    s_list = succs[act]
    if not s_list:
        ff[act] = project_duration - ef[act]
    else:
        ff[act] = min(es[s] for s in s_list) - ef[act]
    if tf[act] == 0:
        critical_acts.append(act)

# Find all paths from start nodes to end nodes
start_nodes = [n for n in G.nodes if G.in_degree(n) == 0]
end_nodes = [n for n in G.nodes if G.out_degree(n) == 0]

all_paths = []
for s in start_nodes:
    for e in end_nodes:
        for path in nx.all_simple_paths(G, s, e):
            p_len = sum(activities[n]["dur"] for n in path)
            all_paths.append((path, p_len))

all_paths.sort(key=lambda x: x[1], reverse=True)

print(f"Project Duration: {project_duration} Working Days")
print(f"Critical Path: {' -> '.join(all_paths[0][0])} (Length: {all_paths[0][1]} Days)")
print(f"Number of Paths in Network: {len(all_paths)}")
print("\nTop 5 Paths by Duration:")
for i, (p, l) in enumerate(all_paths[:5]):
    print(f"  Path {i+1} ({l} days): {' -> '.join(p)}")

print("\nActivity CPM Schedule Details:")
print("Act ID | Dur | ES | EF | LS | LF | TF | FF | Critical? | Name")
print("-" * 80)
for act in sorted(activities.keys()):
    is_crit = "YES (CP)" if tf[act] == 0 else "NO"
    print(f"{act:6} | {activities[act]['dur']:3} | {es[act]:2} | {ef[act]:2} | {ls[act]:2} | {lf[act]:2} | {tf[act]:2} | {ff[act]:2} | {is_crit:9} | {activities[act]['name']}")
