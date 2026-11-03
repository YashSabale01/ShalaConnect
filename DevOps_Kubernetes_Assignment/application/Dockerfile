# ==============================================================================
# Enterprise Cloud-Native Dockerfile: ShalaConnect Microservice
# Application: ShalaConnect Educational Web API (Spring Boot 3.2.3 / Java 21)
# Student: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune
# ==============================================================================
# Multi-Stage Build Architecture for Security, Immutability & Minimal Attack Surface
# Stage 1: Dependency resolution and compiled artifact packaging
# Stage 2: Distroless-style Alpine JRE hardened runtime image (< 180 MB)
# ==============================================================================

# ------------------------------------------------------------------------------
# STAGE 1: Build & Packaging Environment (JDK 21 + Maven)
# ------------------------------------------------------------------------------
FROM maven:3.9.6-eclipse-temurin-21-alpine AS builder

LABEL maintainer="Yash Janardan Sabale <yash.sabale@mitaoe.ac.in>"
LABEL stage="builder"
LABEL description="Compilation & packaging stage for ShalaConnect Spring Boot microservice"

WORKDIR /workspace

# Step 1.1: Cache Maven dependencies layer
# By copying only pom.xml first, Docker caches downloaded dependencies across builds
COPY pom.xml .
RUN mvn dependency:go-offline -B -q

# Step 1.2: Copy application source code and compile
COPY src ./src
RUN mvn clean package -DskipTests -B -q

# ------------------------------------------------------------------------------
# STAGE 2: Hardened, Non-Root Production Runtime (Alpine JRE 21)
# ------------------------------------------------------------------------------
FROM eclipse-temurin:21-jre-alpine AS runtime

LABEL maintainer="Yash Janardan Sabale <yash.sabale@mitaoe.ac.in>"
LABEL description="Production runtime container for ShalaConnect Cloud-Native Pod"
LABEL version="2.0.0"

# Step 2.1: Create non-root system user and group (Least Privilege Security Principle)
# Enforces CIS Docker Benchmark 4.1 (Run as non-root user)
RUN addgroup -S -g 10001 appgroup && \
    adduser -S -u 10001 -G appgroup -s /sbin/nologin appuser

WORKDIR /app

# Step 2.2: Install minimal operational utilities for health checks
RUN apk add --no-cache curl tzdata && \
    rm -rf /var/cache/apk/*

# Set default container timezone
ENV TZ=Asia/Kolkata
ENV SPRING_PROFILES_ACTIVE=prod
ENV SERVER_PORT=8080

# Step 2.3: Copy compiled fat JAR artifact from builder stage
COPY --from=builder /workspace/target/*.jar /app/shalaconnect-app.jar

# Step 2.4: Create application data / uploads directory with strict ownership
RUN mkdir -p /app/data /app/logs && \
    chown -R appuser:appgroup /app && \
    chmod 750 /app

# Switch to unprivileged runtime user
USER appuser

# Expose microservice HTTP port
EXPOSE 8080

# Step 2.5: Container-level Healthcheck for Docker standalone orchestration
# In Kubernetes, kubelet probes (readiness/liveness) take precedence
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Step 2.6: JVM Container Memory Limits and Signal Handling
# Uses cgroup memory constraints (-XX:+UseContainerSupport) to avoid OOMKills
ENTRYPOINT ["java", \
    "-XX:+UseContainerSupport", \
    "-XX:MaxRAMPercentage=75.0", \
    "-XX:InitialRAMPercentage=50.0", \
    "-XX:+ExitOnOutOfMemoryError", \
    "-Djava.security.egd=file:/dev/./urandom", \
    "-jar", "/app/shalaconnect-app.jar"]
