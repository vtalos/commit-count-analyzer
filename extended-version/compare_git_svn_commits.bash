#!/bin/bash
# This script counts the total number of commits made in the year 2013 and 
# the total number of commits made in the period from 2005 to 2023 (excluding 2013) 
# with "git-svn-id" in the commit message, for all the projects in the projects-accepted.txt file.

set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github
total_commits_2013=0
total_commits_excluding_2013=0

while IFS= read -r name; do
    dir_name="$REPO_LOCATION/$name"
    cd "$dir_name" || continue
    
    # Count commits with "git-svn-id" in the commit message for 2013
    commits_2013=$(git log --after="2013-01-01" --before="2013-12-31" --grep="git-svn-id" --oneline | wc -l)
    total_commits_2013=$((total_commits_2013 + commits_2013))

    # Count commits with "git-svn-id" in the commit message for the [2005, 2023] period excluding 2013
    commits_excluding_2013=$(git log --after="2005-01-01" --before="2023-12-31" --grep="git-svn-id" --oneline --invert-grep --grep="2013" | wc -l)
    total_commits_excluding_2013=$((total_commits_excluding_2013 + commits_excluding_2013))
done < "$DATA_LOCATION/projects-accepted.txt"

# Write results to a text file
echo "Total commits in 2013 with 'git-svn-id': $total_commits_2013" > "$DATA_LOCATION/git_svn_id_commits.txt"
echo "Total commits in [2005, 2023] excluding 2013 with 'git-svn-id': $total_commits_excluding_2013" >> "$DATA_LOCATION/git_svn_id_commits.txt"
