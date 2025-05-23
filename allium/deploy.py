import os
import subprocess
import sys

# Ensure the required environment variable is set
cf_token = os.getenv("CLOUDFLARE_API_TOKEN")
if not cf_token:
    print("Error: CLOUDFLARE_API_TOKEN environment variable not set.", file=sys.stderr)
    sys.exit(1)

# Set the environment variable for wrangler
env = os.environ.copy()
env["CLOUDFLARE_API_TOKEN"] = cf_token

# Define the wrangler deploy command
deploy_command = [
    "wrangler",
    "pages",
    "deploy",
    "./public",  # Replace with your directory if different
    "--project-name=my-cloudflare-project-name",  # Replace with your actual project name
    "--branch=production"  # Or "main", "preview", etc.
]

try:
    print("Deploying to Cloudflare Pages...")
    subprocess.run(deploy_command, check=True, env=env)
    print("✅ Deployment complete.")
except subprocess.CalledProcessError as e:
    print("❌ Deployment failed.")
    sys.exit(e.returncode)
