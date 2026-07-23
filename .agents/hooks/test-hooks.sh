#!/usr/bin/env bash

set -e

for file in .agents/hooks/*.sh
do
    bash -n "$file"
done

echo "All agent hooks are valid."
