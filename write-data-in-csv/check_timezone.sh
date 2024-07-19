#!/bin/bash

commit_author=$1
commit_year=$2
commits_not_in_utc0=$(git log --pretty=format:"%ad %an" | grep "$commit_year" | grep "$commit_author" | grep -v +0000 | cut -d ' ' -f 6)
if [ -z "$commits_not_in_utc0" ]; then
    exit 0
    
else
    exit 1
fi
