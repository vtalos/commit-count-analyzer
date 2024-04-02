#!/bin/bash
# This script counts the number of commits in a specific hour and year
# for all the projects in the projects-accepted.txt file
set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

year=$1
echo "$year" >> "$DATA_LOCATION/check_spike.txt"
while IFS= read -r name; do
        dir_name="$REPO_LOCATION/$name"
        cd "$dir_name" || continue
        # count only the inserted lines, not the deleted lines
        commits_at_22=$(git log --after="$year-01-01" --before="$year-12-31" | grep Date |
        awk '{ print $5 }' | awk '/^22/' | wc -l)
        commits_at_22_last_year=$(git log --after="$((year-1))-01-01" --before="$((year-1))-12-31" | grep Date |
        awk '{ print $5 }' | awk '/^22/' | wc -l)
        diff= $((commits_at_22 - commits_at_22_last_year))
        echo "$name: $commits_at_22 $commits_at_22_last_year $diff" >> "$DATA_LOCATION/check_spike.txt"
    done < "$DATA_LOCATION/projects-accepted.txt"
done