"""
Script to generate a plot showing the frequency of commits for each block of hour within a specific time period.

Usage:
    python plots_on_time.py <filename.csv> <period_name>

Arguments:
    <filename.csv>: CSV file containing commit data.
    <period_name>: String representing the name of the time period for which the hourly frequency plot is desired.

Returns:
    A plot showing the frequency of commits for each hour within the specified time period.

Dependencies:
    - numpy
    - matplotlib
    - csv

Example:
    python plots_on_time.py commit_data.csv 2020
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys

# Fetching the filename and period_name from command line arguments
filename = sys.argv[1]
period_name = sys.argv[2]

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

def hourly_frequences(period_hours, period):
    """
    Function to plot the frequency of commits for each hour within a specific time period.
    """
    rects = []
    x1 = np.arange(len(hours))
    width = 0.5

    fig, ax = plt.subplots()

    count = len(period_hours)
    rect = ax.bar(x1, period_hours, width, label=hours)
    rects.append(rect)

    ax.set_xticks(x1)
    ax.set_xticklabels(hours, rotation=45)
    
    # Add labels and titles for the first plot
    ax.set_ylabel('Percentage (%)', fontsize=35)
    ax.set_xlabel('Hour', fontsize=35)

    # Set xtick labels with empty strings for every other label
    labels = ["" if i % 2 == 1 else hours[i] for i in range(len(hours))]
    ax.set_xticklabels(labels)
    
    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(30)

    # Set tick font size
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(30)

    plt.show()


for i in range(len(periods)):
    if periods[i] == period_name:
        hourly_frequences(period[i], period_name)
        break