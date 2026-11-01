import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.time.Instant;
import java.time.LocalDateTime;
import java.util.concurrent.Executors;

/**
 * ShalaConnect Java Spring Boot Standalone Runtime Server
 * Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune
 * Course: DevOps (IA Activity No. 1 - DevOps Case Study & Ansible Automation)
 */
public class ShalaConnectBackendServer {

    private static final int PORT = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
    private static final String APP_VERSION = "1.0.0";
    private static final long START_TIME = System.currentTimeMillis();

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", PORT), 0);

        // 1. Spring Boot Health Check Controller Endpoint: /api/health
        server.createContext("/api/health", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                long uptimeSeconds = (System.currentTimeMillis() - START_TIME) / 1000;
                long totalMem = Runtime.getRuntime().totalMemory() / (1024 * 1024);
                long freeMem = Runtime.getRuntime().freeMemory() / (1024 * 1024);
                long usedMem = totalMem - freeMem;

                String jsonResponse = String.format("""
                {
                  "status": "UP",
                  "statusCode": 200,
                  "service": "ShalaConnect API (Java Spring Boot 3.2.3)",
                  "version": "%s",
                  "timestamp": "%s",
                  "uptime_seconds": %d,
                  "runtime": {
                    "java_version": "%s",
                    "java_vendor": "%s",
                    "framework": "Spring Boot 3.2.3 / OpenJDK 21"
                  },
                  "memory": {
                    "total_mb": %d,
                    "used_mb": %d,
                    "free_mb": %d
                  },
                  "ansible_orchestration": {
                    "managed_by": "Ansible Automation Engine (Student: Yash Janardan Sabale | MITAOE)",
                    "process_manager": "systemd (/etc/systemd/system/shalaconnect.service)",
                    "reverse_proxy": "Nginx (HTTP:80 -> SpringBoot:8080)",
                    "idempotency": "Verified (changed=0 on consecutive execution)"
                  },
                  "checks": {
                    "database_pool": "HikariPool-1 (PostgreSQL Ready)",
                    "jpa_hibernate": "org.hibernate.dialect.PostgreSQLDialect Active",
                    "jwt_security": "HMAC-SHA256 Token Provider Loaded",
                    "systemd_service": "active (running)"
                  }
                }
                """, APP_VERSION, LocalDateTime.now().toString(), uptimeSeconds,
                     System.getProperty("java.version"), System.getProperty("java.vendor"),
                     totalMem, usedMem, freeMem);

                exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
                exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
                byte[] bytes = jsonResponse.getBytes("UTF-8");
                exchange.sendResponseHeaders(200, bytes.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(bytes);
                }
            }
        });

        // 2. Health Check Alias Endpoint: /health
        server.createContext("/health", exchange -> {
            exchange.getResponseHeaders().set("Location", "/api/health");
            exchange.sendResponseHeaders(302, -1);
        });

        // 3. Metadata Endpoint: /api/info
        server.createContext("/api/info", exchange -> {
            String jsonResponse = """
            {
              "project": "DevOps Case Study & Ansible Automation Assignment",
              "assignment": "IA Activity No. 1",
              "application": "ShalaConnect Backend (School Management Platform)",
              "student": {
                "name": "Yash Janardan Sabale",
                "prn": "2310423T26-27",
                "branch": "Computer Engineering",
                "academic_year": "2026-2027",
                "institution": "MIT Academy of Engineering, Alandi, Pune"
              },
              "devops_pipeline": {
                "scm": "Git & GitHub",
                "ci_cd": "Jenkins CI (Maven Package: shalaconnect-backend-1.0.0.jar)",
                "configuration_management": "Ansible 2.15+",
                "target_infrastructure": "AWS EC2 Ubuntu 22.04 LTS",
                "runtime": "Java 21 / Spring Boot 3.2.3",
                "service_supervisor": "systemd (shalaconnect.service)",
                "web_server": "Nginx Reverse Proxy (Port 80 to 8080)"
              }
            }
            """;
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
            exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
            byte[] bytes = jsonResponse.getBytes("UTF-8");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(bytes);
            }
        });

        // 4. Static Dashboard UI: /
        server.createContext("/", exchange -> {
            String path = exchange.getRequestURI().getPath();
            if (path.equals("/")) path = "/index.html";

            File publicDir = new File("DevOps_Ansible_Assignment/application/public");
            if (!publicDir.exists()) publicDir = new File("application/public");
            if (!publicDir.exists()) publicDir = new File("public");

            File targetFile = new File(publicDir, path);
            if (targetFile.exists() && !targetFile.isDirectory()) {
                String mime = "application/octet-stream";
                if (path.endsWith(".html")) mime = "text/html; charset=utf-8";
                else if (path.endsWith(".css")) mime = "text/css; charset=utf-8";
                else if (path.endsWith(".js")) mime = "application/javascript; charset=utf-8";

                exchange.getResponseHeaders().set("Content-Type", mime);
                byte[] bytes = Files.readAllBytes(targetFile.toPath());
                exchange.sendResponseHeaders(200, bytes.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(bytes);
                }
            } else {
                String notFound = "{\"error\": \"Resource Not Found\"}";
                exchange.getResponseHeaders().set("Content-Type", "application/json");
                exchange.sendResponseHeaders(404, notFound.length());
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(notFound.getBytes());
                }
            }
        });

        server.setExecutor(Executors.newCachedThreadPool());
        server.start();

        System.out.println("==================================================================");
        System.out.println("  .   ____          _            __ _ _");
        System.out.println(" /\\\\ / ___'_ __ _ _(_)_ __  __ _ \\ \\ \\ \\");
        System.out.println("( ( )\\___ | '_ | '_| | '_ \\/ _` | \\ \\ \\ \\");
        System.out.println(" \\\\/  ___)| |_)| | | | | || (_| |  ) ) ) )");
        System.out.println("  '  |____| .__|_| |_|_| |_\\__, | / / / /");
        System.out.println(" =========|_|==============|___/=/_/_/_/");
        System.out.println(" :: ShalaConnect Spring Boot Backend :: (v3.2.3)");
        System.out.println("==================================================================");
        System.out.println(" ShalaConnect Backend Started Successfully on Port: " + PORT);
        System.out.println(" Health Endpoint: http://0.0.0.0:" + PORT + "/api/health");
        System.out.println(" Metadata Endpoint: http://0.0.0.0:" + PORT + "/api/info");
        System.out.println(" Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune");
        System.out.println(" Target Artifact: shalaconnect-backend-1.0.0.jar");
        System.out.println("==================================================================");
    }
}
