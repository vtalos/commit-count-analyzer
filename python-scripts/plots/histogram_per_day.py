import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys

filename = sys.argv[1] # The first argument is the file name
day = sys.argv[2] # The second argument is the preferred day
# day list contains the number of commits for each week day in every time period
day = [[] for _ in range(7)]

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
        for j in range(1, len(period)):
            day[i].append(period[j][i])
    # Calculate total commits for each period
    for i in range(1, len(period)):
        sum_period.append(sum(period[i]))
    
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
