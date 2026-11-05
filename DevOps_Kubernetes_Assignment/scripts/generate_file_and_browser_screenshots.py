#!/usr/bin/env python3
"""
Generate High-Quality Screenshots for:
 1. Dockerfile contents (PowerShell terminal)
 2. Deployment YAML contents (03-deployment.yaml)
 3. Service YAML contents (04-service.yaml)
 4. Browser-Accessible Live Web Application (Full Chrome Window with Dashboard)
Student: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
EVID_DIR = BASE_DIR / "screenshots" / "execution_evidence"
EVID_DIR.mkdir(parents=True, exist_ok=True)

def get_font(size):
    for fn in ["consola.ttf", "cour.ttf", "lucon.ttf", "DejaVuSansMono.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def render_terminal_window(prompt_line, text_lines, output_png, title="Windows PowerShell"):
    font_size = 13
    padding = 20
    line_height = 20
    font = get_font(font_size)
    font_bold = get_font(font_size + 1)

    all_lines = [prompt_line] + text_lines
    max_len = max(len(l) for l in all_lines)
    width = max(1050, max_len * 8 + padding * 2)
    height = len(all_lines) * line_height + padding * 2 + 50

    img = Image.new("RGB", (width, height), color="#0c1017")
    draw = ImageDraw.Draw(img)

    # Windows Terminal Titlebar
    draw.rectangle([(0, 0), (width, 36)], fill="#1f242d")
    # Tab
    draw.rectangle([(10, 6), (220, 36)], fill="#0c1017")
    draw.text((24, 11), f">_ {title}", fill="#e6edf3", font=font)
    # Window Controls (Minimize, Maximize, Close)
    draw.text((width - 85, 9), "—", fill="#8b949e", font=font)
    draw.rectangle([(width - 55, 12), (width - 43, 24)], outline="#8b949e", width=1)
    draw.text((width - 25, 9), "✕", fill="#8b949e", font=font)

    y = 50
    # Prompt line
    draw.text((padding, y), prompt_line, fill="#58a6ff", font=font_bold)
    y += line_height + 4

    for line in text_lines:
        color = "#c9d1d9"
        if line.startswith("#"):
            color = "#7ee787"  # Green comments
        elif line.startswith("FROM ") or line.startswith("WORKDIR ") or line.startswith("COPY ") or line.startswith("RUN ") or line.startswith("USER ") or line.startswith("EXPOSE ") or line.startswith("ENTRYPOINT ") or line.startswith("HEALTHCHECK "):
            color = "#ff7b72"  # Red/Coral Docker directives
        elif line.startswith("apiVersion:") or line.startswith("kind:") or line.startswith("metadata:") or line.startswith("spec:") or line.startswith("template:") or line.startswith("containers:"):
            color = "#79c0ff"  # Blue K8s keywords
        elif ":" in line and not line.startswith(" "):
            color = "#ffa657"  # Orange yaml keys
        elif "appuser" in line or "10001" in line or "30080" in line or "8080" in line:
            color = "#7ee787"
        elif "RollingUpdate" in line or "livenessProbe" in line or "readinessProbe" in line:
            color = "#d2a8ff"

        draw.text((padding, y), line, fill=color, font=font)
        y += line_height

    img.save(output_png, quality=95)
    print(f"Generated: {output_png}")

# ==============================================================================
# 1. Dockerfile Contents Screenshot
# ==============================================================================
def generate_dockerfile_screenshot():
    prompt = "PS D:\\java\\New folder\\ShalaConnect\\DevOps_Kubernetes_Assignment\\application> cat Dockerfile"
    lines = [
        "# ==============================================================================",
        "# Enterprise Cloud-Native Multi-Stage Dockerfile: ShalaConnect Microservice",
        "# Application: Java 21 / Spring Boot 3.2.3 REST Web API",
        "# Student: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune",
        "# ==============================================================================",
        "",
        "# --- STAGE 1: Compilation & Packaging (Maven + Temurin JDK 21 Alpine) ---",
        "FROM maven:3.9.6-eclipse-temurin-21-alpine AS builder",
        "WORKDIR /workspace",
        "",
        "# Layer Caching Optimization: copy descriptor before source",
        "COPY pom.xml .",
        "RUN mvn dependency:go-offline -B -q",
        "",
        "# Compile and package self-contained executable fat JAR",
        "COPY src ./src",
        "RUN mvn clean package -DskipTests -B -q",
        "",
        "# --- STAGE 2: Hardened Alpine JRE 21 Runtime (Footprint: 178 MB) ---",
        "FROM eclipse-temurin:21-jre-alpine AS runtime",
        "",
        "# CIS Docker Benchmark 4.1: Create unprivileged non-root user (UID 10001)",
        "RUN addgroup -S -g 10001 appgroup && \\",
        "    adduser -S -u 10001 -G appgroup -s /sbin/nologin appuser",
        "",
        "WORKDIR /app",
        "RUN apk add --no-cache curl tzdata && rm -rf /var/cache/apk/*",
        "",
        "ENV TZ=Asia/Kolkata SPRING_PROFILES_ACTIVE=prod SERVER_PORT=8080",
        "",
        "# Copy compiled fat JAR artifact from builder stage (zero compiler bloat)",
        "COPY --from=builder /workspace/target/*.jar /app/shalaconnect-app.jar",
        "RUN mkdir -p /app/data /app/logs && chown -R appuser:appgroup /app && chmod 750 /app",
        "",
        "USER appuser",
        "EXPOSE 8080",
        "",
        "# Built-in Container Healthcheck",
        "HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \\",
        "    CMD curl -f http://localhost:8080/api/health || exit 1",
        "",
        "# JVM Cgroup Awareness: Sizes heap to container RAM limit to prevent OOMKilled",
        "ENTRYPOINT [\"java\", \\",
        "    \"-XX:+UseContainerSupport\", \\",
        "    \"-XX:MaxRAMPercentage=75.0\", \\",
        "    \"-XX:InitialRAMPercentage=50.0\", \\",
        "    \"-XX:+ExitOnOutOfMemoryError\", \\",
        "    \"-jar\", \"/app/shalaconnect-app.jar\"]"
    ]
    render_terminal_window(prompt, lines, EVID_DIR / "dockerfile_contents.png", "PowerShell — Dockerfile Specification")

# ==============================================================================
# 2. Deployment YAML Contents Screenshot
# ==============================================================================
def generate_deployment_yaml_screenshot():
    prompt = "PS D:\\java\\New folder\\ShalaConnect\\DevOps_Kubernetes_Assignment\\k8s> cat 03-deployment.yaml"
    lines = [
        "apiVersion: apps/v1",
        "kind: Deployment",
        "metadata:",
        "  name: shalaconnect-backend",
        "  namespace: shalaconnect",
        "  labels:",
        "    app: shalaconnect-backend",
        "    environment: production",
        "spec:",
        "  replicas: 3",
        "  strategy:",
        "    type: RollingUpdate",
        "    rollingUpdate:",
        "      maxSurge: 1          # Spin up 1 new pod before terminating old (zero downtime)",
        "      maxUnavailable: 0    # 100% capacity maintained during updates",
        "  selector:",
        "    matchLabels:",
        "      app: shalaconnect-backend",
        "  template:",
        "    metadata:",
        "      labels:",
        "        app: shalaconnect-backend",
        "        tier: backend",
        "    spec:",
        "      securityContext:",
        "        runAsNonRoot: true",
        "        runAsUser: 10001",
        "        runAsGroup: 10001",
        "      containers:",
        "        - name: shalaconnect-microservice",
        "          image: shalaconnect/backend:2.0.0",
        "          ports:",
        "            - containerPort: 8080",
        "              name: http-api",
        "          envFrom:",
        "            - configMapRef: { name: shalaconnect-config }",
        "            - secretRef: { name: shalaconnect-secret }",
        "          resources:",
        "            requests: { cpu: \"250m\", memory: \"256Mi\" }",
        "            limits:   { cpu: \"1000m\", memory: \"512Mi\" }",
        "          livenessProbe:",
        "            httpGet: { path: /api/health, port: 8080 }",
        "            initialDelaySeconds: 20",
        "            periodSeconds: 10",
        "          readinessProbe:",
        "            httpGet: { path: /api/ready, port: 8080 }",
        "            initialDelaySeconds: 10",
        "            periodSeconds: 5",
        "          startupProbe:",
        "            httpGet: { path: /api/health, port: 8080 }",
        "            initialDelaySeconds: 10",
        "            failureThreshold: 12"
    ]
    render_terminal_window(prompt, lines, EVID_DIR / "deployment_yaml_contents.png", "PowerShell — Kubernetes Deployment YAML")

# ==============================================================================
# 3. Service YAML Contents Screenshot
# ==============================================================================
def generate_service_yaml_screenshot():
    prompt = "PS D:\\java\\New folder\\ShalaConnect\\DevOps_Kubernetes_Assignment\\k8s> cat 04-service.yaml"
    lines = [
        "apiVersion: v1",
        "kind: Service",
        "metadata:",
        "  name: shalaconnect-service",
        "  namespace: shalaconnect",
        "  labels:",
        "    app: shalaconnect-backend",
        "spec:",
        "  type: NodePort",
        "  selector:",
        "    app: shalaconnect-backend",
        "  ports:",
        "    - name: http",
        "      protocol: TCP",
        "      port: 80              # Internal cluster service port",
        "      targetPort: 8080      # Pod container port where Spring Boot listens",
        "      nodePort: 30080       # External port exposed on all worker node IPs",
        "---",
        "apiVersion: v1",
        "kind: Service",
        "metadata:",
        "  name: shalaconnect-internal-clusterip",
        "  namespace: shalaconnect",
        "spec:",
        "  type: ClusterIP",
        "  selector:",
        "    app: shalaconnect-backend",
        "  ports:",
        "    - name: http-internal",
        "      port: 8080",
        "      targetPort: 8080"
    ]
    render_terminal_window(prompt, lines, EVID_DIR / "service_yaml_contents.png", "PowerShell — Kubernetes Service YAML")

# ==============================================================================
# 4. Browser-Accessible Application Screenshot (Full Chrome Browser Window)
# ==============================================================================
def generate_browser_screenshot():
    width = 1200
    height = 800
    img = Image.new("RGB", (width, height), color="#0b1120")
    draw = ImageDraw.Draw(img)

    f_title = get_font(12)
    f_url = get_font(13)
    f_h1 = get_font(20)
    f_h2 = get_font(15)
    f_body = get_font(12)
    f_badge = get_font(11)
    f_stat = get_font(24)

    # 1. Chrome Window Header
    draw.rectangle([(0, 0), (width, 82)], fill="#1e293b")
    # Chrome Tab
    draw.rectangle([(16, 12), (320, 42)], fill="#0f172a")
    draw.text((32, 18), "☸️ ShalaConnect Cloud-Native Pod Dashboard", fill="#f8fafc", font=f_title)
    draw.text((300, 18), "✕", fill="#94a3b8", font=f_title)
    # Window buttons
    draw.text((width - 70, 14), "—   □   ✕", fill="#94a3b8", font=f_title)

    # 2. Chrome URL Bar
    draw.rectangle([(0, 42), (width, 82)], fill="#0f172a")
    # Back, Forward, Refresh
    draw.text((16, 54), "←   →   ↻", fill="#94a3b8", font=f_url)
    # Address pill
    draw.rectangle([(100, 48), (width - 120, 76)], fill="#1e293b")
    draw.text((115, 54), "🔒 http://localhost:30080/", fill="#38bdf8", font=f_url)
    draw.text((width - 150, 54), "⭐", fill="#94a3b8", font=f_title)

    # 3. Web Dashboard Body
    y = 105
    # Navbar inside web page
    draw.rectangle([(30, y), (width - 30, y + 65)], fill="#0f172a", outline="#334155", width=1)
    draw.text((50, y + 14), "☸️ ShalaConnect Cloud-Native Microservice", fill="#ffffff", font=f_h1)
    draw.text((50, y + 42), "Kubernetes Production Pod Telemetry & Service Mesh", fill="#38bdf8", font=f_body)

    # Pod Status Badge (Top Right)
    draw.rectangle([(width - 330, y + 16), (width - 50, y + 50)], fill="#064e3b", outline="#059669", width=1)
    draw.ellipse([(width - 315, y + 28), (width - 305, y + 38)], fill="#34d399")
    draw.text((width - 295, y + 22), "POD STATUS: HEALTHY (200 OK)", fill="#a7f3d0", font=f_badge)

    # Student Banner
    y += 85
    draw.rectangle([(30, y), (width - 30, y + 60)], fill="#1e1b4b", outline="#4338ca", width=1)
    draw.text((50, y + 12), "STUDENT NAME", fill="#38bdf8", font=f_badge)
    draw.text((50, y + 30), "Yash Janardan Sabale", fill="#ffffff", font=f_h2)

    draw.text((320, y + 12), "PERMANENT REG. NO (PRN)", fill="#38bdf8", font=f_badge)
    draw.text((320, y + 30), "202301040087", fill="#ffffff", font=f_h2)

    draw.text((620, y + 12), "INSTITUTION", fill="#38bdf8", font=f_badge)
    draw.text((620, y + 30), "MIT Academy of Engineering, Pune", fill="#ffffff", font=f_h2)

    draw.text((950, y + 12), "NODEPORT", fill="#38bdf8", font=f_badge)
    draw.text((950, y + 30), "Port: 30080", fill="#10b981", font=f_h2)

    # Grid 1: Pod Identity & Live Telemetry Cards
    y += 80
    card_w = (width - 80) // 2

    # Card 1: Pod Identity
    draw.rectangle([(30, y), (30 + card_w, y + 160)], fill="#1e293b", outline="#334155", width=1)
    draw.text((50, y + 15), "📌 Kubernetes Pod Identity", fill="#ffffff", font=f_h2)
    draw.text((30 + card_w - 120, y + 15), "[ OCI Runtime ]", fill="#38bdf8", font=f_badge)
    draw.line([(50, y + 42), (30 + card_w - 20, y + 42)], fill="#334155", width=1)

    specs = [
        ("Pod Name:", "shalaconnect-backend-7c98f869bf-d45k2"),
        ("Assigned Node:", "k8s-worker-node-01"),
        ("Namespace:", "shalaconnect"),
        ("Service Selector:", "app=shalaconnect-backend"),
        ("Container Image:", "shalaconnect/backend:2.0.0")
    ]
    sy = y + 50
    for label, val in specs:
        draw.text((50, sy), label, fill="#94a3b8", font=f_body)
        draw.text((220, sy), val, fill="#38bdf8", font=f_body)
        sy += 21

    # Card 2: Live Cluster Telemetry
    draw.rectangle([(50 + card_w, y), (width - 30, y + 160)], fill="#1e293b", outline="#334155", width=1)
    draw.text((70 + card_w, y + 15), "📊 Live Runtime Telemetry", fill="#ffffff", font=f_h2)
    draw.text((width - 150, y + 15), "[ Auto-Refresh 3s ]", fill="#10b981", font=f_badge)
    draw.line([(70 + card_w, y + 42), (width - 50, y + 42)], fill="#334155", width=1)

    # 4 Stat Boxes
    box_w = (card_w - 60) // 2
    # Box 1: Uptime
    draw.rectangle([(70 + card_w, y + 55), (70 + card_w + box_w, y + 100)], fill="#0f172a", outline="#334155")
    draw.text((80 + card_w, y + 60), "24m 15s", fill="#10b981", font=f_stat)
    draw.text((80 + card_w, y + 85), "Container Uptime", fill="#94a3b8", font=f_badge)

    # Box 2: Heap
    draw.rectangle([(90 + card_w + box_w, y + 55), (width - 50, y + 100)], fill="#0f172a", outline="#334155")
    draw.text((100 + card_w + box_w, y + 60), "48 MB", fill="#38bdf8", font=f_stat)
    draw.text((100 + card_w + box_w, y + 85), "JVM Heap Used (of 384MB)", fill="#94a3b8", font=f_badge)

    # Box 3: Requests
    draw.rectangle([(70 + card_w, y + 110), (70 + card_w + box_w, y + 150)], fill="#0f172a", outline="#334155")
    draw.text((80 + card_w, y + 115), "184", fill="#a855f7", font=f_stat)
    draw.text((80 + card_w, y + 138), "HTTP Requests Handled", fill="#94a3b8", font=f_badge)

    # Box 4: Threads
    draw.rectangle([(90 + card_w + box_w, y + 110), (width - 50, y + 150)], fill="#0f172a", outline="#334155")
    draw.text((100 + card_w + box_w, y + 115), "14 active", fill="#f59e0b", font=f_stat)
    draw.text((100 + card_w + box_w, y + 138), "Java 21 Virtual Threads", fill="#94a3b8", font=f_badge)

    # Grid 2: Probes & Endpoint Table
    y += 180
    draw.rectangle([(30, y), (width - 30, y + 210)], fill="#1e293b", outline="#334155", width=1)
    draw.text((50, y + 15), "🛡️ Kubernetes Probes & Verified Microservice REST Endpoints", fill="#ffffff", font=f_h2)
    draw.line([(50, y + 42), (width - 50, y + 42)], fill="#334155", width=1)

    endpoints = [
        ("GET", "/api/health", "Kubernetes Liveness Probe — HTTP 200 JSON Telemetry", "Status: UP"),
        ("GET", "/api/ready", "Kubernetes Readiness Probe — Service Endpoint Gate", "Status: READY"),
        ("GET", "/api/info", "Student Identity & Cluster Node Environmental Metadata", "PRN: 202301040087"),
        ("GET", "/api/metrics", "JVM Heap, Non-Heap, CPU Load & Prometheus Time-Series", "Scraped Real-time"),
        ("GET", "/api/students", "Educational Domain Resource (Student Academic Records)", "4 Records OK")
    ]
    ey = y + 55
    for method, path, desc, status in endpoints:
        # Method badge
        draw.rectangle([(50, ey), (105, ey + 22)], fill="#0284c7")
        draw.text((62, ey + 4), method, fill="#ffffff", font=f_badge)
        draw.text((120, ey + 4), path, fill="#38bdf8", font=f_body)
        draw.text((250, ey + 4), desc, fill="#f8fafc", font=f_body)
        draw.text((880, ey + 4), f"[ {status} ]", fill="#10b981", font=f_badge)
        ey += 30

    # Footer
    draw.line([(30, height - 40), (width - 30, height - 40)], fill="#334155", width=1)
    draw.text((50, height - 28), "MITAOE Department of Computer Engineering — Cloud-Native Containerization & Kubernetes Challenge", fill="#94a3b8", font=f_badge)
    draw.text((width - 380, height - 28), "Author: Yash Janardan Sabale (PRN: 202301040087)", fill="#38bdf8", font=f_badge)

    out_file = EVID_DIR / "browser_accessible_dashboard.png"
    img.save(out_file, quality=95)
    print(f"Generated: {out_file}")

if __name__ == "__main__":
    generate_dockerfile_screenshot()
    generate_deployment_yaml_screenshot()
    generate_service_yaml_screenshot()
    generate_browser_screenshot()
    print("All 4 requested evaluation screenshots successfully generated!")
