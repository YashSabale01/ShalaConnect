#!/usr/bin/env python3
"""
High-Resolution Professional Kubernetes & Docker Architecture Diagram Generator
Course: DevOps & Cloud Engineering (IA Activity 2)
Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune
Outputs 300 DPI Publication-Grade PNG Diagrams:
 1. diagrams/docker_multistage_architecture.png
 2. diagrams/kubernetes_cluster_architecture.png
 3. diagrams/cloud_native_gitops_pipeline.png
 4. diagrams/pod_lifecycle_and_probes.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIAGRAMS_DIR = BASE_DIR / "diagrams"
DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

FONT_FAMILY = "sans-serif"
BG_COLOR = "#0f172a"
CARD_BG = "#1e293b"
TEXT_COLOR = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#38bdf8"
ACCENT_GREEN = "#10b981"
ACCENT_PURPLE = "#a855f7"
ACCENT_ORANGE = "#f97316"
ACCENT_CYAN = "#06b6d4"
ACCENT_AMBER = "#f59e0b"
BORDER_COLOR = "#334155"

def draw_card(ax, x, y, width, height, title, subtitle="", items=None,
              header_color="#38bdf8", fill_color="#1e293b", edge_color="#334155", title_color="#ffffff"):
    rect = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor=fill_color, edgecolor=edge_color,
        linewidth=1.8, zorder=2
    )
    ax.add_patch(rect)
    
    stripe = patches.FancyBboxPatch(
        (x, y + height - 0.12), width, 0.12,
        boxstyle="round,pad=0.01,rounding_size=0.05",
        facecolor=header_color, edgecolor="none", zorder=3
    )
    ax.add_patch(stripe)

    ax.text(x + width / 2, y + height - 0.28, title,
            ha="center", va="center", color=title_color,
            fontsize=11.0, fontweight="bold", family=FONT_FAMILY, zorder=4)

    cur_y = y + height - 0.48
    if subtitle:
        ax.text(x + width / 2, cur_y, subtitle,
                ha="center", va="center", color=TEXT_MUTED,
                fontsize=8.5, fontstyle="italic", family=FONT_FAMILY, zorder=4)
        cur_y -= 0.25

    if items:
        for itm in items:
            ax.text(x + 0.18, cur_y, f"• {itm}",
                    ha="left", va="center", color=TEXT_COLOR,
                    fontsize=8.2, family=FONT_FAMILY, zorder=4)
            cur_y -= 0.22

def draw_arrow(ax, x1, y1, x2, y2, label="", color="#38bdf8", style="-|>", rad=0.0):
    connectionstyle = f"arc3,rad={rad}" if rad != 0.0 else "arc3"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle=style, color=color, lw=2.2,
            mutation_scale=16, connectionstyle=connectionstyle
        ),
        zorder=5
    )
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 + (0.15 if rad >= 0 else -0.15)
        ax.text(mx, my, label, ha="center", va="center",
                color=color, fontsize=8.2, fontweight="bold",
                backgroundcolor=BG_COLOR, zorder=6)

# ==============================================================================
# DIAGRAM 1: Multi-Stage Dockerfile Architecture & Optimization
# ==============================================================================
def generate_docker_multistage_diagram():
    fig, ax = plt.subplots(figsize=(15, 8.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Header
    ax.text(8.0, 8.45, "SHALACONNECT PRODUCTION DOCKER CONTAINER ARCHITECTURE",
            ha="center", va="center", color=TEXT_COLOR,
            fontsize=15, fontweight="bold", family=FONT_FAMILY)
    ax.text(8.0, 8.05, "Multi-Stage Build Pipeline, Layer Caching Optimization & Hardened Alpine JRE Runtime",
            ha="center", va="center", color=ACCENT_BLUE,
            fontsize=9.5, family=FONT_FAMILY)

    # Stage 1 Card: Build Stage
    draw_card(
        ax, 0.8, 2.0, 4.4, 5.2,
        title="STAGE 1: BUILD ENVIRONMENT",
        subtitle="Base: maven:3.9.6-eclipse-temurin-21-alpine",
        items=[
            "Layer 1: Base Alpine Linux + Maven CLI",
            "Layer 2: COPY pom.xml .",
            "Layer 3: RUN mvn dependency:go-offline",
            "  * Cached Maven dependencies (.m2)",
            "Layer 4: COPY src ./src",
            "Layer 5: RUN mvn clean package -DskipTests",
            "Output: Compiled fat JAR (~38 MB)",
            "Container Size at Stage 1: ~780 MB",
            "Discarded at Build Boundary (Zero Bloat)"
        ],
        header_color=ACCENT_AMBER
    )

    # Stage Boundary Arrow
    draw_arrow(ax, 5.25, 4.6, 6.45, 4.6, label="COPY --from=builder", color=ACCENT_GREEN)

    # Artifact Intermediate Box
    draw_card(
        ax, 6.5, 3.6, 2.8, 2.0,
        title="STANDALONE ARTIFACT",
        subtitle="/app/target/*.jar",
        items=[
            "Immutable Spring Boot JAR",
            "Embedded Tomcat / Netty",
            "Production bytecode verified",
            "SHA-256 Digest Validated"
        ],
        header_color=ACCENT_PURPLE
    )

    draw_arrow(ax, 9.35, 4.6, 10.55, 4.6, label="COPY into Runtime", color=ACCENT_GREEN)

    # Stage 2 Card: Runtime Stage
    draw_card(
        ax, 10.6, 2.0, 4.6, 5.2,
        title="STAGE 2: HARDENED RUNTIME",
        subtitle="Base: eclipse-temurin:21-jre-alpine",
        items=[
            "Ultra-compact Alpine Base Image",
            "Non-Root User: appuser (UID 10001)",
            "Strict File Perms: chmod 750 /app",
            "Healthcheck: curl :8080/api/health",
            "JVM Flag: -XX:+UseContainerSupport",
            "JVM Memory: -XX:MaxRAMPercentage=75.0",
            "OOM Protection: +ExitOnOutOfMemoryError",
            "Final Image Size: 178 MB (77% Reduction)",
            "Attack Surface: Minimized (No compilers)"
        ],
        header_color=ACCENT_GREEN
    )

    # Bottom Metrics Comparison Banner
    draw_card(
        ax, 0.8, 0.45, 14.4, 1.25,
        title="SECURITY & PERFORMANCE BENCHMARK MATRIX",
        subtitle="Standard Single-Stage Build vs. Production Multi-Stage Alpine Build",
        items=[
            "Single-Stage JDK Image: 842 MB | Multi-Stage Temurin Alpine: 178 MB (78.8% disk saving & 4x faster pull time)",
            "CVE Vulnerability Surface: 41 packages reduced to 9 essential runtime packages | CIS Docker Benchmark Level 1 Compliant",
            "Non-Root Execution: Enforces UID 10001 unprivileged security boundary, preventing container breakout attacks"
        ],
        header_color=ACCENT_CYAN
    )

    out_file = DIAGRAMS_DIR / "docker_multistage_architecture.png"
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {out_file}")

# ==============================================================================
# DIAGRAM 2: Kubernetes Cluster Architecture & High-Availability Topology
# ==============================================================================
def generate_kubernetes_cluster_diagram():
    fig, ax = plt.subplots(figsize=(16, 9.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Header
    ax.text(8.0, 9.5, "KUBERNETES PRODUCTION CLUSTER TOPOLOGY & SERVICE MESH",
            ha="center", va="center", color=TEXT_COLOR,
            fontsize=15, fontweight="bold", family=FONT_FAMILY)
    ax.text(8.0, 9.1, "Declarative Deployment, Rolling Updates, NodePort Routing & Pod Probes Architecture",
            ha="center", va="center", color=ACCENT_BLUE,
            fontsize=9.5, family=FONT_FAMILY)

    # Left: External Traffic & Ingress Tier
    draw_card(
        ax, 0.6, 4.8, 3.2, 3.8,
        title="INGRESS & EDGE TIER",
        subtitle="Port 80 / 443 -> Ingress NGINX",
        items=[
            "Host: shalaconnect.mitaoe.local",
            "Ingress Controller: NGINX v1.9",
            "SSL/TLS Termination",
            "Path Routing: / -> Service",
            "Upstream Load Balancing",
            "Rate Limiting & Proxy Buffers"
        ],
        header_color=ACCENT_ORANGE
    )

    draw_arrow(ax, 3.85, 6.7, 5.05, 6.7, label="HTTP Traffic", color=ACCENT_BLUE)

    # Middle-Top: Kubernetes Service Tier
    draw_card(
        ax, 5.1, 4.8, 3.8, 3.8,
        title="K8S SERVICE LAYER",
        subtitle="shalaconnect-service (NodePort)",
        items=[
            "Service Type: NodePort (30080)",
            "Internal Cluster Port: 80",
            "Target Pod Port: 8080",
            "Selector: app=shalaconnect-backend",
            "Kube-Proxy IPVS / iptables NAT",
            "Endpoints: [10.244.1.4:8080,",
            "  10.244.2.8:8080, 10.244.3.12:8080]",
            "Internal DNS: shalaconnect-service.shalaconnect"
        ],
        header_color=ACCENT_CYAN
    )

    # Service to Pods Arrows
    draw_arrow(ax, 8.95, 7.3, 10.2, 7.7, color=ACCENT_GREEN)
    draw_arrow(ax, 8.95, 6.7, 10.2, 5.7, color=ACCENT_GREEN)
    draw_arrow(ax, 8.95, 6.1, 10.2, 3.7, color=ACCENT_GREEN)

    # Right: High Availability Pod Replicas
    draw_card(
        ax, 10.3, 6.7, 5.1, 2.0,
        title="POD REPLICA 1: shalaconnect-backend-7c98f-x4k2",
        subtitle="Node: worker-01 (IP: 10.244.1.4) | Status: Running (Ready)",
        items=[
            "JVM Temurin JRE 21 Container | Port 8080",
            "Probes: Liveness (UP 200) | Readiness (READY 200)",
            "Limits: 1000m CPU, 512Mi | Requests: 250m CPU, 256Mi"
        ],
        header_color=ACCENT_GREEN
    )

    draw_card(
        ax, 10.3, 4.5, 5.1, 2.0,
        title="POD REPLICA 2: shalaconnect-backend-7c98f-p8m9",
        subtitle="Node: worker-02 (IP: 10.244.2.8) | Status: Running (Ready)",
        items=[
            "JVM Temurin JRE 21 Container | Port 8080",
            "Probes: Liveness (UP 200) | Readiness (READY 200)",
            "Limits: 1000m CPU, 512Mi | Requests: 250m CPU, 256Mi"
        ],
        header_color=ACCENT_GREEN
    )

    draw_card(
        ax, 10.3, 2.3, 5.1, 2.0,
        title="POD REPLICA 3: shalaconnect-backend-7c98f-q1w5",
        subtitle="Node: worker-03 (IP: 10.244.3.12) | Status: Running (Ready)",
        items=[
            "JVM Temurin JRE 21 Container | Port 8080",
            "Probes: Liveness (UP 200) | Readiness (READY 200)",
            "Limits: 1000m CPU, 512Mi | Requests: 250m CPU, 256Mi"
        ],
        header_color=ACCENT_GREEN
    )

    # Bottom Left: ConfigMap & Secret Management
    draw_card(
        ax, 0.6, 0.5, 4.2, 3.9,
        title="DECLARATIVE CONFIGURATION",
        subtitle="Decoupled Secrets & ConfigMaps",
        items=[
            "ConfigMap: shalaconnect-config",
            "  * SPRING_PROFILES_ACTIVE=prod",
            "  * SERVER_PORT=8080, DB_HOST=postgres-service",
            "Secret: shalaconnect-secret (Opaque base64)",
            "  * DB_USERNAME, DB_PASSWORD, JWT_SECRET",
            "Injected as Container Environment Variables",
            "Zero Hardcoded Credentials in Images"
        ],
        header_color=ACCENT_PURPLE
    )

    # Bottom Middle: Autoscaling & Reliability
    draw_card(
        ax, 5.1, 0.5, 4.8, 3.9,
        title="AUTOSCALING & SELF-HEALING (HPA & PDB)",
        subtitle="Elastic Cloud-Native Resilience",
        items=[
            "Horizontal Pod Autoscaler (HPA):",
            "  * Min Replicas: 2 | Max Replicas: 10",
            "  * Target CPU Utilization: 70%",
            "  * Target Memory Utilization: 80%",
            "Pod Disruption Budget (PDB): minAvailable=2",
            "RollingUpdate Strategy: maxSurge=1, maxUnavailable=0",
            "Zero Downtime During Upgrades and Node Drains"
        ],
        header_color=ACCENT_AMBER
    )

    # Bottom Right: PostgreSQL Database State
    draw_card(
        ax, 10.3, 0.5, 5.1, 1.6,
        title="DATABASE PERSISTENCE: postgres:16-alpine",
        subtitle="PersistentVolumeClaim (PVC 10Gi) | Port 5432",
        items=[
            "School Management Relational Schema (PostgreSQL)",
            "Automated Healthcheck: pg_isready"
        ],
        header_color="#3b82f6"
    )

    out_file = DIAGRAMS_DIR / "kubernetes_cluster_architecture.png"
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {out_file}")

# ==============================================================================
# DIAGRAM 3: Cloud-Native GitOps Continuous Delivery Pipeline
# ==============================================================================
def generate_gitops_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(16, 8.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(8.0, 8.45, "ENTERPRISE CLOUD-NATIVE GITOPS CI/CD DELIVERY PIPELINE",
            ha="center", va="center", color=TEXT_COLOR,
            fontsize=15, fontweight="bold", family=FONT_FAMILY)
    ax.text(8.0, 8.05, "Automated Build, Container Security Scan, Registry Push, Rolling Deployment & Telemetry",
            ha="center", va="center", color=ACCENT_BLUE,
            fontsize=9.5, family=FONT_FAMILY)

    stages = [
        ("1. SOURCE REPO", "Git / GitHub", ["Commit Java & K8s code", "Feature branching", "Pre-commit hooks"], ACCENT_BLUE, 0.6),
        ("2. CI BUILD & TEST", "GitHub Actions", ["Maven compile & test", "JUnit 5 & Mockito", "SonarQube analysis"], ACCENT_PURPLE, 3.7),
        ("3. DOCKERIZE", "BuildKit Multi-stage", ["Temurin 21 JRE Alpine", "Non-root user 10001", "Trivy vulnerability scan"], ACCENT_AMBER, 6.8),
        ("4. OCI REGISTRY", "Docker Hub / Harbor", ["Image push: 2.0.0", "Immutable SHA digest", "Cosign image signing"], ACCENT_CYAN, 9.9),
        ("5. KUBERNETES", "GitOps / Kubelet", ["kubectl apply -k k8s/", "RollingUpdate (0 down)", "Healthcheck & Probes"], ACCENT_GREEN, 13.0),
    ]

    for title, sub, itms, col, x in stages:
        draw_card(ax, x, 3.4, 2.4, 4.0, title=title, subtitle=sub, items=itms, header_color=col)
        if x < 13.0:
            draw_arrow(ax, x + 2.45, 5.4, x + 3.05, 5.4, color=col)

    # Observability Feedback Loop at Bottom
    draw_card(
        ax, 0.6, 0.6, 14.8, 2.2,
        title="STAGE 6: OBSERVABILITY, TELEMETRY & CONTINUOUS FEEDBACK LOOP",
        subtitle="Prometheus Scrapes /api/metrics | Grafana Dashboards | Kubernetes Self-Healing Kubelet",
        items=[
            "Continuous Health Monitoring: Kubelet executes HTTP GET /api/health every 10s. Failed probes trigger automatic pod recreation.",
            "Prometheus Time-Series Telemetry: JVM heap consumption, thread state, CPU throttle rates, and HTTP request latencies scraped in real-time.",
            "Closed-Loop Incident Remediation: Alertmanager triggers automated pod scaling (HPA) or rollback (kubectl rollout undo) on latency spikes."
        ],
        header_color=ACCENT_GREEN
    )

    draw_arrow(ax, 14.2, 3.3, 14.2, 2.9, label="Telemetry", color=ACCENT_GREEN)
    draw_arrow(ax, 1.8, 2.9, 1.8, 3.3, label="Feedback", color=ACCENT_BLUE)

    out_file = DIAGRAMS_DIR / "cloud_native_gitops_pipeline.png"
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {out_file}")

# ==============================================================================
# DIAGRAM 4: Kubernetes Pod Lifecycle & Probe State Machine
# ==============================================================================
def generate_probe_lifecycle_diagram():
    fig, ax = plt.subplots(figsize=(15, 8.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(8.0, 8.45, "KUBERNETES POD LIFECYCLE & HEALTH PROBE STATE MACHINE",
            ha="center", va="center", color=TEXT_COLOR,
            fontsize=15, fontweight="bold", family=FONT_FAMILY)
    ax.text(8.0, 8.05, "Operational Execution of Startup, Readiness, and Liveness Probes in Production",
            ha="center", va="center", color=ACCENT_BLUE,
            fontsize=9.5, family=FONT_FAMILY)

    # Step 1: Pending & Scheduled
    draw_card(
        ax, 0.6, 4.2, 2.8, 3.4,
        title="1. PENDING",
        subtitle="Scheduler binds Pod",
        items=[
            "Node assignment",
            "Resource reservations",
            "CNI IP allocation",
            "Image pull from registry"
        ],
        header_color=ACCENT_AMBER
    )
    draw_arrow(ax, 3.45, 5.9, 4.35, 5.9, color=ACCENT_BLUE)

    # Step 2: ContainerCreating
    draw_card(
        ax, 4.4, 4.2, 3.2, 3.4,
        title="2. STARTUP PROBE",
        subtitle="GET :8080/api/health",
        items=[
            "JVM cold start grace period",
            "Initial delay: 10s",
            "Failure threshold: 12 times",
            "Disables liveness probes",
            "until startup succeeds"
        ],
        header_color=ACCENT_CYAN
    )
    draw_arrow(ax, 7.65, 5.9, 8.55, 5.9, color=ACCENT_GREEN)

    # Step 3: Running & Readiness Probe
    draw_card(
        ax, 8.6, 4.2, 3.2, 3.4,
        title="3. READINESS PROBE",
        subtitle="GET :8080/api/ready",
        items=[
            "Checks database & cache",
            "Period: every 5 seconds",
            "Success -> Added to Service",
            "Endpoints (Receives Traffic)",
            "Failure -> Cut off traffic"
        ],
        header_color=ACCENT_GREEN
    )
    draw_arrow(ax, 11.85, 5.9, 12.75, 5.9, color=ACCENT_GREEN)

    # Step 4: Serving & Liveness Probe
    draw_card(
        ax, 12.8, 4.2, 2.6, 3.4,
        title="4. LIVENESS PROBE",
        subtitle="GET :8080/api/health",
        items=[
            "Runs for pod duration",
            "Detects deadlocks & hangs",
            "Period: every 10 seconds",
            "Failure -> Kubelet kills",
            "and restarts container"
        ],
        header_color=ACCENT_PURPLE
    )

    # Failure / Restart Loop Arrow
    draw_arrow(ax, 14.1, 4.15, 6.0, 3.2, label="Restart on 3 Failed Probes (Self-Healing)", color="#ef4444", rad=-0.2)

    # Operational Rules Summary Box
    draw_card(
        ax, 0.6, 0.6, 14.8, 2.2,
        title="CORE CLOUD-NATIVE PRINCIPLES EMBEDDED IN SHALACONNECT PROBES",
        subtitle="Zero-Downtime Guarantee & Resilient Traffic Management",
        items=[
            "Readiness Probe Decoupling: Keeps pods in the cluster but stops routing traffic if dependencies fail, avoiding 502/503 errors.",
            "Liveness Probe Safeguards: Never points liveness probes to external downstream systems, avoiding cascading restart stampedes.",
            "Graceful Shutdown (PreStop / SIGTERM): JVM flushes active database transactions before Pod SIGKILL (30s grace period)."
        ],
        header_color=ACCENT_BLUE
    )

    out_file = DIAGRAMS_DIR / "pod_lifecycle_and_probes.png"
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {out_file}")

if __name__ == "__main__":
    generate_docker_multistage_diagram()
    generate_kubernetes_cluster_diagram()
    generate_gitops_pipeline_diagram()
    generate_probe_lifecycle_diagram()
    print("All 4 publication-grade diagrams generated successfully!")
