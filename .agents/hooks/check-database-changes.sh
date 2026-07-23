#!/bin/bash

FILES=$(git diff --name-only)

if echo "$FILES" | grep -E "models|entities|schemas"; then
    echo "Database-related files changed."
    echo "Review if an Alembic migration is required."
fi

exit 0
