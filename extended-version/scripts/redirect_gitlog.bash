#!/bin/bash
# This script redirects the output of the git log command to a file
# for all the projects in the projects-accepted.txt file.

# Set name of the project e.g. owner/repo and the year to be mined.
name=$1
year=$2
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github
output_file="$DATA_LOCATION/gitlog.txt"

> "$DATA_LOCATION/gitlog.txt"
dir_name="$REPO_LOCATION/$name"
cd "$dir_name" || continue

# Output git log for 2013 for 23:00-23:59
git log --grep="git-svn-id" --pretty="%h - %ad - %s" --after="2012-12-31" --before="2014-01-01" | grep "23:[0-5][0-9]:[0-5][0-9]" >> "$output_file"


    
