"""
Script to plot the number of contributors from results.txt for each year.

Usage:
    contributors_plot.py <filename.txt>

Arguments:
    <filename.txt>: txt file containing the number of contributors for each year for all of the sample,
    in this case the results.txt file.

Returns:
    A plot showing the number of contributors for the sample for each year.

Dependencies:
    - matplotlib
    - sys
Example:
    python contributors_plot.py results.txt
"""

import matplotlib.pyplot as plt
import sys

filename = sys.argv[1]
years= []
lines_to_commits_ratio_per_year = []
#open the .txt and read its contents 
with open(filename, 'r') as file:
    lines = file.readlines()
    for line in lines:
        #for each line retrieve the year and the contributors
        year, _, lines_to_commits_ratio = line.strip().partition(':')
        years.append(int(year.strip()))
        lines_to_commits_ratio_per_year.append(int(lines_to_commits_ratio.strip()))
#set font sizes, ticks and plot the data
fig, ax = plt.subplots()
print(years)
print(lines_to_commits_ratio_per_year)
plt.plot(years, lines_to_commits_ratio_per_year, linestyle='-', marker='o', color='blue', linewidth=5, markersize=15)
ax.set_xlabel('Year', fontsize = 18)
ax.set_ylabel('Lines to Commits Ratio', fontsize = 18)
plt.xticks(range(2004, 2024, 2), rotation = 45)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(15)
plt.grid(True)
plt.show()

        