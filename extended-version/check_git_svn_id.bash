#!/bin/bash
# This script counts the number of commits with "git-svn-id" in the commit
# message for all the projects in the projects-accepted.txt file
set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github

year=$1
echo "$year" >> "$DATA_LOCATION/check_git_svn_id.txt"
while IFS= read -r name; do
    dir_name="$REPO_LOCATION/$name"
    cd "$dir_name" || continue
    # count only the inserted lines, not the deleted lines
    commits_with_git_svn=$(git log --after="$year-01-01" --before="$year-12-31" --grep="git-svn-id" --oneline | wc -l)
    commits_with_git_svn_next_year=$(git log --after="$((year+1))-01-01" --before="$((year+1))-12-31" --grep="git-svn-id" --oneline | wc -l)
    diff=$((commits_with_git_svn - commits_with_git_svn_next_year))
    echo "$name: $commits_with_git_svn $commits_with_git_svn_next_year $diff"
    echo "$name: $commits_with_git_svn $commits_with_git_svn_next_year $diff" >> "$DATA_LOCATION/check_git_svn_id.txt"
done < "$DATA_LOCATION/projects-accepted.txt"
