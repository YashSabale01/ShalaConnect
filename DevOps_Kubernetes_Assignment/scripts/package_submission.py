#!/usr/bin/env python3
"""
Create Submission Zip Package for DevOps IA Activity No. 2
Student: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune
Output: DevOps_IA2_Submission_Yash_Janardan_Sabale_202301040087.zip
"""

import os
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent
ZIP_NAME = "DevOps_IA2_Submission_Yash_Janardan_Sabale_202301040087.zip"
ZIP_OUTPUT = ROOT_DIR / ZIP_NAME

EXCLUDE_PATTERNS = [
    ".git", "__pycache__", ".pyc", ".DS_Store", "Thumbs.db"
]

def should_exclude(path_str):
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False

def package_submission():
    print(f"Creating academic submission package: {ZIP_OUTPUT}...")
    file_count = 0
    total_size = 0

    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(ROOT_DIR)

                if should_exclude(str(full_path)):
                    continue

                zf.write(full_path, arcname=str(rel_path))
                file_count += 1
                total_size += full_path.stat().st_size

    zip_size_mb = ZIP_OUTPUT.stat().st_size / (1024 * 1024)
    print(f"Submission package created successfully!")
    print(f"Archive: {ZIP_OUTPUT}")
    print(f"Files Packaged: {file_count}")
    print(f"Uncompressed Data: {total_size / (1024 * 1024):.2f} MB")
    print(f"Zip File Size: {zip_size_mb:.2f} MB")

if __name__ == "__main__":
    package_submission()
