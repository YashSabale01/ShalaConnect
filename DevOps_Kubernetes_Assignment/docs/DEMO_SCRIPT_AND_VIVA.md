# VIDEO DEMONSTRATION SCRIPT & TECHNICAL VIVA VOCE GUIDE
## IA Activity No. 2: Containerization & Kubernetes Deployment Challenge
**MIT Academy of Engineering, Alandi, Pune**  
**Student:** Yash Janardan Sabale | **PRN:** 2310423T26-27 | **Academic Year:** 2026–2027

---

# PART 1: 5–7 MINUTE VIDEO DEMONSTRATION SCRIPT

This timed script is designed for recording an online video demonstration explaining the containerization, Kubernetes deployment process, and cloud-native concepts.

---

### [00:00 – 00:45] Slide 1: Introduction & Assignment Scope
- **Visual Display:** Title slide displaying Student Name (Yash Janardan Sabale), PRN (2310423T26-27), MIT Academy of Engineering, IA Activity No. 2, and Architecture Overview.
- **Narrator (Speaking):**
  > *"Respected evaluators and peers, greetings. My name is Yash Janardan Sabale, PRN 2310423T26-27, Third Year Computer Engineering at MIT Academy of Engineering, Pune. Today, I am demonstrating my submission for IA Activity No. 2: the Containerization and Kubernetes Deployment Challenge.
  > In this project, I have containerized our educational platform backend, ShalaConnect, developed with Java 21 and Spring Boot 3.2.3, using an optimized multi-stage Docker build. I then deployed it onto a multi-node Kubernetes cluster using declarative manifests with high availability, health probes, rolling updates, and autoscaling. Let us walk through the practical implementation."*

---

### [00:45 – 01:45] Slide 2 & Terminal: Docker Multi-Stage Build & Optimization
- **Visual Display:** Split screen showing `Dockerfile` and terminal executing `docker build` and `docker images`.
- **Terminal Command:**
  ```bash
  cat application/Dockerfile
  docker build -t shalaconnect/backend:2.0.0 -f application/Dockerfile application/
  docker images | grep shalaconnect
  ```
- **Narrator (Speaking):**
  > *"Let us examine the Dockerfile. Instead of using a single build stage that bundles the entire JDK, Maven compiler, and build tools into production, I designed an OCI-compliant multi-stage build.
  > In Stage 1, the builder stage uses Maven on Eclipse Temurin 21 Alpine to compile our source code and package our fat JAR. Notice that we copy `pom.xml` first to cache dependency layers.
  > In Stage 2, our production runtime switches to the lightweight Eclipse Temurin 21 JRE Alpine image. We create a dedicated non-root user `appuser` with UID 10001, adhering to the CIS Docker Benchmark. We inject JVM container flags, `-XX:+UseContainerSupport` and `-XX:MaxRAMPercentage=75.0`, ensuring the JVM respects container cgroup limits.
  > Notice the image size: our final image is just 178 MB, compared to over 780 MB for the build environment—a massive 77.2% reduction that accelerates deployment speeds and eliminates attack vectors."*

---

### [01:45 – 02:30] Terminal: Standalone Container Execution & Verification
- **Visual Display:** Terminal running container and verifying health endpoint.
- **Terminal Command:**
  ```bash
  docker run -d --name shalaconnect-container -p 8080:8080 shalaconnect/backend:2.0.0
  docker ps
  curl -i http://localhost:8080/api/health
  ```
- **Narrator (Speaking):**
  > *"Next, we run the container standalone using `docker run`, mapping host port 8080 to container port 8080. Running `docker ps`, we observe the container status is healthy, validated by our built-in healthcheck instruction.
  > Querying the `/api/health` endpoint via curl, we receive HTTP 200 OK with JSON telemetry showing container uptime, JVM heap memory usage, and active thread pools. Now, let us advance to the Kubernetes orchestration layer."*

---

### [02:30 – 03:45] Terminal & Diagram: Declarative Kubernetes Manifests & Cluster Deployment
- **Visual Display:** Diagram of Kubernetes Cluster Architecture alongside terminal applying manifests.
- **Terminal Command:**
  ```bash
  kubectl get nodes -o wide
  kubectl apply -f k8s/
  kubectl get all -n shalaconnect -o wide
  ```
- **Narrator (Speaking):**
  > *"Here, our Kubernetes v1.29 cluster consists of a control plane and two ready worker nodes.
  > Following cloud-native best practices, our deployment is completely declarative. In our `k8s/` directory, we have defined eight manifests:
  > First, a dedicated `shalaconnect` namespace for multi-tenant isolation.
  > Second, a `ConfigMap` and a `Secret` to decouple application configuration from container images, following Twelve-Factor App principles.
  > Third, our `Deployment` manifest defines a pool of 3 replicas. It specifies container resource requests of 250 millicores of CPU and 256 MiB RAM, with limits set to 1000 millicores and 512 MiB to ensure Burstable Quality of Service without starvation.
  > As you can see from `kubectl get pods -n shalaconnect -o wide`, all 3 pods are in the Running state and distributed across our worker nodes."*

---

### [03:45 – 04:45] Terminal: Kubernetes Health Probes & Service Mesh Routing
- **Visual Display:** Diagram of Pod Probe State Machine and terminal running `kubectl describe` and testing service.
- **Terminal Command:**
  ```bash
  kubectl describe pod -n shalaconnect -l app=shalaconnect-backend | grep -A 8 "Liveness:"
  kubectl get svc -n shalaconnect
  curl -i http://localhost:30080/api/health
  ```
- **Narrator (Speaking):**
  > *"Let us highlight our health probe engineering. In our deployment, we configured three probes:
  > A `startupProbe` that grants the JVM up to 60 seconds of cold-start buffer before triggering restarts.
  > A `readinessProbe` checking `/api/ready` every 5 seconds. If a pod cannot communicate with the database, it is automatically removed from the Service endpoints to prevent 502 Bad Gateway errors.
  > A `livenessProbe` checking `/api/health` every 10 seconds. If a pod deadlocks, Kubelet automatically terminates and recreates it.
  > To expose our application, our `Service` manifest configures a `NodePort` on port 30080, forwarding port 80 to container port 8080. Running `curl http://localhost:30080/api/health`, we see our request successfully load-balanced across our pods, returning HTTP 200 OK."*

---

### [04:45 – 05:45] Terminal & UI: Zero-Downtime Rolling Update & Web Dashboard
- **Visual Display:** Split screen showing live web UI dashboard auto-refreshing while terminal executes a rolling update.
- **Terminal Command:**
  ```bash
  kubectl set image deployment/shalaconnect-backend shalaconnect-microservice=shalaconnect/backend:2.0.1 -n shalaconnect
  kubectl rollout status deployment/shalaconnect-backend -n shalaconnect
  ```
- **Narrator (Speaking):**
  > *"One of the greatest superpowers of Kubernetes is zero-downtime upgrades. Our rolling update strategy specifies `maxSurge: 1` and `maxUnavailable: 0`. 
  > When we update the container image to version 2.0.1, Kubernetes spins up a new pod first. Only after the new pod passes its readiness probe does it terminate an older pod. 
  > Notice on our live web dashboard: continuous client requests are handled without a single failed connection or dropped packet throughout the entire rollout process."*

---

### [05:45 – 06:30] Slide & Conclusion: Summary of Cloud-Native Concepts
- **Visual Display:** Summary slide detailing Key Cloud-Native Pillars Achieved.
- **Narrator (Speaking):**
  > *"To summarize our achievements:
  > 1. We built an optimized, non-root, multi-stage Docker image resulting in a 77% size reduction.
  > 2. We verified standalone container execution with health checks and cgroup memory limits.
  > 3. We deployed a 3-replica declarative Kubernetes Deployment with decoupled ConfigMaps and Secrets.
  > 4. We engineered Startup, Liveness, and Readiness probes for automated self-healing.
  > 5. We proved zero-downtime rolling updates, Horizontal Pod Autoscaling, and service accessibility over NodePort 30080.
  > All source code, manifests, and documentation are committed to our Git repository. Thank you for your time and evaluation."*

---

# PART 2: 30 COMPREHENSIVE TECHNICAL VIVA VOCE QUESTIONS & ANSWERS

### Q1: What is the primary difference between a Docker container and a Virtual Machine?
**Answer:** A Virtual Machine virtualizes physical hardware via a hypervisor (Type-1 or Type-2), requiring a complete guest operating system with its own kernel, system binaries, and drivers. A Docker container virtualizes the operating system using Linux kernel features (Namespaces and cgroups), sharing the host kernel. Containers are orders of magnitude lighter (megabytes vs gigabytes), instantiate in milliseconds, and offer near-bare-metal execution performance.

### Q2: Explain the significance of a multi-stage Dockerfile build.
**Answer:** In single-stage builds, compilers, build toolchains (like Maven and JDK), and intermediate cached files remain in the final image. A multi-stage build defines multiple `FROM` instructions. Early stages handle dependency resolution and compilation, while the final stage copies only the compiled runtime artifact (e.g. fat JAR) into a minimal base image (like JRE Alpine). This drastically reduces the image size (from 782 MB to 178 MB in our case) and eliminates build tools that could be exploited in an attack.

### Q3: Why should containers never run as the `root` user?
**Answer:** By default, the root user inside a container has UID 0, which corresponds to UID 0 on the host Linux kernel. If an attacker achieves Remote Code Execution (RCE) and breaks out of container isolation, they would obtain root-level access over the entire host machine. Creating and enforcing a dedicated non-root user (e.g., `appuser` with UID 10001) adheres to the Principle of Least Privilege and passes CIS Docker Benchmark 4.1.

### Q4: What is the purpose of `.dockerignore`?
**Answer:** The `.dockerignore` file prevents unnecessary files (such as local `.git` history, temporary test logs, build directories like `target/`, and documentation) from being copied into the Docker build context. This speeds up build context transfer to the Docker daemon, accelerates build times, and prevents secret leaks (e.g. `.env` files).

### Q5: How do Linux cgroups (Control Groups) impact Java running in a container?
**Answer:** Historically, Java runtimes prior to Java 8u191 were unaware of container limits and inspected host physical RAM and CPU cores. When a container exceeded its assigned cgroup memory limit, the Linux kernel OOM killer terminated the container abruptly. With modern Java 21, the flags `-XX:+UseContainerSupport` and `-XX:MaxRAMPercentage=75.0` ensure the JVM reads container cgroups directly and sizes heap memory appropriately.

### Q6: What are the primary components of the Kubernetes Control Plane?
**Answer:** 
1. **kube-apiserver:** RESTful gateway and central communication hub for the entire cluster.
2. **etcd:** Distributed, consistent key-value store maintaining all cluster state and configuration.
3. **kube-scheduler:** Matches unscheduled pods to eligible worker nodes based on resource demands and constraints.
4. **kube-controller-manager:** Runs core controller loops (Deployment, ReplicaSet, Node, Namespace) to reconcile current state with desired state.

### Q7: What are the primary components running on a Kubernetes Worker Node?
**Answer:** 
1. **kubelet:** The node agent that communicates with the API server, manages pod lifecycle, and monitors container runtimes.
2. **kube-proxy:** Implements cluster networking and service abstractions by managing iptables or IPVS packet forwarding rules.
3. **Container Runtime (e.g., containerd / CRI-O):** Downloads container images, creates namespaces/cgroups, and executes container processes.

### Q8: What is a Kubernetes Pod, and why not manage containers directly?
**Answer:** A Pod is the smallest deployable computing unit in Kubernetes. It represents a single instance of an application and encapsulates one or more containers that share the same network namespace (IP address and port space), IPC namespace, and storage volumes. Kubernetes manages Pods rather than raw containers to support co-located, co-managed helper patterns (e.g., sidecars, proxies, and log shippers).

### Q9: Differentiate between a Kubernetes Deployment, ReplicaSet, and Pod.
**Answer:** 
- A **Pod** is the running container instance.
- A **ReplicaSet** ensures a specified number of identical Pod replicas are running at any given time.
- A **Deployment** is a higher-level declarative controller that manages ReplicaSets, enabling declarative updates, rollouts, rollbacks, and pause/resume capabilities.

### Q10: What is the difference between a Liveness Probe and a Readiness Probe?
**Answer:** 
- **Liveness Probe:** Detects whether the container is healthy or deadlocked. If a liveness probe fails repeatedly, Kubelet kills the container and initiates a restart according to the `restartPolicy`.
- **Readiness Probe:** Detects whether the container is ready to accept incoming network traffic. If a readiness probe fails, the Pod IP is temporarily removed from the Service Endpoints list so that no traffic is routed to it, but the container is not terminated.

### Q11: What is a Startup Probe and when should it be used?
**Answer:** A `startupProbe` is used for legacy or slow-starting applications (like JVM applications with heavy initialization frameworks) that require extra warm-up time. While the startup probe is executing, it disables both liveness and readiness checks, preventing Kubelet from killing a container while it is still starting up.

### Q12: How does Kubernetes achieve zero-downtime rolling updates?
**Answer:** In the Deployment specification, `strategy.rollingUpdate` defines `maxSurge` (the number of pods that can be created above desired replica count) and `maxUnavailable` (the maximum number of pods that can be unavailable during the update). By setting `maxSurge: 1` and `maxUnavailable: 0`, Kubernetes spins up new pods and waits for their readiness probes to pass before terminating older pods, ensuring uninterrupted client traffic.

### Q13: Explain the difference between Resource Requests and Resource Limits.
**Answer:** 
- **Requests:** The minimum amount of CPU and memory guaranteed to a container. The `kube-scheduler` uses requests to determine which worker node has sufficient capacity to host the Pod.
- **Limits:** The hard maximum ceiling a container is permitted to consume. If a container exceeds its CPU limit, its CPU cycles are throttled. If it exceeds its memory limit, the Linux kernel terminates it with an OOMKilled error (Exit Code 137).

### Q14: What are the three Kubernetes Quality of Service (QoS) classes?
**Answer:** 
1. **Guaranteed:** Every container in the pod has CPU and memory requests equal to limits.
2. **Burstable:** Requests and limits are declared, but requests are lower than limits (as in our ShalaConnect deployment).
3. **BestEffort:** No requests or limits are declared. These pods are the first to be evicted when a node runs out of memory.

### Q15: What is a Kubernetes Service, and why is it needed?
**Answer:** Pods are ephemeral; when they die or scale, their internal IPs change. A Service provides an immutable virtual IP (ClusterIP) and stable DNS name that proxies and load-balances traffic across dynamic sets of Pods identified by label selectors (`app=shalaconnect-backend`).

### Q16: Compare Service types: ClusterIP, NodePort, LoadBalancer, and ExternalName.
**Answer:** 
- **ClusterIP:** Default type; exposes the Service on an internal IP address reachable only within the cluster.
- **NodePort:** Exposes the Service on a static high-range port (30000–32767) across every worker node's external IP address.
- **LoadBalancer:** Integrates with cloud providers (AWS, GCP, Azure) to provision an external hardware/cloud load balancer.
- **ExternalName:** Maps the Service to an external DNS CNAME record without proxying traffic.

### Q17: What is an Ingress Controller, and how does it differ from a NodePort Service?
**Answer:** A NodePort operates at Layer 4 (TCP/UDP) and requires a dedicated high-range port for each service. An Ingress Controller operates at Layer 7 (HTTP/HTTPS) and acts as an intelligent reverse proxy, enabling path-based routing (`/api` vs `/`), host-based virtual hosting (`app.example.com`), and centralized SSL/TLS termination on standard ports 80 and 443.

### Q18: What is a Kubernetes Namespace, and what are its benefits?
**Answer:** A Namespace is a logical virtual cluster partition within a physical Kubernetes cluster. It provides a scope for unique object names, enables multi-tenancy, isolates environments (e.g. dev, staging, prod), and allows administrators to enforce RBAC permissions and `ResourceQuotas`.

### Q19: Explain the difference between a ConfigMap and a Secret.
**Answer:** Both decouple configuration from container code. A **ConfigMap** stores non-sensitive configuration parameters (such as URLs, feature flags, and log levels) in plain text. A **Secret** stores sensitive data (such as passwords, private keys, and API tokens) encoded in Base64 and stored encrypted at rest in `etcd`.

### Q20: What is the Kubernetes Downward API?
**Answer:** The Downward API allows containers to inspect and consume metadata about themselves and the cluster (such as pod name, pod namespace, pod IP, node name, and resource limits) via environment variables or volume files without coupling the application to the Kubernetes client library.

### Q21: What is a Horizontal Pod Autoscaler (HPA), and how does it work?
**Answer:** An HPA automatically scales the number of pod replicas in a Deployment based on observed metrics (such as average CPU utilization or memory usage). The HPA controller queries the `metrics-server` every 15 seconds, computes the required replica count using the formula:
$$\text{DesiredReplicas} = \lceil \text{CurrentReplicas} \times \frac{\text{CurrentMetricValue}}{\text{TargetMetricValue}} \rceil$$
and updates the Deployment replica count accordingly.

### Q22: What is a Pod Disruption Budget (PDB)?
**Answer:** A PDB defines the minimum number or percentage of pods that must remain available during voluntary disruptions, such as administrative node drains (`kubectl drain`), cluster upgrades, or autoscaler downscaling. It prevents planned operations from taking down mission-critical services.

### Q23: How does kube-proxy route traffic to Pods?
**Answer:** `kube-proxy` runs on every node and watches the API server for changes to Services and Endpoints. In modern clusters, it configures Linux `iptables` or `IPVS` (IP Virtual Server) rules that intercept packets destined for the Service's ClusterIP and rewrite the destination IP to one of the healthy Pod backend IPs using random or round-robin selection.

### Q24: What happens if a Pod's memory exceeds its memory limit?
**Answer:** The Linux kernel detects that the container's memory cgroup has exceeded its ceiling. The kernel's Out-Of-Memory (OOM) killer selects and immediately terminates the container process with signal `SIGKILL`. Kubelet detects exit code `137` (`128 + 9 (SIGKILL)`), marks the container as `OOMKilled`, and restarts it according to its `restartPolicy`.

### Q25: What is the difference between `docker stop` and `docker kill`?
**Answer:** `docker stop` sends a `SIGTERM` signal to PID 1 inside the container, granting a default 10-second grace period for the application to finish pending requests, flush caches, and close database connections cleanly before sending `SIGKILL`. `docker kill` immediately sends an uncatchable `SIGKILL` signal, terminating the process abruptly without graceful cleanup.

### Q26: What is a Kubelet and what is its role in container lifecycle?
**Answer:** Kubelet is the node agent that registers the node with the API server. It receives `PodSpecs` from the API server, instructs the container runtime via CRI (Container Runtime Interface) to pull images and start containers, mounts volumes, executes liveness/readiness probes, and reports node and pod status back to the control plane.

### Q27: How does DNS resolution work inside a Kubernetes cluster?
**Answer:** Kubernetes runs CoreDNS inside the `kube-system` namespace. Each Service is assigned an internal Fully Qualified Domain Name (FQDN) in the format `<service-name>.<namespace>.svc.cluster.local`. Pods receive the CoreDNS IP in their `/etc/resolv.conf`, enabling service discovery by service name across namespaces.

### Q28: How does an application achieve graceful termination in Kubernetes?
**Answer:** When a pod is deleted, Kubernetes sets its state to `Terminating` and simultaneously removes it from Service Endpoints and sends `SIGTERM` to the container. The pod is given a `terminationGracePeriodSeconds` (default 30s) to finish in-flight requests and close connections before Kubelet sends `SIGKILL`.

### Q29: What is the significance of the Twelve-Factor App methodology in containerization?
**Answer:** The Twelve-Factor App provides architectural principles for cloud-native applications:
- **Codebase (I):** One codebase tracked in revision control.
- **Dependencies (II):** Explicitly declared and isolated dependencies (Maven, multi-stage Docker).
- **Config (III):** Strict separation of config from code (ConfigMaps, Secrets).
- **Backing Services (IV):** Treat databases/queues as attached resources.
- **Disposability (IX):** Fast startup and graceful shutdown for elastic scalability.

### Q30: What command rollbacks a failed Kubernetes deployment?
**Answer:** `kubectl rollout undo deployment/<deployment-name> -n <namespace>`. To inspect previous deployment revisions and change causes, operators use `kubectl rollout history deployment/<deployment-name> -n <namespace>`.
