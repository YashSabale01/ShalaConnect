# ShalaConnect: Cloud-Native Containerization & Kubernetes Deployment

## Project Overview
This repository contains the production-grade cloud-native containerization and multi-node Kubernetes orchestration deployment for the **ShalaConnect Educational Platform** backend microservice (Java 21 / Spring Boot 3.2.3).

---

### Student & Academic Details
- **Student Name:** Yash Janardan Sabale
- **Permanent Registration Number (PRN):** 202301040087
- **Department:** Department of Computer Engineering
- **Institution:** MIT Academy of Engineering, Alandi, Pune

---

## What We Covered & Implemented

### 1. Application Architecture & Microservice Runtime
- High-concurrency educational web API built with **Java 21 LTS** and **Spring Boot 3.2.3**.
- Employs **Virtual Threads (Project Loom)** for lightweight concurrent request handling.
- Exposes RESTful domain endpoints (`/api/students`), dynamic telemetry (`/api/metrics`), health indicators (`/api/health`, `/api/ready`, `/api/info`), and an interactive Web Dashboard (`/`).

### 2. Multi-Stage OCI Containerization
- **Stage 1 (Builder):** Uses `maven:3.9.6-eclipse-temurin-21-alpine` to compile source code and package a self-contained executable fat JAR. Implements layer caching by resolving dependencies (`pom.xml`) prior to copying application source.
- **Stage 2 (Hardened Runtime):** Switches to a minimal `eclipse-temurin:21-jre-alpine` runtime image, copying exclusively the compiled JAR artifact.
- **Image Footprint Reduction:** Final production image size is **178 MB**, achieving a **77.2% reduction** compared to the 782 MB build environment.
- **Security Hardening (CIS Docker Benchmark 4.1):** Enforces an unprivileged non-root user (`appuser` with UID `10001`) with disabled login shell (`/sbin/nologin`).
- **Container Cgroup Sizing:** Configured JVM memory constraints (`-XX:+UseContainerSupport`, `-XX:MaxRAMPercentage=75.0`, `-XX:+ExitOnOutOfMemoryError`) ensuring the JVM heap adapts dynamically to container memory limits without OOMKilled terminations.
- **Container Healthcheck:** Built-in Docker `HEALTHCHECK` directive continuously probing `/api/health`.

### 3. Declarative Kubernetes Orchestration
- **Namespace Isolation:** Dedicated `shalaconnect` namespace for logical separation and RBAC multi-tenancy.
- **Decoupled Configurations (12-Factor App):**
  - **`ConfigMap` (`shalaconnect-config`):** Injects non-sensitive environment variables (profiles, ports, database hosts, log levels).
  - **`Secret` (`shalaconnect-secret`):** Safely injects base64-encrypted database passwords, JWT signing keys, and tokens into container environments.
- **High-Availability Deployment (3 Replicas):** Manages 3 identical pod replicas scheduled across worker nodes to prevent single-point-of-failure outages.
- **Zero-Downtime Rolling Update Strategy:**
  - `maxSurge: 1`: Spins up new pod instances before terminating older replicas.
  - `maxUnavailable: 0`: Guarantees 100% capacity and zero dropped client requests throughout rollouts.
- **Resource Limits & Quality of Service (QoS):**
  - `requests`: 250m CPU, 256Mi RAM (guaranteed reservation).
  - `limits`: 1000m CPU, 512Mi RAM (hard ceiling preventing noisy-neighbor starvation).
  - Assigns **Burstable** QoS class.

### 4. Self-Healing Health Probes Engineering
- **Startup Probe (`/api/health`):** Grants the JVM up to 60 seconds of cold-start initialization buffer before liveness checks begin, preventing restart loops.
- **Readiness Probe (`/api/ready`):** Evaluates dependency readiness every 5 seconds. Automatically removes unready pod IPs from Service endpoints to prevent 502/503 errors.
- **Liveness Probe (`/api/health`):** Evaluates container vitality every 10 seconds. Automatically restarts deadlocked or hung containers via Kubelet.

### 5. Service Networking & External Exposure
- **NodePort Service (`shalaconnect-service`):** Exposes internal container port 8080 across all cluster worker nodes via static **NodePort 30080** and cluster port 80.
- **ClusterIP Service (`shalaconnect-internal-clusterip`):** Provides internal East-West cluster communication.
- **Dynamic Endpoint Discovery:** `kube-proxy` continuously registers healthy pod IP addresses (`10.244.x.x`) into Service Endpoints.
- **Ingress Controller Routing (`shalaconnect-ingress`):** Layer-7 HTTP routing mapping `shalaconnect.mitaoe.local` to backend services.

### 6. Elastic Autoscaling & Disruption Budgets
- **Horizontal Pod Autoscaler (HPA):** Monitors CPU and memory utilization. Automatically scales pod replicas from **2 (min) to 10 (max)** when average CPU utilization breaches 70%.
- **Pod Disruption Budget (PDB):** Enforces `minAvailable: 2`, ensuring at least two pods remain online during planned node drains or cluster maintenance.

### 7. Authentic Verification & Execution Artifacts
- **12 Verified Terminal Artifacts:** Demonstrating Docker builds, container execution, Kubernetes node health, manifest application, pod status, probes, rolling updates, HPA load scaling, and cURL telemetry.
- **4 High-Resolution (300 DPI) Architecture Diagrams:** Detailing Docker multi-stage builds, Kubernetes cluster topology, GitOps CI/CD delivery pipeline, and the probe state machine.
- **Live HTTP 200 Telemetry:** Verified responses across `/api/health`, `/api/ready`, `/api/info`, and `/api/metrics`.

---

## 📁 Repository Structure

```
DevOps_Kubernetes_Assignment/
├── README.md                                          # Master Project Documentation & Summary
├── DevOps_IA2_Containerization_Kubernetes_Report_Yash_Sabale.pdf   # Academic PDF Report
├── DevOps_IA2_Containerization_Kubernetes_Report_Yash_Sabale.docx  # Editable Academic Word Report
│
├── application/                                       # Application Source & Docker Packaging
│   ├── Dockerfile                                     # Production multi-stage Dockerfile
│   ├── .dockerignore                                  # Build context exclusion rules
│   ├── docker-compose.yml                             # Multi-container local stack (App + PostgreSQL + Nginx)
│   ├── pom.xml                                        # Maven project descriptor
│   ├── ShalaConnectApplication.java                   # Standalone Java 21 / Spring Boot microservice
│   └── public/                                        # Cloud-native interactive dashboard UI
│       ├── index.html                                 # Dashboard markup & telemetry counters
│       ├── style.css                                  # Dark-mode styling
│       └── app.js                                     # Real-time health poller
│
├── k8s/                                               # Declarative Kubernetes Manifests
│   ├── 00-namespace.yaml                              # Dedicated namespace definition
│   ├── 01-configmap.yaml                              # Decoupled environment configuration
│   ├── 02-secret.yaml                                 # Encrypted credentials & tokens
│   ├── 03-deployment.yaml                             # 3-replica deployment with health probes & limits
│   ├── 04-service.yaml                                # NodePort (30080) & ClusterIP service definitions
│   ├── 05-ingress.yaml                                # Layer-7 HTTP Ingress route
│   ├── 06-hpa.yaml                                    # Horizontal Pod Autoscaler (2 to 10 replicas)
│   ├── 07-pdb.yaml                                    # Pod Disruption Budget (minAvailable: 2)
│   └── kustomization.yaml                             # Kustomize single-command deployment bundle
│
├── diagrams/                                          # Publication-Grade Architecture Visualizations
│   ├── docker_multistage_architecture.png             # Multi-stage build & security layers
│   ├── kubernetes_cluster_architecture.png            # Control plane, worker nodes, pods & service mesh
│   ├── cloud_native_gitops_pipeline.png               # GitOps continuous delivery & telemetry loop
│   └── pod_lifecycle_and_probes.png                   # Probe state machine (Startup, Ready, Live)
│
├── screenshots/
│   └── execution_evidence/                            # Verified CLI execution screenshots (12 Artifacts)
│       ├── 01_docker_version.png                      # Docker Engine & Client verification
│       ├── 02_docker_build_multistage.png             # Multi-stage image build execution
│       ├── 03_docker_images_inspection.png            # 178 MB image inspection & non-root user
│       ├── 04_docker_run_container.png                # Container run & port 8080 mapping
│       ├── 05_docker_health_and_logs.png              # Container health status (healthy) & stdout logs
│       ├── 06_kubectl_cluster_info.png                # Multi-node Kubernetes cluster & node status
│       ├── 07_kubectl_apply_manifests.png             # Declarative manifest application
│       ├── 08_kubectl_get_pods_services.png           # 3/3 Pods running & NodePort 30080 active
│       ├── 09_kubectl_describe_pod_probes.png         # Liveness/Readiness probes & QoS resource limits
│       ├── 10_kubectl_rolling_update.png              # Zero-downtime rolling update & rollout history
│       ├── 11_kubectl_hpa_autoscaling.png             # Horizontal Pod Autoscaler scaling under workload
│       ├── 12_curl_service_telemetry.png              # Microservice HTTP 200 telemetry probe
│       └── execution_test_output.log                  # Raw terminal execution log file
│
└── docs/                                              # In-Depth Technical Documentation
    ├── Kubernetes_Case_Study.md                       # Comprehensive 25-section academic case study
    ├── Cloud_Native_Architecture.md                   # System design, namespaces & cgroup primitives
    ├── Kubernetes_Deployment_Guide.md                 # Step-by-step operational runbook
    ├── DEMO_RECORDING_SCRIPT.md                       # 5-8 minute natural video presentation script
    └── DEMO_SCRIPT_AND_VIVA.md                        # Technical script and 30 Viva Voce questions & answers
```
