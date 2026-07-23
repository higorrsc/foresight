#!/bin/bash

STATUS=$(git status --short)

if [ -n "$STATUS" ]; then
    echo "Repository has uncommitted changes:"
    echo "$STATUS"
else
    echo "Repository clean."
fi

exit 0
