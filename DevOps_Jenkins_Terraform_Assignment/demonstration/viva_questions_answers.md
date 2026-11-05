# Comprehensive Viva-Voce Questions & Expert Answers
## IA Activity No. 3: Jenkins CI/CD + Terraform Mini Project
**Course:** DevOps & Cloud Engineering | **Department:** Computer Engineering | **MITAOE Pune**  
**Student:** Yash Janardan Sabale | **PRN:** 202301040087  

---

### Section 1: Jenkins & Continuous Integration / Continuous Deployment (CI/CD)

#### Q1: What is the fundamental difference between Declarative and Scripted Jenkins Pipelines?
**Answer:**  
- **Declarative Pipeline:** Introduced in Jenkins 2.x, it uses a strict, structured, and opinionated syntax enclosed in a `pipeline { ... }` block. It offers pre-defined sections (`stages`, `stage`, `steps`, `post`, `environment`, `options`), simpler syntax validation before execution, and clean visualization in Jenkins Blue Ocean and Stage View.
- **Scripted Pipeline:** Written in Groovy as a free-form DSL wrapped in a `node { ... }` block. While highly flexible and allowing arbitrary procedural programming (loops, conditionals, exception handling), it lacks declarative structure and is harder to maintain and audit.

#### Q2: Why is the `Jenkinsfile` placed in the root of the source code repository?
**Answer:**  
Placing the `Jenkinsfile` in the root repository adheres to **Pipeline as Code** (PaC) principles. This ensures:
1. Version control of the build and deployment lifecycle alongside application code.
2. Branch-specific pipelines (different branches can test different pipeline features).
3. Auditability, traceability, and peer-review of infrastructure and deployment changes via pull requests.

#### Q3: How does Jenkins integrate with GitHub? What triggers the pipeline execution?
**Answer:**  
Integration is accomplished using the **Jenkins Git Plugin** and GitHub credentials (Personal Access Token or SSH keys). Pipeline triggers can be configured via:
1. **GitHub Webhooks (Push / Pull Request events):** GitHub instantly notifies the Jenkins URL (`http://<jenkins-url>/github-webhook/`) upon commit push.
2. **Poll SCM:** Configured with a cron expression (e.g., `H/5 * * * *` to check for new commits every 5 minutes if webhooks cannot reach private networks).
3. **Manual Trigger:** Parametrized execution via the Jenkins web interface.

#### Q4: What is the purpose of the `post` block in a Jenkinsfile?
**Answer:**  
The `post` block defines actions that execute automatically after pipeline stages complete. Common conditions include:
- `always`: Runs regardless of build outcome (e.g., publishing JUnit test reports via `junit`, workspace cleanup via `cleanWs()`).
- `success`: Executes only if all stages pass (e.g., deployment notifications to Slack, archiving artifacts).
- `failure`: Triggers alerts and notification emails to developers when a build breaks.
- `changed`: Fires when the build state changes from failure to success or vice versa.

#### Q5: How did you handle secrets and credentials in your Jenkins pipeline?
**Answer:**  
Secrets (such as Docker Hub credentials, AWS access keys, and GitHub access tokens) are stored securely in the **Jenkins Credential Store** using AES-256 encryption. Within the `Jenkinsfile`, credentials are bound safely using environment blocks:
```groovy
withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
}
```
This prevents secrets from being exposed in plain text in version control or console logs.

#### Q6: What is DevSecOps, and how is it integrated into your Jenkins pipeline?
**Answer:**  
DevSecOps shifts security left into the early phases of the CI/CD pipeline. In our pipeline:
1. **Static Analysis & Linting:** Maven Compile, Checkstyle, and SpotBugs verify source code quality and check for known vulnerabilities.
2. **Container Security Audit (Trivy):** Before pushing or deploying the container image, Trivy scans OS packages and JAR dependencies for HIGH and CRITICAL Common Vulnerabilities and Exposures (CVEs), halting the build if security thresholds are breached.

---

### Section 2: Terraform & Infrastructure as Code (IaC)

#### Q7: What is Infrastructure as Code (IaC) and what problems does it solve?
**Answer:**  
Infrastructure as Code manages and provisions cloud infrastructure through machine-readable definition files rather than manual console interaction or interactive configuration tools. It solves:
1. **Configuration Drift:** Eliminates discrepancies between staging and production environments.
2. **Human Error:** Removes manual misconfigurations and missed security settings.
3. **Speed & Consistency:** Provisions complex multi-tier environments in minutes with deterministic accuracy.
4. **Version Control & Collaboration:** Enables team code reviews and rollbacks through Git.

#### Q8: Explain the core workflow commands of Terraform (`init`, `validate`, `plan`, `apply`, `destroy`).
**Answer:**  
- `terraform init`: Initializes the working directory, downloads required provider plugins (e.g., `hashicorp/aws`), and configures the backend.
- `terraform validate`: Verifies the syntax, internal consistency, and schema validity of HCL configuration files.
- `terraform plan`: Performs a dry-run comparing existing state with the desired state, generating an execution plan detailing resources to be added (+), modified (~), or destroyed (-).
- `terraform apply`: Applies the changes required to reach the desired state by calling cloud provider APIs.
- `terraform destroy`: Safely tears down and deletes all resources tracked in the Terraform state file.

#### Q9: What is the Terraform State file (`terraform.tfstate`), and why is remote backend locking necessary?
**Answer:**  
The state file records the mapping between declared HCL resources and real-world infrastructure provisioned in the cloud, along with metadata and resource dependencies.  
In an enterprise team setting:
- **Remote Backend (Amazon S3):** Stores the state file centrally with encryption at rest so multiple team members access the single source of truth.
- **State Locking (Amazon DynamoDB):** Prevents simultaneous conflicting applies by acquiring an exclusive lock during `plan` and `apply`, preventing state corruption.

#### Q10: What are Terraform Modules and why did you structure your infrastructure into modules?
**Answer:**  
A Terraform module is a container for multiple resources that are used together. Structuring infrastructure into modules provides:
1. **Reusability:** The VPC or database module can be instantiated repeatedly across staging and production.
2. **Encapsulation:** Hides implementation complexity behind defined input variables and output values.
3. **Maintainability:** Logical separation into `vpc`, `security`, `database`, and `compute` modules allows teams to modify networking without risking database changes.

#### Q11: How do your security groups ensure the principle of least privilege?
**Answer:**  
Our security architecture follows a three-tier defense-in-depth model:
1. **ALB Security Group:** Allows inbound HTTP (port 80) and HTTPS (port 443) from `0.0.0.0/0`.
2. **Application Security Group:** Rejects all direct internet access. Ingress is strictly allowed on port 8080 from the ALB Security Group ID (`security_groups = [aws_security_group.alb.id]`).
3. **Database Security Group:** Ingress on PostgreSQL port 5432 is strictly restricted to traffic originating from the Application Security Group (`security_groups = [aws_security_group.app.id]`).

#### Q12: How does Jenkins coordinate with Terraform during the automated release?
**Answer:**  
In Stage 7 of the `Jenkinsfile`:
1. Jenkins enters the `terraform/` directory.
2. It executes `terraform init` and `terraform validate`.
3. It generates an environment-specific plan: `terraform plan -var="environment=${params.DEPLOY_ENV}" -out=tfplan`.
4. For staging, it automatically applies `tfplan`.
5. It extracts output values (`alb_dns_name`, `rds_endpoint`) via `terraform output -raw` and injects them into downstream container deployment configurations.
