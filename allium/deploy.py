import os
import subprocess
import sys
from pathlib import Path

OUTPUT_DIR = Path("www")
BRANCH_NAME = "output"  # Change to 'output' if desired

def run(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=cwd)

def main():
    # Run allium.py to generate output
    run(["python3", "allium.py", "--out", str(OUTPUT_DIR)])

    if not OUTPUT_DIR.exists():
        print(f"❌ ERROR: Output directory {OUTPUT_DIR} does not exist.")
        sys.exit(1)

    # Set Git config
    GITHUB_REPO = os.getenv("RENDER_GIT_REPO")  # Auto-populated by Render
    GITHUB_ACTOR = os.getenv("GITHUB_ACTOR", "Render Deployer")
    GITHUB_EMAIL = os.getenv("GITHUB_EMAIL", "bot@render.com")

    if not GITHUB_REPO:
        print("❌ ERROR: RENDER_GIT_REPO environment variable not set.")
        sys.exit(1)

    # Use token auth if available
    token = os.getenv("GITHUB_TOKEN")
    if token:
        GITHUB_REPO = GITHUB_REPO.replace("https://", f"https://{token}@")

    # Init repo in output dir
    run(["git", "init"], cwd=OUTPUT_DIR)
    run(["git", "config", "user.name", GITHUB_ACTOR], cwd=OUTPUT_DIR)
    run(["git", "config", "user.email", GITHUB_EMAIL], cwd=OUTPUT_DIR)
    run(["git", "checkout", "-b", BRANCH_NAME], cwd=OUTPUT_DIR)
    run(["git", "add", "."], cwd=OUTPUT_DIR)
    run(["git", "commit", "-m", "Update static output"], cwd=OUTPUT_DIR)
    run(["git", "push", "--force", GITHUB_REPO, f"{BRANCH_NAME}:{BRANCH_NAME}"], cwd=OUTPUT_DIR)

    print("✅ Successfully pushed to GitHub branch:", BRANCH_NAME)

if __name__ == "__main__":
    main()
