#!/bin/bash
# This script counts the number of commits in a specific hour and year
# and the commits for the rest of the day
# for all the projects in the projects-accepted.txt file
set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

> "$DATA_LOCATION/check_spike.txt"
total_commits_at_23=0
total_commits_rest_day=0
total_diff=0
year=$1
echo "$year" >> "$DATA_LOCATION/check_spike.txt"
while IFS= read -r name; do
        dir_name="$REPO_LOCATION/$name"
        cd "$dir_name" || continue
        # count commints inside 23:00-23:59 for the specific year
        commits_at_23=$(git log --after="$year-01-01" --before="$year-12-31"  | grep Date |
        awk '{ print $5 }' | awk '/^23/' | wc -l)
	commits_rest_day=$(git log --after="$year-01-01" --before="$year-12-31" | grep Date|
	awk '{ print $5}' | grep -v '^23' | wc -l)
        #count commits inside 22:00-22:59 for the last year
        commits_at_23_last_year=$(git log --after="$((year-1))-01-01" --before="$((year-1))-12-31"  | grep Date |
        awk '{ print $5 }' | awk '/^23/' | wc -l)
        #calculate the difference
        diff=$((commits_at_23 - commits_at_23_last_year))
	total_commits_at_23=$((commits_at_23 + total_commits_at_23))
	total_diff=$((diff + total_diff))
	total_commits_rest_day=$((commits_rest_day + total_commits_rest_day))
        echo "$name: $commits_at_23 $commits_at_23_last_year $diff $commits_rest_day" >> "$DATA_LOCATION/check_spike.txt"
done < "$DATA_LOCATION/projects-accepted.txt"
echo "total commits 23:00-23:59 $total_commits_at_23 total diff $total_diff total commits rest day $total_commits_rest_day" >> "$DATA_LOCATION/check_spike.txt" 
