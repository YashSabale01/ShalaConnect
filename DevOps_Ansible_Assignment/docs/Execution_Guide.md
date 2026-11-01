# PRACTICAL EXECUTION & VERIFICATION GUIDE
## Step-by-Step Instructions for Control Node & Managed Servers (Java Spring Boot)
**Student:** Yash Janardan Sabale | **PRN:** 2310423T26-27 | **MIT Academy of Engineering, Pune**

---

### Prerequisites & Supported Environments

This automation suite supports:
1. **Ubuntu / Debian Linux** (Native or Cloud EC2 Virtual Machines)
2. **Windows 11 with WSL2 (Ubuntu 22.04 LTS / 24.04 LTS)**
3. **Localhost Development & Testing Mode**

---

### Step 1: Setting Up the Ansible Control Node

#### On Linux / WSL2:
```bash
# Update local package manager
sudo apt update && sudo apt install -y python3 python3-pip git curl openjdk-21-jdk maven

# Install Ansible Core
sudo apt install -y ansible

# Verify installation
ansible --version
java -version
```

#### On Windows (Local Testing Mode):
Python 3.10+ and Java 21+ are required:
```powershell
python scripts/validate_playbooks.py
python scripts/test_local_app.py
```

---

### Step 2: Configuring SSH Access for AWS EC2 Instances

1. Place your private SSH key in `~/.ssh/shalaconnect-key.pem`:
```bash
chmod 400 ~/.ssh/shalaconnect-key.pem
```

2. Open `inventory/inventory.ini` and update the public IP address:
```ini
[aws_ec2]
ec2-app-prod-01 ansible_host=<YOUR_AWS_EC2_PUBLIC_IP> ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/shalaconnect-key.pem
```

3. For local or WSL testing, use `inventory/inventory_local.ini`:
```ini
[local_dev]
localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3
```

---

### Step 3: Verifying Connectivity (Ansible Ping)

```bash
# Ping local environment
ansible all -i inventory/inventory_local.ini -m ping

# Expected Output:
# localhost | SUCCESS => {
#     "changed": false,
#     "ping": "pong"
# }

# Ping AWS EC2 cloud instance
ansible all -i inventory/inventory.ini -m ping
```

---

### Step 4: Syntax Check & Static Code Validation

```bash
# 1. Ansible native syntax check
ansible-playbook playbooks/site.yml --syntax-check

# 2. Complete project validation suite
python3 scripts/validate_playbooks.py
```

---

### Step 5: Full Playbook Execution

Execute the master provisioning and deployment playbook:

```bash
ansible-playbook -i inventory/inventory.ini playbooks/site.yml
```

To run against local/WSL environment:
```bash
ansible-playbook -i inventory/inventory_local.ini playbooks/site.yml
```

---

### Step 6: Verifying Idempotency

Re-run the playbook immediately:
```bash
ansible-playbook -i inventory/inventory.ini playbooks/site.yml
```
**Expected Result:** The `PLAY RECAP` must show `changed=0`, proving zero configuration drift.

---

### Step 7: Verifying Application Health & Endpoints

Query the HTTP endpoints to verify runtime status:

```bash
# 1. Spring Boot health check telemetry endpoint
curl -i http://<TARGET_IP>:8080/api/health

# 2. Nginx reverse proxy endpoint
curl -i http://<TARGET_IP>:80/api/health

# 3. Project metadata endpoint
curl -s http://<TARGET_IP>:8080/api/info | jq .

# 4. View systemd service status on target machine
sudo systemctl status shalaconnect

# 5. Inspect real-time logs
sudo journalctl -u shalaconnect -f
```

---

### Step 8: Running the Local Interactive Web Dashboard

To preview the application dashboard in your local browser:

```powershell
python scripts/test_local_app.py
```
Open your browser and navigate to:
- `http://localhost:8085` — Live Interactive Dashboard
- `http://localhost:8085/api/health` — Spring Boot JSON Health Telemetry
- `http://localhost:8085/api/info` — Project Metadata & Student Details
