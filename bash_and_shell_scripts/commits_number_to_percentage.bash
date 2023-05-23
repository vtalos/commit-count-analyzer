#!/bin/bash
rm -f percentages.csv
# Read the CSV file

input_file="commits.csv"
column=()
sum=()
for ((i=1;i<=5;i++)); do
 sum["$i"]=0
 column["$i"]=0
done

# Extract the columns from the CSV

for ((i=1;i<=5;i++)); do
 column["$i"]+=$(awk -F',' -v i="$i" 'NR > 1 {print $((i+1))}' "$input_file")
done

# Calculate the total sum for the week

for ((i=1;i<=5;i++)); do
 while IFS=',' read -r value; do
  sum["$i"]=$(echo "${sum[$i]} + $value" | bc)
done <<< "${column[$i]}"
done
# Calculate the percentages for each element
percentages=()
for ((i=1;i<=5;i++)); do
 while IFS=',' read -r value; do
  percentage=$(echo "scale=6; $value / ${sum[$i]} *100" | bc)
  percentages+=("$percentage")
  done <<< "${column[$i]}"
done
# Reshape the percentages into a 7x5 matrix
percentage_matrix=()
rows=7
for ((r=1; r<=rows; r++)); do
    percentage_row=()
    for ((i=-1+r; i<=34; i=i+7)); do
        index="$i"
        percentage_row+=("${percentages[$index]}")
    done
     IFS=','
     percentage_matrix+=("${percentage_row[*]}")
done

# Create the header
header="2000-2004,2005-2009,2010-2014,2015-2019,2020-2023"
# Write the header and percentage matrix to the CSV file
echo "$header" >> percentages.csv
for row in "${percentage_matrix[@]}"; do
    echo "$row" >> percentages.csv
done
