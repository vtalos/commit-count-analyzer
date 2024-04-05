#!/bin/bash

name=$1
year=$2
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github
output_file="$DATA_LOCATION/gitlog.txt"

> "$DATA_LOCATION/gitlog.txt"
dir_name="$REPO_LOCATION/$name"

cd "$dir_name" || continue
for month in {01..12}; do
    for day in {01..31}; do
        # Check if the date is valid
        if date -d "$year-$month-$day" > /dev/null 2>&1; then
            # Output git log for the day to the file
            echo "Date: $year-$month-$day"
            git log --date=format-local:"%Y-%m-%d" --after="$year-$month-${day}T22:59:59" --before="$year-$month-{$day}T23:59:59" >> "$output_file"
        fi
    done
done