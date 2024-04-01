#!/bin/bash

#associative array to store commits count by timezone
declare -A commits_by_timezone
#array to store timezone offsets
declare -a timezones

for i in {0..24}; do
    offset=$((i - 12))
    # Format offset with leading zeroes if needed
    if [ $offset -ge 0 ]; then
        timezone="+$(printf %02d $offset)00"
    else
        timezone="$(printf %03d $offset)00"
    fi
    #append in array
    timezones+=("$timezone")
done

#initialize commits_by_timezone array
for timezone_offset in ${timezones[@]}; do
    commits_by_timezone["$timezone_offset"]=0
done

#Loop through projects
while IFS= read -r name; do
    dir_name="$REPO_LOCATION/$name"
    cd "$dir_name" || continue

    # Loop through timezone offsets from -12 to +12
    for timezone_offset in ${timezones[@]}; do
    # Execute git log command with timezone offset
    commits_count=$(git log --before="2004-12-31" | grep -- "$timezone_offset" | wc -l)
    commits_by_timezone["$timezone_offset"]=$(( ${commits_by_timezone["$timezone_offset"]} + commits_count ))
    done 
done < "$DATA_LOCATION/projects-accepted.txt"

# write results to the  file
for timezone_offset in ${timezones[@]}; do
    echo "$timezone_offset: ${commits_by_timezone["$timezone_offset"]}" >> "$DATA_LOCATION/commits_by_timezone.txt"
done
