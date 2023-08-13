import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys

filename = sys.argv[1] # The first argument is the file name
time_block = sys.argv[2] # The second argument is the time block to keep for the linear regression

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
