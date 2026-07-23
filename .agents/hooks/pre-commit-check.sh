#!/bin/bash

set -e

COMMAND="$ANTIGRAVITY_COMMAND"

if [[ "$COMMAND" == git\ commit* ]]; then
    echo "Running quality checks before commit..."

    make check

    if [ $? -ne 0 ]; then
        echo "Commit blocked: quality checks failed."
        exit 1
    fi
fi

exit 0
