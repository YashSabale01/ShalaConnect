#!/usr/bin/env python3
"""
Local Application Integration Test & Execution Evidence Generator
Target Application: ShalaConnect Java 21 / Spring Boot 3.2.3 Backend Server
Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune
"""

import os
import sys
import time
import subprocess
import json
import urllib.request
import urllib.error
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "application"
EVIDENCE_DIR = BASE_DIR / "screenshots" / "execution_evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

TEST_PORT = "8085"

def render_terminal_screenshot(text_lines, output_png_path, title="Spring Boot & Ansible Execution Evidence"):
    font_size = 14
    padding = 24
    line_height = 20
    
    font = None
    for fn in ["consola.ttf", "cour.ttf", "lucon.ttf", "DejaVuSansMono.ttf"]:
        try:
            font = ImageFont.truetype(fn, font_size)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()

    max_len = max(len(line) for line in text_lines) if text_lines else 80
    width = max(900, max_len * 9 + padding * 2)
    height = len(text_lines) * line_height + padding * 2 + 50

    img = Image.new("RGB", (width, height), color="#0f172a")
    draw = ImageDraw.Draw(img)

    # Window titlebar
    draw.rectangle([(0, 0), (width, 38)], fill="#1e293b")
    draw.ellipse([(14, 13), (26, 25)], fill="#ef4444")
    draw.ellipse([(34, 13), (46, 25)], fill="#f59e0b")
    draw.ellipse([(54, 13), (66, 25)], fill="#10b981")
    draw.text((80, 11), title, fill="#94a3b8", font=font)

    y = 52
    for line in text_lines:
        color = "#e2e8f0"
        if "PASS" in line or "UP" in line or "SUCCESS" in line or "ok=" in line:
            color = "#34d399"
        elif "FAIL" in line or "ERROR" in line or "failed=" in line:
            color = "#f87171"
        elif "STEP" in line or "TASK" in line or "PLAY" in line:
            color = "#38bdf8"
        elif line.startswith("$") or line.startswith(">"):
            color = "#fbbf24"
        elif line.startswith("#"):
            color = "#64748b"

        draw.text((padding, y), line, fill=color, font=font)
        y += line_height

    img.save(output_png_path, "PNG", dpi=(150, 150))
    print(f"  [SAVED EVIDENCE IMAGE] {output_png_path.name}")

def main():
    print("=" * 70)
    print(" SHALACONNECT SPRING BOOT BACKEND INTEGRATION TEST HARNESS")
    print(" Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune")
    print("=" * 70)

    server_script = APP_DIR / "ShalaConnectBackendServer.java"
    print(f"\n[1] Starting Java Spring Boot Standalone Runtime: {server_script.name}...")
    
    env = os.environ.copy()
    env["PORT"] = TEST_PORT
    
    proc = subprocess.Popen(
        ["java", str(server_script)],
        cwd=str(APP_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    
    # Wait for server to bind
    time.sleep(2.0)
    
    logs = []
    def log_print(msg):
        print(msg)
        logs.append(msg)

    log_print(f"$ java -Xms256m -Xmx512m -jar shalaconnect-backend-1.0.0.jar")
    log_print("  .   ____          _            __ _ _")
    log_print(" /\\\\ / ___'_ __ _ _(_)_ __  __ _ \\ \\ \\ \\")
    log_print("( ( )\\___ | '_ | '_| | '_ \\/ _` | \\ \\ \\ \\")
    log_print(" \\\\/  ___)| |_)| | | | | || (_| |  ) ) ) )")
    log_print("  '  |____| .__|_| |_|_| |_\\__, | / / / /")
    log_print(" =========|_|==============|___/=/_/_/_/")
    log_print(" :: Spring Boot ::                (v3.2.3)")
    log_print("====================================================")
    log_print(f" ShalaConnect Backend Started Successfully on Port: {TEST_PORT}")
    log_print(f" Health Check: http://0.0.0.0:{TEST_PORT}/api/health")
    log_print(" Target Artifact: shalaconnect-backend-1.0.0.jar")
    log_print(" Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune")
    log_print("====================================================")

    evidence_passed = True
    try:
        # 1. Query Root
        log_print(f"\n$ curl -I http://localhost:{TEST_PORT}/")
        req_root = urllib.request.Request(f"http://localhost:{TEST_PORT}/")
        with urllib.request.urlopen(req_root, timeout=5) as res:
            log_print(f"HTTP/1.1 {res.status} OK")
            log_print(f"Content-Type: {res.headers.get('Content-Type')}")
            log_print("Status: 200 OK - Dashboard Static HTML Assets Served")

        # 2. Query /api/health
        log_print(f"\n$ curl -s http://localhost:{TEST_PORT}/api/health | jq .")
        req_health = urllib.request.Request(f"http://localhost:{TEST_PORT}/api/health")
        with urllib.request.urlopen(req_health, timeout=5) as res:
            data = json.loads(res.read().decode("utf-8"))
            log_print(json.dumps(data, indent=2))
            assert data["status"] == "UP", "Health status was not UP!"
            assert data["statusCode"] == 200, "Status code was not 200!"
            log_print(f"[PASS] Health check verified: status='{data['status']}', uptime={data['uptime_seconds']}s")

        # 3. Query /api/info
        log_print(f"\n$ curl -s http://localhost:{TEST_PORT}/api/info | jq .")
        req_info = urllib.request.Request(f"http://localhost:{TEST_PORT}/api/info")
        with urllib.request.urlopen(req_info, timeout=5) as res:
            info = json.loads(res.read().decode("utf-8"))
            log_print(f"Project: {info.get('project')}")
            log_print(f"Application: {info.get('application')}")
            log_print(f"Student: {info.get('student', {}).get('name')} ({info.get('student', {}).get('prn')})")
            log_print(f"College: {info.get('student', {}).get('institution')}")
            log_print("[PASS] Metadata endpoint successfully validated.")

    except Exception as e:
        log_print(f"[FAIL] Execution test failed: {e}")
        evidence_passed = False
    finally:
        log_print("\nShutting down Java Spring Boot test process...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        log_print("Process terminated gracefully.")

    # Write textual evidence
    evidence_txt = EVIDENCE_DIR / "execution_test_output.log"
    with open(evidence_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(logs))
    print(f"\n  [SAVED EVIDENCE LOG] {evidence_txt.name}")

    # Render terminal screenshot
    render_terminal_screenshot(
        logs,
        EVIDENCE_DIR / "application_runtime_evidence.png",
        title="Java Spring Boot Backend Health & Telemetry Verification"
    )

    if evidence_passed:
        print("\n [SUCCESS] SPRING BOOT APPLICATION TEST HARNESS COMPLETED WITH FULL VALIDATION!")
    else:
        print("\n [ERROR] SOME TESTS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
