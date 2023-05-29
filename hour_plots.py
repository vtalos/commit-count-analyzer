import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys

#filename = sys.argv[1] # The first argument is the file name
#plot = sys.argv[2] # The second argument is the requested plot
filename = 'HourlyCommits.csv'
hours = []

# Open the csv file and read its contents into the lists
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    periods = next(reader)  # Skip header row
    # Copy the reader
    reader_copy1, reader_copy2, reader_copy3 = tee(reader, 3)
    num_of_periods = len(periods) - 1
    period = [[] for _ in range(num_of_periods)]
    print(num_of_periods)
    # Append the number of commits for each day in each period
    for row in reader_copy2:
        for i in range(1, len(period)):
            #print(i, row[i])
            period[i].append(float(row[i]))
    # Split day in 1-hour blocks
    for row in reader_copy3:
        hours.append(row[0])

def hourly_frequences(period_hours, period):
    rects = []
    x1 = np.arange(len(hours))
    width = 0.4

    fig, ax = plt.subplots()

    count = len(period_hours)
    rect = ax.bar(x1, period_hours, width, label=hours)
    rects.append(rect)

    ax.set_xticks(x1)
    ax.set_xticklabels(hours, rotation=35, ha='right')
    # add labels and titles for the first plot
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Hour')
    ax.set_title('Frequency by Hour in Time Period ' + str(period))
    ax.set_xticks(x1)
    ax.set_xticklabels(hours)
    #ax.legend()

    plt.show()

hourly_frequences(period[1], periods[1])