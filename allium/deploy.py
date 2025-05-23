#!/usr/bin/env python3

import os
import subprocess
import boto3
from pathlib import Path
import sys

# === Configuration ===

OUTPUT_DIR = Path("www")

# Load from environment
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")

# === Sanity Checks ===
if not all([R2_BUCKET_NAME, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT_URL]):
    print("❌ Missing one or more required environment variables:")
    print("R2_BUCKET_NAME, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT_URL")
    sys.exit(1)

# === Step 1: Run allium.py to generate static files ===
print("🚀 Generating static HTML files...")
subprocess.run(["python3", "allium.py", "--out", str(OUTPUT_DIR)], check=True)

# === Step 2: Upload to R2 ===
print("📤 Uploading to Cloudflare R2...")

session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    endpoint_url=R2_ENDPOINT_URL,
)

for file in OUTPUT_DIR.rglob("*"):
    if file.is_file():
        key = str(file.relative_to(OUTPUT_DIR))
        print(f" → Uploading {key}")
        s3.upload_file(
            Filename=str(file),
            Bucket=R2_BUCKET_NAME,
            Key=key,
            ExtraArgs={"ACL": "public-read"}  # optional if Worker handles access
        )

print("✅ Deployment to R2 complete.")
