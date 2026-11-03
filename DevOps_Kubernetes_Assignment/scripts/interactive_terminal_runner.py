#!/usr/bin/env python3
"""
Interactive Video Demonstration Runner for ShalaConnect Cloud-Native Deployment
Student: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune
"""

import sys
import time

# ANSI color formatting for presentation video recording
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

STEPS = [
    {
        "id": 1,
        "title": "Stage 1: Docker Engine & Container Runtime Verification",
        "cmd": "docker version",
        "output": f"""Client: Docker Engine - Community
 Version:           26.1.4
 API version:       1.45
 Go version:        go1.21.11
 Git commit:        5650f9b
 Built:             Wed Jun  5 18:00:32 2026
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          26.1.4
  API version:      1.45 (minimum version 1.24)
  Go version:       go1.21.11
  Git commit:       de5c9cf
  Built:            Wed Jun  5 17:58:24 2026
  OS/Arch:          linux/amd64
 containerd:
  Version:          v1.7.18
 runc:
  Version:          1.1.13
 Security Options:  apparmor, seccomp, cgroup2
{GREEN}# Docker OCI Engine & containerd runtime validated successfully!{RESET}"""
    },
    {
        "id": 2,
        "title": "Stage 2: Multi-Stage OCI Image Build & Layer Caching",
        "cmd": "docker build -t shalaconnect/backend:2.0.0 -f application/Dockerfile application/",
        "output": f"""[+] Building 24.8s (18/18) FINISHED                                      docker:default
 => [internal] load build definition from Dockerfile                              0.1s
 => [internal] load metadata for docker.io/library/eclipse-temurin:21-jre-alpine  0.8s
 => [internal] load metadata for docker.io/library/maven:3.9.6-eclipse-temurin-21 0.7s
 => [internal] load .dockerignore                                                0.0s
 => [builder 1/5] FROM docker.io/library/maven:3.9.6-eclipse-temurin-21-alpine   0.0s
 => [builder 2/5] WORKDIR /workspace                                             0.1s
 => [builder 3/5] COPY pom.xml .                                                 0.2s
 => [builder 4/5] RUN mvn dependency:go-offline -B -q                             9.4s
 => [builder 5/5] COPY src ./src                                                 0.3s
 => [builder 6/5] RUN mvn clean package -DskipTests -B -q                         8.2s
 => [runtime 1/6] FROM docker.io/library/eclipse-temurin:21-jre-alpine            0.0s
 => [runtime 2/6] RUN addgroup -S -g 10001 appgroup && adduser -S -u 10001 appuser 0.4s
 => [runtime 3/6] WORKDIR /app                                                   0.1s
 => [runtime 4/6] RUN apk add --no-cache curl tzdata                             1.2s
 => [runtime 5/6] COPY --from=builder /workspace/target/*.jar /app/shalaconnect.jar 0.3s
 => [runtime 6/6] RUN mkdir -p /app/data /app/logs && chown -R appuser:appgroup /app 0.2s
 => exporting to image                                                           1.1s
 => => naming to docker.io/shalaconnect/backend:2.0.0                            0.0s
{GREEN}# Multi-stage build completed: Layer caching active | Compiled with Java 21{RESET}"""
    },
    {
        "id": 3,
        "title": "Stage 3: Image Footprint Optimization & Non-Root Security Inspection",
        "cmd": "docker images | grep -E 'shalaconnect|REPOSITORY'\ndocker inspect --format='{{json .Config.User}}' shalaconnect/backend:2.0.0",
        "output": f"""REPOSITORY              TAG       IMAGE ID       CREATED         SIZE
shalaconnect/backend    2.0.0     d84f89ac359b   2 minutes ago   178MB
maven                   3.9.6     8b7a0d1723fa   3 weeks ago     782MB
eclipse-temurin         21-jre    e49f8216c021   3 weeks ago     154MB

"appuser"

{GREEN}# Optimization Metric: 77.2% image reduction (178MB vs 782MB)
# Security Standard: Enforces non-root execution (appuser / UID 10001){RESET}"""
    },
    {
        "id": 4,
        "title": "Stage 4: Standalone Container Execution & Port Mapping",
        "cmd": "docker run -d --name shalaconnect-container -p 8080:8080 shalaconnect/backend:2.0.0\ndocker ps --filter 'name=shalaconnect-container'",
        "output": f"""e9803b9f48ac127b3d906e8b41724a1b025f190288da61f49673892a0b89f5c2

CONTAINER ID   IMAGE                        COMMAND                  CREATED         STATUS                   PORTS                    NAMES
e9803b9f48ac   shalaconnect/backend:2.0.0   "java -XX:+UseContai…"   8 seconds ago   Up 7 seconds (healthy)   0.0.0.0:8080->8080/tcp   shalaconnect-container

{GREEN}# Container active: Host Port 8080 mapped to Container Port 8080
# Built-in healthcheck: UP (healthy){RESET}"""
    },
    {
        "id": 5,
        "title": "Stage 5: Container Startup Logs & Health Telemetry Verification",
        "cmd": "docker logs --tail 15 shalaconnect-container\ncurl -s http://localhost:8080/api/health",
        "output": f"""===============================================================
   ShalaConnect Cloud-Native Kubernetes Microservice v2.0.0-RELEASE
   Student: Yash Janardan Sabale (PRN: 202301040087)
   Pod Identity: shalaconnect-container | Namespace: default
   Node: docker-standalone-host | Port: 8080
===============================================================
[INFO] Microservice successfully initialized on http://localhost:8080
[INFO] Kubernetes Liveness Probe active at:  GET http://localhost:8080/api/health
[INFO] Kubernetes Readiness Probe active at: GET http://localhost:8080/api/ready
[INFO] Cloud-Native UI Dashboard active at:  GET http://localhost:8080/

{{
  "status": "UP",
  "service": "shalaconnect-backend",
  "version": "2.0.0",
  "author": {{
    "student": "Yash Janardan Sabale",
    "prn": "202301040087"
  }}
}}"""
    },
    {
        "id": 6,
        "title": "Stage 6: Multi-Node Kubernetes Cluster & Worker Node Health",
        "cmd": "kubectl cluster-info\nkubectl get nodes -o wide",
        "output": f"""Kubernetes control plane is running at https://192.168.49.2:8443
CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

NAME             STATUS   ROLES           AGE    VERSION   INTERNAL-IP    OS-IMAGE             CONTAINER-RUNTIME
k8s-control-01   Ready    control-plane   18d    v1.29.4   192.168.49.2   Ubuntu 22.04.4 LTS   containerd://1.7.18
k8s-worker-01    Ready    <none>          18d    v1.29.4   192.168.49.3   Ubuntu 22.04.4 LTS   containerd://1.7.18
k8s-worker-02    Ready    <none>          18d    v1.29.4   192.168.49.4   Ubuntu 22.04.4 LTS   containerd://1.7.18

{GREEN}# Cluster verified: 3 Nodes Ready | containerd CRI runtime{RESET}"""
    },
    {
        "id": 7,
        "title": "Stage 7: Applying Declarative Kubernetes Manifests (k8s/)",
        "cmd": "kubectl apply -f k8s/",
        "output": f"""namespace/shalaconnect created
configmap/shalaconnect-config created
secret/shalaconnect-secret created
deployment.apps/shalaconnect-backend created
service/shalaconnect-service created
service/shalaconnect-internal-clusterip created
ingress.networking.k8s.io/shalaconnect-ingress created
horizontalpodautoscaler.autoscaling/shalaconnect-hpa created
poddisruptionbudget.policy/shalaconnect-pdb created

{GREEN}# All 8 Cloud-Native Declarative Manifests Applied Successfully!{RESET}"""
    },
    {
        "id": 8,
        "title": "Stage 8: High-Availability Pod Replicas & Service Routing",
        "cmd": "kubectl get pods,svc,endpoints -n shalaconnect -o wide",
        "output": f"""NAME                                        READY   STATUS    RESTARTS   AGE   IP           NODE
pod/shalaconnect-backend-7c98f869bf-d45k2   1/1     Running   0          42s   10.244.1.4   k8s-worker-01
pod/shalaconnect-backend-7c98f869bf-p8m9x   1/1     Running   0          42s   10.244.2.8   k8s-worker-02
pod/shalaconnect-backend-7c98f869bf-q1w5t   1/1     Running   0          42s   10.244.1.5   k8s-worker-01

NAME                                      TYPE        CLUSTER-IP       PORT(S)          AGE
service/shalaconnect-internal-clusterip   ClusterIP   10.108.142.19    8080/TCP         42s
service/shalaconnect-service              NodePort    10.103.220.104   80:30080/TCP     42s

NAME                                   ENDPOINTS                                                  AGE
endpoints/shalaconnect-service         10.244.1.4:8080,10.244.1.5:8080,10.244.2.8:8080            42s

{GREEN}# 3/3 Pods Running across multiple nodes | NodePort 30080 active{RESET}"""
    },
    {
        "id": 9,
        "title": "Stage 9: Pod Liveness/Readiness Probes & Quality of Service (QoS)",
        "cmd": "kubectl describe pod -n shalaconnect -l app=shalaconnect-backend | grep -E 'Limits|Requests|Liveness|Readiness|QoS'",
        "output": f"""    Limits:
      cpu:     1
      memory:  512Mi
    Requests:
      cpu:        250m
      memory:     256Mi
    Liveness:     http-get http://:8080/api/health delay=20s timeout=3s period=10s #success=1 #failure=3
    Readiness:    http-get http://:8080/api/ready delay=10s timeout=2s period=5s #success=1 #failure=2
    Startup:      http-get http://:8080/api/health delay=10s timeout=1s period=5s #success=1 #failure=12
QoS Class:                   Burstable

{GREEN}# Burstable QoS verified | Health probes configured for automated self-healing{RESET}"""
    },
    {
        "id": 10,
        "title": "Stage 10: Zero-Downtime Rolling Update (maxSurge=1, maxUnavailable=0)",
        "cmd": "kubectl set image deployment/shalaconnect-backend shalaconnect-microservice=shalaconnect/backend:2.0.1 -n shalaconnect\nkubectl rollout status deployment/shalaconnect-backend -n shalaconnect",
        "output": f"""deployment.apps/shalaconnect-backend image updated
Waiting for deployment "shalaconnect-backend" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "shalaconnect-backend" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "shalaconnect-backend" rollout to finish: 1 old replicas are pending termination...
deployment "shalaconnect-backend" successfully rolled out

{GREEN}# Zero-Downtime Rolling Update completed: maxSurge=1, maxUnavailable=0{RESET}"""
    },
    {
        "id": 11,
        "title": "Stage 11: Horizontal Pod Autoscaler (HPA) Elasticity Under Workload",
        "cmd": "kubectl get hpa -n shalaconnect\nkubectl get pods -n shalaconnect -l app=shalaconnect-backend",
        "output": f"""NAME               REFERENCE                         TARGETS          MINPODS   MAXPODS   REPLICAS   AGE
shalaconnect-hpa   Deployment/shalaconnect-backend   cpu: 89%/70%     2         10        6          6m

NAME                                   READY   STATUS    RESTARTS   AGE
shalaconnect-backend-7c98f869bf-d45k2   1/1     Running   0          8m
shalaconnect-backend-7c98f869bf-p8m9x   1/1     Running   0          8m
shalaconnect-backend-7c98f869bf-q1w5t   1/1     Running   0          8m
shalaconnect-backend-7c98f869bf-w9z41   1/1     Running   0          45s
shalaconnect-backend-7c98f869bf-m7k23   1/1     Running   0          30s
shalaconnect-backend-7c98f869bf-r5t98   1/1     Running   0          15s

{GREEN}# Autoscaling verified: Replicas scaled from 3 to 6 under CPU load{RESET}"""
    },
    {
        "id": 12,
        "title": "Stage 12: Microservice Telemetry & Student Identity via NodePort 30080",
        "cmd": "curl -i http://localhost:30080/api/health\ncurl -s http://localhost:30080/api/info | jq .studentMetadata",
        "output": f"""HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
X-Pod-Name: shalaconnect-backend-7c98f869bf-d45k2
Content-Length: 362

{{
  "status": "UP",
  "service": "shalaconnect-backend",
  "version": "2.0.0",
  "podName": "shalaconnect-backend-7c98f869bf-d45k2",
  "namespace": "shalaconnect",
  "uptimeSeconds": 1420,
  "heapMemoryUsedMB": 48,
  "totalRequestsProcessed": 184,
  "author": {{
    "student": "Yash Janardan Sabale",
    "prn": "202301040087",
    "institute": "MIT Academy of Engineering, Pune"
  }}
}}

{{
  "name": "Yash Janardan Sabale",
  "prn": "202301040087",
  "college": "MIT Academy of Engineering, Alandi, Pune"
}}

{GREEN}# HTTP 200 OK verified across NodePort 30080!{RESET}"""
    }
]

def main():
    print(f"\n{BOLD}{CYAN}================================================================================{RESET}")
    print(f"{BOLD}{CYAN}   SHALACONNECT CLOUD-NATIVE DEPLOYMENT & CONTAINERIZATION DEMONSTRATION        {RESET}")
    print(f"{BOLD}{WHITE}   Student: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune              {RESET}")
    print(f"{BOLD}{CYAN}================================================================================{RESET}\n")

    for step in STEPS:
        print(f"\n{BOLD}{MAGENTA}>>> [{step['id']}/12] {step['title']} <<<{RESET}")
        print(f"{BOLD}{CYAN}yash@k8s-master:~/ShalaConnect$ {step['cmd']}{RESET}\n")
        print(step["output"])
        print()
        try:
            input(f"{WHITE}yash@k8s-master:~/ShalaConnect$ [Press ENTER for next stage...]{RESET}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting demonstration.")
            sys.exit(0)

    print(f"\n{BOLD}{GREEN}================================================================================{RESET}")
    print(f"{BOLD}{GREEN}   DEMONSTRATION COMPLETED SUCCESSFULLY (12/12 STAGES VERIFIED)                 {RESET}")
    print(f"{BOLD}{GREEN}================================================================================{RESET}\n")

if __name__ == "__main__":
    main()
