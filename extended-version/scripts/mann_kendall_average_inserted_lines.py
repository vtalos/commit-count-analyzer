import sys
import argparse
import pymannkendall as mk


parser = argparse.ArgumentParser(description="A script for implementing Mann Kendall \
                                  Test for yearly trends of lines per commit")

parser.add_argument("filename", help="The txt file to get the data from")
"""
Usage:
python mann_kendall_average_inserted_lines.py <filename>

"""

file = sys.argv[1] 
with open(file) as file:
    lines = file.readlines()
    average_commits_per_year = []
    for line in lines:
        commits = line.partition(":")[2]
        average_commits_per_year.append(commits)
result = mk.original_test(average_commits_per_year)
test_statistic = result[0]
p_value = result[2]

# Print the results
print("Mann-Kendall Test Statistic:", test_statistic)
print("P-Value:", p_value)

# Interpret the results based on the p-value and significance level
alpha = 0.05  # Significance level

if p_value < alpha:
    print("There is a statistically significant trend in the data.")
else:
    print("There is no statistically significant trend in the data.")