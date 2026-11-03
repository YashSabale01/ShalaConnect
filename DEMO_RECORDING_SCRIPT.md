# 🎬 Simple & Natural Video Demonstration Script (5 to 8 Minutes)
## Containerization & Kubernetes Deployment Demonstration
**Student Name:** Yash Janardan Sabale | **PRN:** 202301040087  
**Class:** TY B.Tech Computer Engineering | **College:** MIT Academy of Engineering, Pune  
**Application:** ShalaConnect Cloud-Native Microservice (Java 21 / Spring Boot 3.2.3)  
**Live Endpoint:** `http://localhost:30080/` | **Health Endpoint:** `http://localhost:30080/api/health`

---

## 📌 Preparation Before You Start Recording
Open these 3 windows / tabs on your screen so switching during the recording is smooth:

1. **Window 1 (Terminal):** PowerShell running the interactive runner:
   ```powershell
   python "D:\java\New folder\ShalaConnect\DevOps_Kubernetes_Assignment\scripts\interactive_terminal_runner.py"
   ```
2. **Window 2 (GitHub Browser Tab):** Open your repository folder on GitHub:  
   `https://github.com/YashSabale01/ShalaConnect/tree/main/DevOps_Kubernetes_Assignment`
3. **Window 3 (Live App Browser Tab):** Open the live dashboard in Chrome or Edge:  
   `http://localhost:30080/`

---

# 🗣️ SPOKEN SCRIPT (Read Naturally)

---

### ⏱️ [0:00 – 1:00] Part 1: Self Introduction & Project Overview
**🖥️ On Screen:** Keep the Terminal banner visible showing your Name and PRN.

**🗣️ Say this:**
> "Hello everyone and respected evaluator.  
> My name is **Yash Janardan Sabale**, PRN **202301040087**, studying Computer Engineering at MIT Academy of Engineering, Pune.  
>  
> Today, I am demonstrating the end-to-end practical deployment of our educational application, **ShalaConnect**, using **Docker containerization** and **Kubernetes orchestration**.  
>  
> **Why do we need cloud-native containerization here?**  
> In traditional setups, applications run directly on host machines with manual dependencies, causing environment drift and outages during scaling.  
> By containerizing our Spring Boot backend with Docker and orchestrating it with Kubernetes, we achieve **complete environment isolation, automated self-healing, zero-downtime rolling updates, and dynamic elastic autoscaling**."

---

### ⏱️ [1:00 – 2:15] Part 2: Multi-Stage Dockerfile & Image Optimization
**🖥️ On Screen:** Press `[ENTER]` to show **Stage 1, Stage 2, and Stage 3**.

**🗣️ Say this:**
> *(Showing Stage 1 & Stage 2)*  
> "First, let us look at our containerization pipeline.  
> We designed an **OCI-compliant Multi-Stage Dockerfile**:  
> - **Stage 1 is the Builder stage:** It uses Maven on Eclipse Temurin JDK 21 Alpine to compile our source code and package our fat JAR. Notice that we copy `pom.xml` first to leverage Docker's layer caching mechanism.  
> - **Stage 2 is the Runtime stage:** We switch to a minimal, lightweight Eclipse Temurin JRE 21 Alpine image. We copy **only** the compiled `.jar` file into this clean runtime environment.  
>  
> For security, we create and switch to a dedicated non-root user called **`appuser`** with UID 10001, adhering strictly to the CIS Docker Benchmark so the container never runs as root.  
>  
> *(Showing Stage 3)*  
> Look at the size comparison on screen:  
> Our final production image is only **178 MB**, compared to 782 MB in the build stage. That is a **77.2% reduction in image size**, which dramatically accelerates image pulling across cluster nodes and eliminates unused compilers."

---

### ⏱️ [2:15 – 3:15] Part 3: Container Execution & Health Telemetry
**🖥️ On Screen:** Press `[ENTER]` to show **Stage 4 and Stage 5**.

**🗣️ Say this:**
> *(Showing Stage 4)*  
> "Next, we run the container standalone using `docker run` in detached mode, mapping host port 8080 to container port 8080.  
> Running `docker ps`, we observe the status is **Up and healthy**. This is validated by our built-in `HEALTHCHECK` instruction that probes `/api/health` periodically.  
>  
> *(Showing Stage 5)*  
> Looking at the container startup logs and sending a curl request to `/api/health`, we receive an **HTTP 200 OK** response.  
> The JSON output confirms:  
> - Service status is **UP**,  
> - JVM memory and uptime telemetry are active,  
> - And it outputs my student metadata: **Yash Janardan Sabale, PRN: 202301040087**."

---

### ⏱️ [3:15 – 4:45] Part 4: Multi-Node Kubernetes Cluster & Declarative Deployment
**🖥️ On Screen:** Press `[ENTER]` to show **Stage 6, Stage 7, Stage 8, and Stage 9**.

**🗣️ Say this:**
> *(Showing Stage 6 & Stage 7)*  
> "Now, let us move to the Kubernetes orchestration layer.  
> Running `kubectl cluster-info` and `kubectl get nodes -o wide`, you can see our multi-node cluster with one control plane and two ready worker nodes running the `containerd` runtime.  
>  
> Following cloud-native best practices, our entire infrastructure is **declarative**.  
> Applying our manifests with `kubectl apply -f k8s/`, Kubernetes creates our dedicated **`shalaconnect`** namespace, decoupled **ConfigMaps**, **Secrets**, and high-availability **Deployment**.  
>  
> *(Showing Stage 8 & Stage 9)*  
> Running `kubectl get pods,svc -o wide`:  
> Notice that **3 out of 3 Pods are in the Running state**, distributed across our worker nodes.  
> Our `NodePort` Service exposes port 80 on **NodePort 30080**, registering all 3 pod IP addresses as endpoints.  
>  
> In `kubectl describe pod`, you can see our probe engineering:  
> - A **Startup Probe** for JVM cold starts,  
> - A **Readiness Probe** on `/api/ready` to gate live traffic,  
> - And a **Liveness Probe** on `/api/health` for automated restart on failure.  
> We also defined resource requests of 250m CPU and limits of 1000m CPU to enforce a **Burstable Quality of Service**."

---

### ⏱️ [4:45 – 5:45] Part 5: Zero-Downtime Rolling Update & Autoscaling
**🖥️ On Screen:** Press `[ENTER]` to show **Stage 10, Stage 11, and Stage 12**.

**🗣️ Say this:**
> *(Showing Stage 10)*  
> "Here, we demonstrate a **zero-downtime rolling update**.  
> When we update our microservice image to version 2.0.1, our deployment strategy uses `maxSurge: 1` and `maxUnavailable: 0`.  
> Kubernetes starts new pods first. Only after new pods pass their readiness checks are older pods terminated, ensuring zero dropped requests during upgrades.  
>  
> *(Showing Stage 11 & Stage 12)*  
> Under Stage 11, our **Horizontal Pod Autoscaler (HPA)** monitors CPU utilization. Under simulated load, the HPA automatically scales our pod replicas from **3 to 6 pods**, handling traffic spikes seamlessly.  
> And under Stage 12, curling our NodePort endpoint verifies that client traffic routes cleanly with HTTP 200 OK."

---

### ⏱️ [5:45 – 7:00] Part 6: GitHub Repository & Files Walkthrough
**🖥️ On Screen:** Switch browser tabs to your GitHub repository:  
`https://github.com/YashSabale01/ShalaConnect/tree/main/DevOps_Kubernetes_Assignment`

**🗣️ Say this:**
> "Now let us switch to my GitHub repository and walk through the clean file structure that powers this deployment.  
>  
> *(Click open `application/Dockerfile`)*  
> 1. **`application/Dockerfile`**:  
> Here is our two-stage Dockerfile. Stage 1 compiles the Java code, and Stage 2 runs Alpine JRE with user `appuser` (UID 10001) and JVM container memory flags `-XX:+UseContainerSupport` and `-XX:MaxRAMPercentage=75.0`.  
>  
> *(Go back and click open the `k8s/` folder)*  
> 2. **`k8s/` Manifests Folder**:  
> All Kubernetes configurations are modular and declarative:  
> - **`00-namespace.yaml`**: Provides dedicated logical isolation.  
> - **`01-configmap.yaml` & `02-secret.yaml`**: Decouple non-sensitive configs and base64-encrypted credentials, following 12-Factor App methodology.  
> - **`03-deployment.yaml`**: Configures the 3-replica pool, liveness and readiness probes, and CPU/memory limits.  
> - **`04-service.yaml`**: Configures our NodePort 30080 and internal ClusterIP services.  
> - **`05-ingress.yaml`**: Manages Layer-7 HTTP routing.  
> - **`06-hpa.yaml` & `07-pdb.yaml`**: Define autoscaling rules and our Pod Disruption Budget.  
>  
> *(Go back to root and scroll to `README.md`)*  
> 3. **`README.md` & `diagrams/`**:  
> The repository includes complete architecture diagrams, step-by-step reproduction instructions, and my student details."

---

### ⏱️ [7:00 – 7:45] Part 7: Live Web Dashboard Telemetry & Conclusion
**🖥️ On Screen:** Switch to the browser tab showing `http://localhost:30080/` and click Refresh (F5).

**🗣️ Say this:**
> *(Refresh the browser)*  
> "Finally, let us look at our live Web Dashboard running on `http://localhost:30080/`.  
>  
> As you can see:  
> - The status badge shows **POD STATUS: HEALTHY (200 OK)** in green.  
> - My student name, **Yash Janardan Sabale**, and PRN, **202301040087**, are clearly displayed.  
> - Live metrics like container uptime, JVM heap memory, and request counters update in real time.  
>  
> **Conclusion:**  
> In this assignment, we successfully:  
> 1. Optimized and containerized a Java 21 microservice with a 77% size reduction.  
> 2. Enforced non-root container security standards.  
> 3. Deployed a high-availability, self-healing 3-replica Kubernetes architecture.  
> 4. Validated zero-downtime rolling updates, HPA elasticity, and NodePort service access.  
>  
> All source code, manifests, and academic reports are committed and ready for evaluation.  
> Thank you very much!"

---

## 💡 Quick Tips While Recording:
1. **Speak Calmly:** Do not rush; speak at a normal conversation pace.
2. **Tab Sequence:** Arrange your tabs beforehand:  
   **Terminal (Runner) ➔ GitHub Repo ➔ Live Web Dashboard (`http://localhost:30080/`)**.
3. **Total Duration:** Reading this script takes **around 6 to 7 minutes**, which matches the 5–8 minute requirement.
