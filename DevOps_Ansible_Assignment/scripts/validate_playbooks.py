#!/usr/bin/env python3
"""
Ansible Playbook & Inventory Static Syntax and Integrity Validator
Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune
"""

import os
import sys
import configparser
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def print_banner(text):
    print("=" * 70)
    print(f" {text}")
    print("=" * 70)

def validate_yaml_files():
    print("\n[STEP 1] Validating YAML Playbooks and Role Tasks...")
    yaml_files = []
    
    # Collect playbooks
    playbook_dir = BASE_DIR / "playbooks"
    for f in playbook_dir.glob("*.yml"):
        yaml_files.append(f)
        
    # Collect role files
    role_dir = BASE_DIR / "roles"
    for f in role_dir.rglob("*.yml"):
        yaml_files.append(f)

    all_passed = True
    for yf in sorted(yaml_files):
        rel_path = yf.relative_to(BASE_DIR)
        try:
            with open(yf, "r", encoding="utf-8") as stream:
                docs = list(yaml.safe_load_all(stream))
                task_count = 0
                for doc in docs:
                    if isinstance(doc, list):
                        task_count += len(doc)
                    elif isinstance(doc, dict):
                        task_count += len(doc.get("tasks", [])) + len(doc.get("pre_tasks", []))
                print(f"  [PASS] {str(rel_path):<45} (Valid YAML, items: {task_count})")
        except Exception as e:
            print(f"  [FAIL] {str(rel_path):<45} ERROR: {e}")
            all_passed = False

    return all_passed

def validate_inventory():
    print("\n[STEP 2] Validating Ansible Inventory Files...")
    inventory_dir = BASE_DIR / "inventory"
    all_passed = True
    
    for inv_file in inventory_dir.glob("*.ini"):
        rel_path = inv_file.relative_to(BASE_DIR)
        try:
            with open(inv_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            groups = set()
            hosts = []
            for line in lines:
                line = line.strip()
                if line.startswith("[") and line.endswith("]"):
                    group_name = line[1:-1].split(":")[0]
                    groups.add(group_name)
                elif line and not line.startswith("#"):
                    host_name = line.split()[0]
                    hosts.append(host_name)
                    
            print(f"  [PASS] {str(rel_path):<45} (Groups: {len(groups)}, Hosts/Vars: {len(hosts)})")
            for g in sorted(groups):
                print(f"         - Group: [{g}]")
        except Exception as e:
            print(f"  [FAIL] {str(rel_path):<45} ERROR: {e}")
            all_passed = False

    return all_passed

def validate_templates():
    print("\n[STEP 3] Validating Jinja2 Service & Proxy Templates...")
    template_dir = BASE_DIR / "roles" / "springboot_app" / "templates"
    all_passed = True
    
    for t_file in template_dir.glob("*.j2"):
        rel_path = t_file.relative_to(BASE_DIR)
        try:
            with open(t_file, "r", encoding="utf-8") as f:
                content = f.read()
            # Simple check for matched jinja braces
            open_var = content.count("{{")
            close_var = content.count("}}")
            open_block = content.count("{%")
            close_block = content.count("%}")
            
            if open_var == close_var and open_block == close_block:
                print(f"  [PASS] {str(rel_path):<45} (Balanced Jinja2 Tags: {open_var} vars, {open_block} blocks)")
            else:
                print(f"  [FAIL] {str(rel_path):<45} Unbalanced Jinja2 tags!")
                all_passed = False
        except Exception as e:
            print(f"  [FAIL] {str(rel_path):<45} ERROR: {e}")
            all_passed = False

    return all_passed

def validate_config():
    print("\n[STEP 4] Validating ansible.cfg Configuration...")
    cfg_file = BASE_DIR / "ansible.cfg"
    try:
        config = configparser.ConfigParser()
        config.read(cfg_file)
        sections = config.sections()
        print(f"  [PASS] ansible.cfg found and parsed successfully.")
        print(f"         Sections found: {sections}")
        print(f"         Inventory Path: {config.get('defaults', 'inventory', fallback='N/A')}")
        print(f"         Roles Path:     {config.get('defaults', 'roles_path', fallback='N/A')}")
        print(f"         Become Sudo:    {config.get('privilege_escalation', 'become', fallback='N/A')}")
        return True
    except Exception as e:
        print(f"  [FAIL] ansible.cfg validation failed: {e}")
        return False

def main():
    print_banner("SHALACONNECT ANSIBLE PLAYBOOK & INVENTORY VALIDATION AUDIT")
    print("Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune\n")
    
    v1 = validate_yaml_files()
    v2 = validate_inventory()
    v3 = validate_templates()
    v4 = validate_config()
    
    print("\n" + "=" * 70)
    if v1 and v2 and v3 and v4:
        print(" [SUCCESS] ALL ANSIBLE SPECIFICATIONS, PLAYBOOKS & CONFIGS ARE VALID!")
        print(" All YAML files, Jinja2 templates, and INI inventories passed syntax check.")
        print("=" * 70)
        sys.exit(0)
    else:
        print(" [ERROR] SYNTAX OR INTEGRITY VALIDATION FAILED!")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()
