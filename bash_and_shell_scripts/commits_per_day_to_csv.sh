#!/bin/bash
cd php-src.git
echo "-,2000-2004" > ../commits.csv
git_log=$(git log --all --pretty=format:%aD --since="2000-01-01" --until="2005-01-01" |
cut -d ',' -f1 | sort | uniq -c)
echo "$git_log" | while read -r row; do
day=$(echo "$row" | awk '{print $1}')
num_commits=$(echo "$row" | awk '{print $2}')
echo "$num_commits,$day">> ../commits.csv
done
echo "2005-2009">../column.csv
git_log=$(git log --all --pretty=format:%aD --since="2005-01-01" --until="2010-01-01" |
cut -d ',' -f1 | sort | uniq -c)
echo "$git_log" | while read -r row; do
num_commits=$(echo "$row" | awk '{print $1}')
echo "$num_commits">> ../column.csv
done
paste -d',' ../commits.csv ../column.csv > ../commits2.csv
echo "2010-2014">../column.csv
git_log=$(git log --all --pretty=format:%aD --since="2010-01-01" --until="2015-01-01" |
cut -d ',' -f1 | sort | uniq -c)
echo "$git_log" | while read -r row; do
num_commits=$(echo "$row" | awk '{print $1}')
echo "$num_commits">> ../column.csv
done
paste -d',' ../commits2.csv ../column.csv > ../commits3.csv
echo "2015-2019">../column.csv
git_log=$(git log --all --pretty=format:%aD --since="2015-01-01" --until="2020-01-01" |
cut -d ',' -f1 | sort | uniq -c)
echo "$git_log" | while read -r row; do
num_commits=$(echo "$row" | awk '{print $1}')
echo "$num_commits">> ../column.csv
done
paste -d',' ../commits3.csv ../column.csv > ../commits4.csv
echo "2020-2023">../column.csv
git_log=$(git log --all --pretty=format:%aD --since="2020-01-01" --until="2024-01-01" |
cut -d ',' -f1 | sort | uniq -c)
echo "$git_log" | while read -r row; do
num_commits=$(echo "$row" | awk '{print $1}')
echo "$num_commits">> ../column.csv
done
paste -d',' ../commits4.csv ../column.csv > ../commits.csv
rm -f ../commits2.csv ../commits3.csv ../commits4.csv ../commits5.csv ../column.csv

