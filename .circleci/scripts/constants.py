import enum
import os
import subprocess


class COMMIT_TYPES(enum.Enum):
    FEAT = "feat"
    FIX = "fix"
    BUMP = "version_bump"
    UNKNOWN = "unknown"

CODEBASE_ROOT_DIR = "spaas_core/"

# Fetch useful CircleCI environment variables
REPO_OWNER = os.environ["CIRCLE_PROJECT_USERNAME"]
REPO_NAME = os.environ["CIRCLE_PROJECT_REPONAME"]
BUMPVERSION_CFG = os.environ.get("BUMPVERSION_CFG")
PROJECT_ROOT = os.environ["PROJECT_ROOT"]
COMMIT_SHA = os.environ["CIRCLE_SHA1"]
CURRENT_BRANCH = os.environ.get("CIRCLE_BRANCH")
CIRCLE_TAG = os.environ.get("CIRCLE_TAG", False)

PROJECT_GIT_DIR = PROJECT_ROOT + "/.git"

# Get the git commit message subject line.
git_log_output = subprocess.run(
    f"git --git-dir {PROJECT_GIT_DIR} log "
    f"--format=oneline -n 1 {COMMIT_SHA} --format=%s".split(" "),
    check=True,
    stdout=subprocess.PIPE,
)
COMMIT_MSG = git_log_output.stdout.decode("UTF-8")

# Detect if files in the codebase were changed.
changed_files = subprocess.run(
    f"git --git-dir {PROJECT_GIT_DIR} diff-tree"
    f"--no-commit-id --name-only -r {COMMIT_SHA}".split(" "),
    check=True,
    stdout=subprocess.PIPE,
)
changed_files = changed_files.stdout.decode("UTF-8").split("\n")
IS_CODEBASE_CHANGE = bool([file.startswith(CODEBASE_ROOT_DIR) for file in changed_files])


if COMMIT_MSG.lower().startswith("[feat-#"):
    COMMIT_TYPE = COMMIT_TYPES.FEAT
elif COMMIT_MSG.lower().startswith("[fix-#"):
    COMMIT_TYPE = COMMIT_TYPES.FIX
elif CIRCLE_TAG:
    COMMIT_TYPE = COMMIT_TYPES.BUMP
else:
    COMMIT_TYPE = COMMIT_TYPES.UNKNOWN

# GH API auth token.
GH_AUTH_TOKEN = os.environ["GITHUB_TOKEN"]
GH_AUTH_HEADERS = {"Authorization": f"token {GH_AUTH_TOKEN}"}
