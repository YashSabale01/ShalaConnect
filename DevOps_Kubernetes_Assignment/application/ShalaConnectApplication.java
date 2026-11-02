package com.shalaconnect;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.OperatingSystemMXBean;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.time.Instant;
import java.time.format.DateTimeFormatter;
import java.util.UUID;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicLong;

/**
 * ==============================================================================
 * ShalaConnect Cloud-Native Microservice & Kubernetes Demonstration Server
 * Course: DevOps & Cloud Engineering (IA Activity 2)
 * Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune
 * ==============================================================================
 * Features:
 * 1. Low-footprint, cloud-native Java 21 HTTP microservice.
 * 2. Implements Kubernetes Liveness & Readiness Probes (/api/health, /api/ready).
 * 3. Real-time telemetry, pod identity, and JVM container cgroup metrics (/api/metrics).
 * 4. Interactive visual dashboard served at root (/).
 * 5. Fully compatible with Docker containers, Pod scaling, and Service routing.
 */
public class ShalaConnectApplication {

    private static final String APP_VERSION = "2.0.0-RELEASE";
    private static final String STUDENT_NAME = "Yash Janardan Sabale";
    private static final String STUDENT_PRN = "2310423T26-27";
    private static final Instant START_TIME = Instant.now();
    private static final AtomicLong REQUEST_COUNTER = new AtomicLong(0);

    public static void main(String[] args) throws IOException {
        int port = 8080;
        String portEnv = System.getenv("SERVER_PORT");
        if (portEnv != null && !portEnv.isBlank()) {
            try {
                port = Integer.parseInt(portEnv.trim());
            } catch (NumberFormatException ignored) {}
        }

        String podName = System.getenv().getOrDefault("HOSTNAME", "shalaconnect-pod-" + UUID.randomUUID().toString().substring(0, 8));
        String nodeName = System.getenv().getOrDefault("NODE_NAME", "k8s-worker-node-01");
        String namespace = System.getenv().getOrDefault("POD_NAMESPACE", "shalaconnect");

        System.out.println("===============================================================");
        System.out.println("   ShalaConnect Cloud-Native Kubernetes Microservice v" + APP_VERSION);
        System.out.println("   Student: " + STUDENT_NAME + " (PRN: " + STUDENT_PRN + ")");
        System.out.println("   Pod Identity: " + podName + " | Namespace: " + namespace);
        System.out.println("   Node: " + nodeName + " | Port: " + port);
        System.out.println("===============================================================");

        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", port), 0);

        server.createContext("/", new DashboardHandler(podName, nodeName, namespace));
        server.createContext("/api/health", new HealthHandler(podName, namespace));
        server.createContext("/api/ready", new ReadyHandler());
        server.createContext("/api/info", new InfoHandler(podName, nodeName, namespace));
        server.createContext("/api/metrics", new MetricsHandler());
        server.createContext("/api/students", new StudentsHandler());

        server.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
        server.start();

        System.out.println("[INFO] Microservice successfully initialized on http://0.0.0.0:" + port);
        System.out.println("[INFO] Kubernetes Liveness Probe active at:  GET http://0.0.0.0:" + port + "/api/health");
        System.out.println("[INFO] Kubernetes Readiness Probe active at: GET http://0.0.0.0:" + port + "/api/ready");
        System.out.println("[INFO] Cloud-Native UI Dashboard active at:  GET http://0.0.0.0:" + port + "/");
    }

    private static class HealthHandler implements HttpHandler {
        private final String podName;
        private final String namespace;

        public HealthHandler(String podName, String namespace) {
            this.podName = podName;
            this.namespace = namespace;
        }

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            REQUEST_COUNTER.incrementAndGet();
            MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
            long heapUsed = memoryBean.getHeapMemoryUsage().getUsed() / (1024 * 1024);
            long heapMax = memoryBean.getHeapMemoryUsage().getMax() / (1024 * 1024);
            long uptimeSeconds = (Instant.now().toEpochMilli() - START_TIME.toEpochMilli()) / 1000;

            String jsonResponse = String.format(
                "{\n" +
                "  \"status\": \"UP\",\n" +
                "  \"service\": \"shalaconnect-backend\",\n" +
                "  \"version\": \"%s\",\n" +
                "  \"podName\": \"%s\",\n" +
                "  \"namespace\": \"%s\",\n" +
                "  \"uptimeSeconds\": %d,\n" +
                "  \"heapMemoryUsedMB\": %d,\n" +
                "  \"heapMemoryMaxMB\": %d,\n" +
                "  \"totalRequestsProcessed\": %d,\n" +
                "  \"timestamp\": \"%s\",\n" +
                "  \"author\": {\n" +
                "    \"student\": \"%s\",\n" +
                "    \"prn\": \"%s\",\n" +
                "    \"institute\": \"MIT Academy of Engineering, Pune\"\n" +
                "  }\n" +
                "}",
                APP_VERSION, podName, namespace, uptimeSeconds, heapUsed, heapMax,
                REQUEST_COUNTER.get(), DateTimeFormatter.ISO_INSTANT.format(Instant.now()),
                STUDENT_NAME, STUDENT_PRN
            );

            byte[] bytes = jsonResponse.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
            exchange.getResponseHeaders().set("X-Pod-Name", podName);
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        }
    }

    private static class ReadyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            REQUEST_COUNTER.incrementAndGet();
            String response = "{\"status\":\"READY\",\"probe\":\"KubernetesReadinessProbe\",\"code\":200}";
            byte[] bytes = response.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        }
    }

    private static class InfoHandler implements HttpHandler {
        private final String podName;
        private final String nodeName;
        private final String namespace;

        public InfoHandler(String podName, String nodeName, String namespace) {
            this.podName = podName;
            this.nodeName = nodeName;
            this.namespace = namespace;
        }

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            REQUEST_COUNTER.incrementAndGet();
            String hostIp = "127.0.0.1";
            try {
                hostIp = InetAddress.getLocalHost().getHostAddress();
            } catch (Exception ignored) {}

            String jsonResponse = String.format(
                "{\n" +
                "  \"application\": \"ShalaConnect Cloud-Native Educational Platform\",\n" +
                "  \"description\": \"Containerization and Kubernetes Deployment Challenge (IA2)\",\n" +
                "  \"version\": \"%s\",\n" +
                "  \"runtime\": \"OpenJDK 21 - Alpine Linux Container\",\n" +
                "  \"kubernetes\": {\n" +
                "    \"pod\": \"%s\",\n" +
                "    \"node\": \"%s\",\n" +
                "    \"namespace\": \"%s\",\n" +
                "    \"podIp\": \"%s\"\n" +
                "  },\n" +
                "  \"studentMetadata\": {\n" +
                "    \"name\": \"%s\",\n" +
                "    \"prn\": \"%s\",\n" +
                "    \"course\": \"DevOps & Cloud Engineering (2310423T26-27)\",\n" +
                "    \"college\": \"MIT Academy of Engineering, Alandi, Pune\"\n" +
                "  }\n" +
                "}",
                APP_VERSION, podName, nodeName, namespace, hostIp, STUDENT_NAME, STUDENT_PRN
            );

            byte[] bytes = jsonResponse.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        }
    }

    private static class MetricsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            REQUEST_COUNTER.incrementAndGet();
            OperatingSystemMXBean osBean = ManagementFactory.getOperatingSystemMXBean();
            MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
            int availableProcessors = osBean.getAvailableProcessors();
            double systemLoad = osBean.getSystemLoadAverage();
            long heapUsed = memoryBean.getHeapMemoryUsage().getUsed();
            long heapCommitted = memoryBean.getHeapMemoryUsage().getCommitted();
            long nonHeapUsed = memoryBean.getNonHeapMemoryUsage().getUsed();
            int threadCount = ManagementFactory.getThreadMXBean().getThreadCount();

            String metrics = String.format(
                "{\n" +
                "  \"cpuCores\": %d,\n" +
                "  \"systemLoadAverage\": %.2f,\n" +
                "  \"jvmHeapUsedBytes\": %d,\n" +
                "  \"jvmHeapCommittedBytes\": %d,\n" +
                "  \"jvmNonHeapUsedBytes\": %d,\n" +
                "  \"liveThreadCount\": %d,\n" +
                "  \"httpRequestsTotal\": %d\n" +
                "}",
                availableProcessors, systemLoad, heapUsed, heapCommitted, nonHeapUsed, threadCount, REQUEST_COUNTER.get()
            );

            byte[] bytes = metrics.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        }
    }

    private static class StudentsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            REQUEST_COUNTER.incrementAndGet();
            String json = "[\n" +
                "  {\"id\": 101, \"name\": \"Aarav Sharma\", \"grade\": \"10th\", \"status\": \"Active\", \"school\": \"Pune Model Public School\"},\n" +
                "  {\"id\": 102, \"name\": \"Diya Deshmukh\", \"grade\": \"10th\", \"status\": \"Active\", \"school\": \"Pune Model Public School\"},\n" +
                "  {\"id\": 103, \"name\": \"Rohan Patil\", \"grade\": \"9th\", \"status\": \"Active\", \"school\": \"Alandi English Medium High\"},\n" +
                "  {\"id\": 104, \"name\": \"Ananya Kulkarni\", \"grade\": \"10th\", \"status\": \"Active\", \"school\": \"MIT Higher Secondary\"}\n" +
                "]";

            byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        }
    }

    private static class DashboardHandler implements HttpHandler {
        private final String podName;
        private final String nodeName;
        private final String namespace;

        public DashboardHandler(String podName, String nodeName, String namespace) {
            this.podName = podName;
            this.nodeName = nodeName;
            this.namespace = namespace;
        }

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String path = exchange.getRequestURI().getPath();
            if ("/style.css".equals(path)) {
                serveStaticFile(exchange, "style.css", "text/css");
                return;
            } else if ("/app.js".equals(path)) {
                serveStaticFile(exchange, "app.js", "application/javascript");
                return;
            }

            REQUEST_COUNTER.incrementAndGet();
            File htmlFile = new File("public/index.html");
            String html;
            if (htmlFile.exists()) {
                html = Files.readString(htmlFile.toPath(), StandardCharsets.UTF_8);
                html = html.replace("{{POD_NAME}}", podName)
                           .replace("{{NODE_NAME}}", nodeName)
                           .replace("{{NAMESPACE}}", namespace)
                           .replace("{{STUDENT_NAME}}", STUDENT_NAME)
                           .replace("{{STUDENT_PRN}}", STUDENT_PRN)
                           .replace("{{APP_VERSION}}", APP_VERSION);
            } else {
                html = getFallbackHtml(podName, nodeName, namespace);
            }

            byte[] bytes = html.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        }

        private void serveStaticFile(HttpExchange exchange, String filename, String contentType) throws IOException {
            File f = new File("public/" + filename);
            if (f.exists()) {
                byte[] data = Files.readAllBytes(f.toPath());
                exchange.getResponseHeaders().set("Content-Type", contentType);
                exchange.sendResponseHeaders(200, data.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(data);
                }
            } else {
                exchange.sendResponseHeaders(404, -1);
            }
        }

        private String getFallbackHtml(String pod, String node, String ns) {
            return "<!DOCTYPE html><html><head><title>ShalaConnect Kubernetes Pod</title>" +
                   "<style>body{font-family:system-ui,sans-serif;background:#0f172a;color:#f8fafc;padding:40px;text-align:center;}" +
                   ".card{background:#1e293b;max-width:600px;margin:auto;padding:30px;border-radius:12px;border:1px solid #334155;}" +
                   ".badge{background:#10b981;color:#fff;padding:6px 14px;border-radius:20px;font-weight:bold;display:inline-block;margin-bottom:15px;}" +
                   "</style></head><body><div class='card'>" +
                   "<div class='badge'>Pod Status: Active (Running)</div>" +
                   "<h1>ShalaConnect Microservice</h1>" +
                   "<p><strong>Student:</strong> " + STUDENT_NAME + " | <strong>PRN:</strong> " + STUDENT_PRN + "</p>" +
                   "<hr style='border:0;border-top:1px solid #334155;margin:20px 0;'>" +
                   "<p><strong>Pod:</strong> <code>" + pod + "</code></p>" +
                   "<p><strong>Node:</strong> <code>" + node + "</code></p>" +
                   "<p><strong>Namespace:</strong> <code>" + ns + "</code></p>" +
                   "<p><strong>Health Endpoint:</strong> <a href='/api/health' style='color:#38bdf8;'>/api/health</a></p>" +
                   "</div></body></html>";
        }
    }
}
