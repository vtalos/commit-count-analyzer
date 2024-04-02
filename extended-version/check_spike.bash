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
        commits_at_22=$(git log --after="$year-01-01" --before="$year-12-31" | grep Date | awk '{ print $5 }' | awk '/^22/' | wc -l)
        echo "name: $name year: $year commits at 22:00-22:59: $commits_at_22"
        echo "$name: $commits_at_22" >> "$DATA_LOCATION/check_spike.txt"
    done < "$DATA_LOCATION/projects-accepted.txt"
done