#!/bin/bash
# This script counts the commits for a repo for 23:57-23:59
# for Tuesday April 16. The date was found after manual inspection
# of the gitlog for mariadb.

# Set name of the project e.g. owner/repo and the year to be mined.
name=$1
year=$2
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

dir_name="$REPO_LOCATION/$name"
cd "$dir_name" || continue

# Output git log for 2013 for 23:00-23:59
spike_commits=$(git log --format="%ad - %s" --after="$((year -1))-12-31" --before="$((year +1))-01-01"|
grep "23:5[7-9]:[0-5][0-9]" | grep "Tue Apr 16" |wc -l) 
echo "Commits during 23:57-23:59 on 16 April for $name: $spike_commits "


    
