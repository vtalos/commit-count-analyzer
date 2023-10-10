import pymannkendall as mk
import sys
import argparse
from itertools import tee
import csv
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="A script for implementing Mann Kendall Test")

parser.add_argument("filename", help="The csv file to get the data from")
parser.add_argument("day", help="The day of the week to implement the Mann Kendall Test")

filename = sys.argv[1] # The first argument is the filename
week_day = sys.argv[2] # The second argument is the day of the week

day_total = []
all_commits = [[] for _ in range(7)]
sum_period = []

# Open the csv file and read its contents into the lists
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    periods = next(reader)  # Skip header row
    # Copy the reader
    reader_copy1, reader_copy2 = tee(reader)
    num_of_periods = len(periods)
    period = [[] for _ in range(num_of_periods)]

    # Append the number of commits for each day in each period
    for row in reader_copy2:
        for i in range(1, len(period)):
            period[i].append(float(row[i]))
    # Append for each week day the number of commits for every period
    for i in range(len(period[1])):
        total_commits = 0
        for j in range(1, len(period)):
            all_commits[i].append(period[j][i]) # Calculate the total number of commits for each day
            total_commits += period[j][i]
        day_total.append(total_commits)
    # Calculate total commits for each period
    for i in range(1, len(period)):
        sum_period.append(sum(period[i]))

per = range(1, len(periods))
periods = periods[1:len(periods)]
data = all_commits[int(week_day)]

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


days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Create a time series plot
plt.plot(periods, data, marker='o', linestyle='-')
plt.xlabel('Time')
plt.ylabel('Data Values')
plt.title(f'Time Series Data for {days[int(week_day)]}')
plt.grid(True)

# Display the trend line
if p_value < alpha:
    plt.plot(data, marker='o', linestyle='-', color='red', label='Trend Line')
    plt.legend(['Data', 'Trend Line'])

# Show the plot
plt.show()





