#!/bin/bash
# This script counts the number of lines per commit for each year
# for all the projects in the projects-accepted.txt file
set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

for year in {2004..2023}; do
    total_lines=0
    total_commits=0

    while IFS= read -r name; do
        dir_name="$REPO_LOCATION/$name"
        cd "$dir_name" || continue
        lines_per_project=$(git log --after="$year-01-01" --before="$year-12-31" --stat |
                            grep -E '\| *[0-9]+' |  awk -F'|' '{sum=0; sum+=$2} END {print sum}')
        commits_per_project=$(git log --after="$year-01-01" --before="$year-12-31" --oneline | wc -l)
        total_lines=$((total_lines + lines_per_project))
        total_commits=$((total_commits + commits_per_project))
        echo "$name $year $total_lines $total_commits"
    done < "$DATA_LOCATION/projects-accepted.txt"

    echo "$year: $total_lines/$total_commits" >> "$DATA_LOCATION/lines_per_commit.txt"
done