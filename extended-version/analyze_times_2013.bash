#!/bin/bash
# This script calculates and compares the total number of commits made 
# during the 23:00-23:59 time-block and other hours in the year 2013
# across all GitHub projects listed in the 'projects-accepted.txt' file.

set -eu

DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

target_year=2013
output_file="$DATA_LOCATION/commit_counts_2013.txt"

# Check if output file exists, truncate if it does
> "$output_file"

# Check if projects file exists
projects_file="$DATA_LOCATION/projects-accepted.txt"
if [ ! -f "$projects_file" ]; then
    echo "Error: projects file not found."
    exit 1
fi

total_commits_specific_hour=0
total_commits_other_hours=0

while IFS= read -r project_name; do
    dir_name="$REPO_LOCATION/$project_name"
    
    if [ ! -d "$dir_name" ]; then
        echo "Error: Directory not found - $dir_name"
        continue
    fi
    
    # Change to project directory
    if ! cd "$dir_name"; then
        echo "Error: Failed to change directory - $dir_name"
        continue
    fi

    # Count commits for 23:00-23:59 and all other hours in the target year
    commits_at_specific_hour=$(git log --after="$target_year-01-01" --before="$target_year-12-31" --pretty=format:%cd | grep -c '^.*23:.*')
    commits_at_other_hours=$(git log --after="$target_year-01-01" --before="$target_year-12-31" --pretty=format:%cd | grep -vc '^.*23:.*')
    
    # Accumulate counts
    (( total_commits_specific_hour += commits_at_specific_hour ))
    (( total_commits_other_hours += commits_at_other_hours ))
done < "$projects_file"

# Write total counts to output file
echo "Total commits at 23:00-23:59: $total_commits_specific_hour" >> "$output_file"
echo "Total commits at other hours: $total_commits_other_hours" >> "$output_file"