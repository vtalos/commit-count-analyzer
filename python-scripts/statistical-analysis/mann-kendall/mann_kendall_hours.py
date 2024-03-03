import pymannkendall as mk
import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys
import statsmodels.api as sm

filename = sys.argv[1] # The first argument is the file name
time_block_start = int(sys.argv[2]) # The second argument is the time block to keep for the linear regression
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

# Create a time series plot
plt.xlabel('Time')
plt.ylabel('Data Values')
if time_block_start == time_block_end:
    plt.title(f'Time Series Data for period {hours[int(time_block_start)]}')
else:
    plt.title(f'Time Series Data for period {hours[int(time_block_start)]} - {hours[int(time_block_end)]}')


plt.grid(True)
plt.xticks(rotation=35)

# Display the trend line if exists
if p_value < alpha:
    plt.plot(periods, data, marker='o', linestyle='-', color='red', label='Trend Line')
    plt.legend(['Trend Line'])
else:
    plt.plot(periods, data, marker='o', linestyle='-')
    plt.legend(['Data'])

# Show the plot
plt.show()
