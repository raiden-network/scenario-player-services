import os
import subprocess

from spaas_core import __version__

from constants import (
    BUMPVERSION_CFG,
    CIRCLE_TAG,
    COMMIT_TYPE,
    COMMIT_TYPES,
    CURRENT_BRANCH,
    IS_CODEBASE_CHANGE,
    PROJECT_GIT_DIR,
)


CI_CONFIG_DIR = os.environ["CI_CONFIG_DIR"]
# Bump if changes to codebase (spaas_core/**)
# Skip bumping if changes to other files

# patch bump if Commit message starts with '[FIX-#xxx'
# minor bump if commit message starts with '[FEAT-#xxx'

parts = {
    COMMIT_TYPES.FEAT: "minor",
    COMMIT_TYPES.FIX: "patch",
    COMMIT_TYPES.BUMP: "bump_part"
}

PART = parts[COMMIT_TYPE]

if CURRENT_BRANCH != "master":
    print("Skipping non-master branch.")
    exit(0)
elif COMMIT_TYPE is COMMIT_TYPES.BUMP:
    print("Skipping tagging to avoid loop.")
    exit(0)
elif COMMIT_TYPE is COMMIT_TYPES.UNKNOWN:
    print("No type specified, skipping tagging.")
    exit(0)
elif not IS_CODEBASE_CHANGE:
    print("No tagging for commits unrelated to the codebase! Skipping..")
    exit(0)


print(f"Tagging new version ({__version__} -> {PART})..")
r = subprocess.run(
    f"bumpversion --config-file={BUMPVERSION_CFG} "
    f"--current-version={__version__} {PART}".split(" "),
    check=True,
    stdout=subprocess.PIPE,
)

print("Push bump commit..")
subprocess.run(
    f"git --git-dir={PROJECT_GIT_DIR} push --set-upstream origin {CURRENT_BRANCH}".split(" "),
    check=True,
)

print("Push tag..")
subprocess.run(f"git --git-dir={PROJECT_GIT_DIR} push -u --tags origin".split(" "), check=True)
