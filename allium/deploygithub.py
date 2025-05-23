import os
import subprocess
import sys
from pathlib import Path

OUTPUT_DIR = Path("./www")
BRANCH_NAME = "output"  # or "gh-pages"

def run(cmd, cwd=None):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=cwd)

def main():
    # Set Git config (use env vars or hardcode if necessary)
    GITHUB_REPO = os.getenv("GITHUB_REPO")  # e.g. git@github.com:user/repo.git
    GITHUB_ACTOR = os.getenv("GITHUB_ACTOR", "Render Bot")
    GITHUB_EMAIL = os.getenv("GITHUB_EMAIL", "bot@render.com")

    if not GITHUB_REPO:
        print("Missing GITHUB_REPO environment variable", file=sys.stderr)
        sys.exit(1)

    # Create a temp git repo inside the output directory
    if not OUTPUT_DIR.exists():
        print(f"Error: {OUTPUT_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    run(["git", "init"], cwd=OUTPUT_DIR)
    run(["git", "config", "user.name", GITHUB_ACTOR], cwd=OUTPUT_DIR)
    run(["git", "config", "user.email", GITHUB_EMAIL], cwd=OUTPUT_DIR)
    run(["git", "checkout", "-b", BRANCH_NAME], cwd=OUTPUT_DIR)
    run(["git", "add", "."], cwd=OUTPUT_DIR)
    run(["git", "commit", "-m", "Update generated HTML"], cwd=OUTPUT_DIR)
    run(["git", "push", "--force", GITHUB_REPO, f"{BRANCH_NAME}:{BRANCH_NAME}"], cwd=OUTPUT_DIR)

    print("✅ Pushed to GitHub")

if __name__ == "__main__":
    main()
