import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys

filename = sys.argv[1] # The first argument is the file name
plot = sys.argv[2] # The second argument is the requested plot
# day list contains the number of commits for each week day in every time period
day = [[] for _ in range(7)]

sum_period = []

# Open the csv file and read its contents into the lists
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    # Copy the reader
    reader_copy1, reader_copy2 = tee(reader)
    num_of_periods = len(list(reader_copy1)) - 1
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
periods = ["2000-2004", "2005-2009", "2010-2014", "2015-2019", "2020-2023"]

rects = []

def freq_by_period():
    x1 = np.arange(len(days))
    width = 0.15

    fig, ax = plt.subplots()

    count = len(period)
    for i in range(1, len(period)):
        x_shift = x1 + (i - count / 2 + 0.5) * width
        rect = ax.bar(x_shift, period[i], width, label=periods[i-1])
        rects.append(rect)

    # add labels and titles for the first plot
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Day')
    ax.set_title('Frequency by Day and Time Period')
    ax.set_xticks(x1)
    ax.set_xticklabels(days)
    ax.legend()


def freq_by_day():
    # create new x values for the second plot
    x2 = np.arange(len(periods))
    width = 0.1

    fig2, ax2 = plt.subplots()

    for i in range(len(day)):   
        x_shift = x2 + (i - (len(day) - 1) / 2) * width
        #x_shift = x2 + (i - 7 / 2 + 0.5) * width
        rect = ax2.bar(x_shift, day[i], width, label=days[i])
        rects.append(rect)

    ax2.set_ylabel('Frequencies')
    ax2.set_xlabel('Periods')
    ax2.set_title('Frequency by Time Period for each Day')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(periods)
    ax2.legend()


def freq_for_weekends():
    x3 = np.arange(len(periods))
    width = 0.16
    offset = width * 1.5

    fig3, ax3 = plt.subplots()

    for i in range(2):
        x_shift = x2 + (i - 1 / 2) * width
        #x_shift = x2 + (i - 7 / 2 + 0.5) * width
        rect = ax3.bar(x_shift, day[i], width, label=days[i])
        rects.append(rect)

    ax3.set_ylabel('Frequencies')
    ax3.set_xlabel('Periods')
    ax3.set_title('Frequency by Time Period for each Weekend')
    ax3.set_xticks(x3)
    ax3.set_xticklabels(periods)
    ax3.legend()


def total_commits_per_period():
    x4 = np.arange(len(periods))
    width = 0.3

    fig4, ax4 = plt.subplots()
    rects.append(ax4.bar(x4, sum_period, width))

    ax4.set_ylabel('Total Commits')
    ax4.set_xlabel('Period')
    ax4.set_title('Total Commits per Period')
    ax4.set_xticks(x4)
    ax4.set_xticklabels(periods)

if plot == "freq_by_period":
    freq_by_period()
elif plot == "freq_by_day":
    freq_by_day()
elif plot == "freq_for_weekends":
    freq_for_weekends()
else:
    total_commits_per_period()

plt.show()