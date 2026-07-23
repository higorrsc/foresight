#!/bin/bash

set -e

COMMAND="$ANTIGRAVITY_COMMAND"

if [[ "$COMMAND" == git\ commit* ]]; then
    echo "Running quality checks before commit..."

    make check || {
        echo "Commit blocked: quality checks failed."
        exit 1
    }
fi

exit 0
