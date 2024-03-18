#!/bin/bash
set -eu
DATA_LOCATION=$(pwd)
REPO_LOCATION=/home/repos/github
for year in {2004..2023}; do
    contributors_per_year_all_repos=0 
    while IFS= read -r name ; do
        contributors_per_year=0  
        dir_name="$REPO_LOCATION/$name"	
        cd "$dir_name" || continue
        contributors_per_year=$(git log --after="$year-01-01" --before="$((year+1))-01-01" --format='%ae' | sort -u | wc -l) 
        contributors_per_year_all_repos=$((contributors_per_year_all_repos + contributors_per_year)) 
         echo "$year, $name, $contributors_per_year"
	 echo "$contributors_per_year_all_repos"
    done
    echo "$year: $contributors_per_year_all_repos" >> results.txt 
done < "$DATA_LOCATION/projects-accepted.txt"
