#!/usr/bin/env bash

set -e

LOG_FILE=".agents/hooks/debug.log"

{
    echo "=========="
    date
    echo "Command:"
    echo "${ANTIGRAVITY_COMMAND:-unknown}"

    echo "Arguments:"
    echo "$@"

    echo "Environment:"
    env | sort

} >> "$LOG_FILE"

exit 0
