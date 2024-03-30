#!/bin/bash
# This script counts the number of lines per commit for each year
# for all the projects in the projects-accepted.txt file
set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

# modify diff.renameLimit configuration
git config diff.renames 5000

for year in {2004..2023}; do
    total_lines=0
    total_commits=0

    while IFS= read -r name; do
        dir_name="$REPO_LOCATION/$name"
        cd "$dir_name" || continue
        # count only the inserted lines, not the deleted lines
        lines_per_project=$(git log --after="2023-09-01" --stat | grep -E 'insertions' | 
        awk '{insertions += $4} END {print insertions}')
        commits_per_project=$(git log --after="$year-01-01" --before="$year-12-31" --oneline | wc -l)
        total_lines=$((total_lines + lines_per_project))
        total_commits=$((total_commits + commits_per_project))
        echo "name: $name year: $year lines_per_project: $lines_per_project commits_per_project: $commits_per_project"
    done < "$DATA_LOCATION/projects-accepted.txt"
    echo "year: $year total lines: $total_lines total commits: $total_commits"
    average_lines_per_commit=$(echo "scale=2; $total_lines / $total_commits" | bc)
    echo "$year: $average_lines_per_commit" >> "$DATA_LOCATION/lines_per_commit.txt"
done