import os
from pathlib import Path

path = Path(os.path.join(".", ".git", "hooks"))
print("Hooks path:")
print(str(path))
path.mkdir(parents=True, exist_ok=True)

file_content = r"""
#!/usr/bin/env bash

# git hook to run a command after `git pull` if a specified file was changed
# Run `chmod +x post-merge` to make it executable then put it into `.git/hooks/`.

PREV_COMMIT=$1
POST_COMMIT=$2

changed_files="$(git diff-tree -r --name-only --no-commit-id $PREV_COMMIT $POST_COMMIT)"

check_run() {
	echo "$changed_files" | grep --quiet "$1" && eval "$2"
}

# Example usage
# In this example it's used to run `poetry install` if package.json changed
check_run poetry.lock "poetry install"
"""

print("Opening...")
with open(os.path.join(path, "post-checkout"), "wt") as f:
    print("Writing...")
    f.write(file_content)
