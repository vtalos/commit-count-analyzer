import pymannkendall as mk
import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys
import statsmodels.api as sm

filename = sys.argv[1] # The first argument is the file name
time_block_start = int(sys.argv[2]) # The second argument is the first time block to consider
time_block_end = int(sys.argv[3]) # The third argument is the last time block to consider

hours = []

# Open the csv file and read its contents into the lists
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    periods = next(reader)  # Skip header row
    # Copy the reader
    reader_copy1, reader_copy2, reader_copy3 = tee(reader, 3)
    num_of_periods = len(periods)
    period = [[] for _ in range(num_of_periods)]

    for row in reader_copy2:
        for i in range(1, len(period)):
            period[i].append(float(row[i]))

    # Split day in 1-hour blocks
    for row in reader_copy3:
        hours.append(row[0])

data = []

for per in period:
    if len(per) > 0:

        if time_block_start != time_block_end:
            total = 0
            for i in range(time_block_start, time_block_end):
                total += per[i]
        else:
            total = per[time_block_start]

        data.append(total)

# Apply Mann Kendall Test
result = mk.original_test(data)

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

periods = periods[1:len(periods)]

# Plotting
fig, ax = plt.subplots()

# Create a time series plot
plt.xlabel('Time', fontsize=15)
plt.ylabel('Commits (%)', fontsize=15)

# Set xtick labels with empty strings for every other label
labels = ["" if i % 2 == 1 else periods[i] for i in range(len(periods))]
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=45)

plt.grid(True)
plt.xticks(rotation=35)

# Set tick font size
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(12)

# Set tick font size
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(12)

# Display the trend line if exists
if p_value < alpha:
    plt.plot(periods, data, marker='o', linestyle='-', color='red', label='Trend Line', linewidth=5, markersize=15)
else:
    plt.plot(periods, data, marker='o', linestyle='-', linewidth=5, markersize=15)

# Show the plot
plt.show()
