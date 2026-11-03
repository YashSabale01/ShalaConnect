# COMPLETE KUBERNETES DEPLOYMENT & OPERATIONAL GUIDE
## Practical Execution Manual for IA Activity No. 2
**MIT Academy of Engineering, Pune | Department of Computer Engineering**  
**Student:** Yash Janardan Sabale | **PRN:** 2310423T26-27

---

## 1. PREREQUISITES & ENVIRONMENT SETUP

Ensure the following tools are installed on your workstation or cloud VM:
- **Docker Engine:** v24.0+ / v26.1+
- **Kubectl CLI:** v1.28+ / v1.29+
- **Kubernetes Cluster:** Minikube, Kind, K3s, MicroK8s, or AWS EKS / GCP GKE
- **Java Development Kit:** OpenJDK 21 LTS (optional for local running)
- **cURL & jq:** For testing HTTP endpoints and parsing JSON telemetry

Verify your toolchain:
```bash
docker version
kubectl version --client
```

---

## 2. DOCKER CONTAINERIZATION STEP-BY-STEP

### Step 2.1: Inspect the Project Directory
```bash
cd DevOps_Kubernetes_Assignment
ls -la application/
```

### Step 2.2: Build the Multi-Stage Production Image
```bash
docker build -t shalaconnect/backend:2.0.0 -f application/Dockerfile application/
```

### Step 2.3: Verify Built Image & Security Characteristics
```bash
docker images | grep shalaconnect
docker inspect --format='{{json .Config.User}}' shalaconnect/backend:2.0.0
```
Expected output:
- Size: ~178 MB
- Configured User: `"appuser"` (UID 10001)

### Step 2.4: Execute Standalone Container
```bash
docker run -d \
  --name shalaconnect-container \
  -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=prod \
  -e STUDENT_NAME="Yash Janardan Sabale" \
  -e STUDENT_PRN="202301040087" \
  shalaconnect/backend:2.0.0
```

### Step 2.5: Verify Container Health & Logs
```bash
docker ps --filter "name=shalaconnect-container"
docker logs --tail 20 shalaconnect-container
curl -i http://localhost:8080/api/health
```

### Step 2.6: Stop & Clean Up Standalone Container
```bash
docker stop shalaconnect-container
docker rm shalaconnect-container
```

---

## 3. KUBERNETES CLUSTER DEPLOYMENT

### Step 3.1: Verify Cluster Connectivity
```bash
kubectl cluster-info
kubectl get nodes -o wide
```

### Step 3.2: Deploy All Manifests
Deploy using standard `kubectl apply`:
```bash
kubectl apply -f k8s/
```
Or deploy using Kustomize:
```bash
kubectl apply -k k8s/
```

### Step 3.3: Verify Namespace & Config Creation
```bash
kubectl get namespaces | grep shalaconnect
kubectl get configmap,secret -n shalaconnect
```

### Step 3.4: Verify High-Availability Pods & Services
```bash
kubectl get pods -n shalaconnect -o wide
kubectl get svc -n shalaconnect
kubectl get endpoints -n shalaconnect shalaconnect-service
```
Expected output:
- 3/3 Pods in `Running` status.
- `shalaconnect-service` type `NodePort` on port `30080`.
- 3 Pod IPs listed under endpoints.

### Step 3.5: Inspect Health Probes and QoS Configuration
```bash
kubectl describe pod -n shalaconnect -l app=shalaconnect-backend | grep -E "Liveness|Readiness|Limits|Requests|QoS"
```

---

## 4. SERVICE TESTING & ENDPOINT VERIFICATION

### Step 4.1: Test via NodePort (Port 30080)
If using Minikube:
```bash
minikube service shalaconnect-service -n shalaconnect --url
```
Or directly via node IP:
```bash
curl -i http://localhost:30080/api/health
curl -s http://localhost:30080/api/info | jq .
curl -s http://localhost:30080/api/metrics | jq .
curl -s http://localhost:30080/api/students | jq .
```

### Step 4.2: Port Forwarding (Alternative Access)
```bash
kubectl port-forward -n shalaconnect svc/shalaconnect-service 8080:80
```
Open in browser: `http://localhost:8080/` to view the live Web Dashboard.

---

## 5. ZERO-DOWNTIME ROLLING UPDATE & ROLLBACK

### Step 5.1: Trigger Rolling Update
Update the container image to version 2.0.1:
```bash
kubectl set image deployment/shalaconnect-backend \
  shalaconnect-microservice=shalaconnect/backend:2.0.1 \
  -n shalaconnect --record=true
```

### Step 5.2: Watch Rollout Progress
```bash
kubectl rollout status deployment/shalaconnect-backend -n shalaconnect
```

### Step 5.3: Verify Rollout History
```bash
kubectl rollout history deployment/shalaconnect-backend -n shalaconnect
```

### Step 5.4: Test Rollback (If Needed)
```bash
kubectl rollout undo deployment/shalaconnect-backend -n shalaconnect
```

---

## 6. AUTOSCALING (HPA) VALIDATION UNDER LOAD

### Step 6.1: Check Initial HPA Status
```bash
kubectl get hpa -n shalaconnect
```

### Step 6.2: Generate Simulated Load
Using `ab` (ApacheBench) or a bash loop:
```bash
# Generate 10,000 requests with 50 concurrent workers
ab -n 10000 -c 50 http://localhost:30080/api/health
```

### Step 6.3: Observe Dynamic Pod Scaling
```bash
kubectl get hpa -n shalaconnect --watch
kubectl get pods -n shalaconnect -l app=shalaconnect-backend
```
Expected output: Replicas will scale up from 3 towards 6–10 pods based on CPU consumption.

---

## 7. CLUSTER CLEANUP

To delete all resources when testing is finished:
```bash
kubectl delete -f k8s/
# or
kubectl delete namespace shalaconnect
```
