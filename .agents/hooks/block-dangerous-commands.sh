#!/bin/bash

COMMAND="$ANTIGRAVITY_COMMAND"

BLOCKED_PATTERNS=(
    "git push --force"
    "git push -f"
    "git reset --hard"
    "git clean -fd"
    "rm -rf /"
    "chmod -R 777"
)

for pattern in "${BLOCKED_PATTERNS[@]}"
do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        echo "Blocked dangerous command: $pattern"
        exit 1
    fi
done

exit 0
