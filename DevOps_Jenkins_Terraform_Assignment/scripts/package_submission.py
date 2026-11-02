#!/usr/bin/env python3
"""
Create Submission Zip Archive for DevOps IA Activity 3
Jenkins CI/CD + Terraform Mini Project
Student: Yash Janardan Sabale | PRN: 2310423T26-27 | MITAOE Pune
Output: DevOps_IA3_Submission_Yash_Janardan_Sabale_2310423T26-27.zip
"""

import os
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSIGNMENT_DIR = ROOT_DIR / "DevOps_Jenkins_Terraform_Assignment"
ZIP_PATH = ROOT_DIR / "DevOps_IA3_Submission_Yash_Janardan_Sabale_2310423T26-27.zip"

def create_zip():
    print(f"Creating zip archive at: {ZIP_PATH}")
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Include root Jenkinsfile
        root_jenkinsfile = ROOT_DIR / "Jenkinsfile"
        if root_jenkinsfile.exists():
            zipf.write(root_jenkinsfile, "Jenkinsfile")

        # Walk through DevOps_Jenkins_Terraform_Assignment
        for root, dirs, files in os.walk(ASSIGNMENT_DIR):
            # Skip heavy downloaded provider binaries
            if ".terraform" in root and "providers" in root:
                continue
            for file in files:
                fpath = Path(root) / file
                arcname = fpath.relative_to(ROOT_DIR)
                zipf.write(fpath, arcname)

    size_mb = ZIP_PATH.stat().st_size / (1024 * 1024)
    print(f"Archive successfully created: {ZIP_PATH} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    create_zip()
