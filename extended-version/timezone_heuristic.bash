#!/bin/bash

# This script checks if contributors have different timezone offset in their commits.
# It iterates over all contributors and checks if the timzeone in their first and last commits are different.

set -eu


#hardcoded
cd ../../Working_Patterns_Tex_Src
# Get a list of unique contributors' email addresses
contributors=$(git log --format='%ae' | sort -u)

# Iterate over each contributor
for contributor in $contributors; do
    # Find the first commit of the contributor
    first_commit_date=$(git log --format='%ad' --author="$contributor" | tail -n 1 | awk '{print $1, $2, $3, $4, $5}')
    # Find the last commit of the contributor
    last_commit_date=$(git log --format='%ad' --author="$contributor" | head -n 1 | awk '{print $1, $2, $3, $4, $5}')
    # Extract timezone offsets from the dates
    first_tz_offset=$(date -d "$first_commit_date" +%z)
    last_tz_offset=$(date -d "$last_commit_date" +%z)

    # Check if timezone offsets are different
    if [ "$first_tz_offset" != "$last_tz_offset" ]; then
        echo "Contributor email $contributor has different timezone offsets: $first_tz_offset and $last_tz_offset"
    fi
done
