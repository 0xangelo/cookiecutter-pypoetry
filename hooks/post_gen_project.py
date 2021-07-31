import os
from pathlib import Path

path = Path(os.path.join(".", ".git", "hooks"))
print("Hooks path:", str(path))
path.mkdir(parents=True, exist_ok=True)

file_content = \
r"""#!/usr/bin/env zsh

# git hook to run a command after `git checkout` if a specified file was changed
# Run `chmod +x post-checkout` to make it executable then put it into `.git/hooks/`.

PREV_COMMIT=$1
POST_COMMIT=$2

NOCOLOR='\e[0m'
REDCOLOR='\e[37;41m'

if [[ -f poetry.lock ]]; then
  DIFF=$(git diff --shortstat "$PREV_COMMIT".."$POST_COMMIT" poetry.lock)
  if [[ $DIFF != "" ]]; then
    echo -e "${REDCOLOR}poetry.lock has changed. You must run poetry install${NOCOLOR}"
  fi
fi
"""

with open(os.path.join(path, "post-checkout"), "wt") as f:
    print("Writing post-checkout hook")
    f.write(file_content)


file_content = \
r"""#!/usr/bin/env bash
# MIT © Sindre Sorhus - sindresorhus.com

# git hook to run a command after `git pull` if a specified file was changed
# Run `chmod +x post-merge` to make it executable then put it into `.git/hooks/`.

changed_files="$(git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD)"

check_run() {
	echo "$changed_files" | grep --quiet "$1" && eval "$2"
}

# Example usage
# In this example it's used to run `npm install` if package.json changed
check_run poetry.lock "poetry install"
"""
with open(os.path.join(path, "post-merge"), "wt") as f:
    print("Writing post-merge hook")
    f.write(file_content)


