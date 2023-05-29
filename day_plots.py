import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee

day = [[] for _ in range(7)]

sum_period = []

# open the csv file and read its contents into the lists
with open("CommitCountsDaily.csv") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    reader_copy1, reader_copy2 = tee(reader)
    num_of_periods = len(list(reader_copy1)) - 1
    period = [[] for _ in range(num_of_periods)]

    for row in reader_copy2:
        for i in range(1, len(period)):
            period[i].append(float(row[i]))

    for i in range(len(period[1])):
        day[i].append(period[1][i])
        day[i].append(period[2][i])
        day[i].append(period[3][i])
        day[i].append(period[4][i])
        day[i].append(period[5][i])

    for i in range(1, len(period)):
        sum_period.append(sum(period[i]))
    
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
periods = ["2000-2004", "2005-2009", "2010-2014", "2015-2019", "2020-2023"]

rects = []

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

count = count+len(day)

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


x4 = np.arange(len(periods))
width = 0.3

fig4, ax4 = plt.subplots()
rects.append(ax4.bar(x4, sum_period, width))

ax4.set_ylabel('Total Commits')
ax4.set_xlabel('Period')
ax4.set_title('Total Commits per Period')
ax4.set_xticks(x4)
ax4.set_xticklabels(periods)

plt.show()