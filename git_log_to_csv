#!/bin/bash

# Get the git log with date format and UTC offset for all branches
cd php-src.git
git_log=$(git log --pretty=format:%aD --all)

# Create a CSV header
echo "Date,Time" > ../commits.csv

# Loop through each line of the git log
echo "$git_log" | while read -r commit_date; do
  # Extract the date and time from the local time string
  day=$(echo "$commit_date" | awk '{print $1}')
  time=$(echo "$commit_date" | awk '{print $5}')
  year=$(echo "$commit_date" | awk '{print $4}')
  # Print the commit date and time as a CSV row
  echo "$day,$year,$time" >> ../commits.csv
done 

