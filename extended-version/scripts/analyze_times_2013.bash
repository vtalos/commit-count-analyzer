#!/bin/bash
# This script calculates and compares the total number of commits made 
# during the 23:00-23:59 time-block and other hours in the year 2013
# across all GitHub projects listed in the 'projects-accepted.txt' file.

set -eu

DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

target_year=2013
output_file="$DATA_LOCATION/commit_counts_2013.txt"
> "$output_file"
# Check if projects file exists
projects_file="$DATA_LOCATION/projects-accepted.txt"

total_commits_specific_hour=0
total_commits_other_hours=0

while IFS= read -r project_name; do
    dir_name="$REPO_LOCATION/$project_name"
    cd $dir_name || continue 
    # Count commits for 23:00-23:59 and all other hours in the target year
    commits_at_specific_hour=$(git log --after="$((target_year-1))-31-12" --before="$((target_year+1))-01-01" --pretty=format:%cd --all | grep -c '.*23:.*')
    commits_at_other_hours=$(git log --after="$((target_year-1))-31-12" --before="$((target_year+1))-01-01" --pretty=format:%cd --all | grep -vc '.*23:.*')
    # Accumulate counts
    (( total_commits_specific_hour=$total_commits_specific_hour + $commits_at_specific_hour ))
    (( total_commits_other_hours=$total_commits_other_hours + $commits_at_other_hours ))
done < "$projects_file"
echo "$total_commits_specific_hour"
# Write total counts to output file
echo "Total commits at 23:00-23:59: $total_commits_specific_hour" >> "$output_file"
echo "Total commits at other hours: $total_commits_other_hours" >> "$output_file"
