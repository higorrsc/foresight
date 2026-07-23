#!/usr/bin/env bash

set -e

CHANGED_FILES=$(git diff --name-only -- '*.py')

if [ -z "$CHANGED_FILES" ]; then
    exit 0
fi

echo "Formatting changed Python files..."

ruff format $CHANGED_FILES
ruff check $CHANGED_FILES --fix
