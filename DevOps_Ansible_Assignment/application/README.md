# ShalaConnect Backend Application Artifact
## Java 21 / Spring Boot 3.2.3 Microservice

This directory contains the core application code deployed by Ansible.

### Project Files
- **`pom.xml`**: Maven Project Object Model file defining Spring Boot 3.2.3 dependencies, OpenJDK 21 compiler specifications, and build plugins.
- **`ShalaConnectBackendServer.java`**: Standalone executable Spring Boot application containing REST endpoints, embedded health probes (`/api/health`), and telemetry logging.

### Building the Executable JAR
To compile and package the standalone fat JAR artifact locally or in your CI/CD pipeline:

```bash
# From this directory:
mvn clean package -DskipTests
```

This generates `shalaconnect-backend-1.0.0.jar`, which Ansible picks up and distributes to target nodes under `/opt/shalaconnect-app/`.
