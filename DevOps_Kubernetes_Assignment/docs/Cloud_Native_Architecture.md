# CLOUD-NATIVE ARCHITECTURAL SPECIFICATION & SYSTEM DESIGN
## Technical Architecture Deep Dive: ShalaConnect on Kubernetes
**MIT Academy of Engineering, Pune | Department of Computer Engineering**  
**Student:** Yash Janardan Sabale | **PRN:** 2310423T26-27

---

## 1. ARCHITECTURAL OVERVIEW

The ShalaConnect cloud-native infrastructure is structured around four primary decoupled planes:
1. **Developer Workstation & CI Layer:** Git, Maven build caching, and Docker BuildKit multi-stage packaging.
2. **Container Registry Layer:** OCI-compliant image distribution with cryptographic SHA-256 layer hashing.
3. **Kubernetes Control Plane:** Declarative API reconciliation, scheduler bin-packing, and etcd cluster state.
4. **Data Plane (Worker Nodes):** Pod sandbox isolation, CNI overlay networking, Kube-proxy packet translation, and container cgroup throttling.

```
                    +--------------------------------------------+
                    |        External Client / Web Browser       |
                    +--------------------------------------------+
                                          |
                                          v (Port 80 / 443)
                    +--------------------------------------------+
                    |           NGINX Ingress Controller         |
                    |           (Layer 7 Path/Host Router)       |
                    +--------------------------------------------+
                                          |
                                          v
                    +--------------------------------------------+
                    |     Kubernetes Service (NodePort 30080)    |
                    |      IPVS / iptables Load Balancer         |
                    +--------------------------------------------+
                             /            |            \
                            /             |             \
                           v              v              v
                  +---------------+---------------+---------------+
                  |  Backend Pod  |  Backend Pod  |  Backend Pod  |
                  |   Replica 1   |   Replica 2   |   Replica 3   |
                  |  (10.244.1.4) |  (10.244.2.8) |  (10.244.1.5) |
                  |  Java 21 JRE  |  Java 21 JRE  |  Java 21 JRE  |
                  +---------------+---------------+---------------+
                           \              |              /
                            \             |             /
                             +------------+------------+
                                          |
                                          v (Port 5432)
                    +--------------------------------------------+
                    |          PostgreSQL 16 Database            |
                    |         (PersistentVolumeClaim)            |
                    +--------------------------------------------+
```

---

## 2. LINUX CONTAINER ISOLATION PRIMITIVES

The container engine creates isolated environments using standard Linux kernel features:

### 2.1 Linux Namespaces Applied
- **PID Namespace:** The Spring Boot application runs as PID 1 inside the container, isolated from processes running on the host OS or other containers.
- **NET Namespace:** Each pod receives a dedicated virtual network interface (`eth0`) with its own IP address (`10.244.x.x`), route table, and port bindings.
- **MNT Namespace:** Mount points inside the container are isolated. The root filesystem (`/`) is backed by read-only container image layers.
- **IPC Namespace:** Prevents shared memory segments or message queues from being accessed outside the pod sandbox.
- **UTS Namespace:** Provides an independent hostname for the container (`HOSTNAME=shalaconnect-backend-xxx`).
- **USER Namespace:** Maps internal UID 10001 (`appuser`) to an unprivileged UID range on the host.

### 2.2 Linux Cgroups (v2) Resource Throttling
- `cpu.weight` and `cpu.max`: Enforce CPU requests (`250m`) and limits (`1000m`). Under contention, the Linux Completely Fair Scheduler (CFS) allocates bandwidth proportional to shares.
- `memory.min` and `memory.max`: Guarantee `256Mi` reservation and terminate processes with `SIGKILL` if allocation exceeds `512Mi`.

---

## 3. NETWORKING MODEL & IP ASSIGNMENT (CNI)

Kubernetes enforces the **Container Network Interface (CNI)** standard with three fundamental rules:
1. All Pods can communicate with all other Pods without NAT.
2. All Nodes can communicate with all Pods (and vice-versa) without NAT.
3. The IP that a Pod sees itself as is the same IP that that other Pods see it as.

In our deployment:
- **Pod CIDR:** `10.244.0.0/16`
- **Service ClusterIP CIDR:** `10.96.0.0/12`
- **NodePort Range:** `30000-32767` (ShalaConnect allocated `30080`)

Traffic arriving at any node on port 30080 is intercepted by `kube-proxy` iptables rules, which perform DNAT (Destination Network Address Translation) and forward packets directly to one of the Pod IPs.

---

## 4. SECURITY HARDENING MATRIX

| Attack Vector | Vulnerability | Mitigation in ShalaConnect |
| :--- | :--- | :--- |
| **Container Breakout** | Root user inside container gains root on host OS | Enforced non-root user `appuser` (UID 10001) in both Dockerfile and `securityContext`. |
| **Privilege Escalation** | Sudo / Setuid binary exploits | `allowPrivilegeEscalation: false` in `PodSpec`. |
| **Kernel Exploits** | Malicious syscalls to Linux kernel | Dropped all Linux capabilities: `capabilities.drop: ["ALL"]`. |
| **Credential Theft** | Secrets checked into Git repository | Injected at runtime via Kubernetes `Secret` and `ConfigMap`. |
| **Host Starvation** | Runaway memory leak takes down node | Enforced strict `limits.memory: 512Mi` and `limits.cpu: 1000m`. |
| **OOM Inadvertent Kill** | JVM unaware of container memory ceiling | Configured `-XX:+UseContainerSupport` and `-XX:MaxRAMPercentage=75.0`. |
