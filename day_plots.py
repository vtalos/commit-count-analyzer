import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee

# create empty lists for each time period
period1 = []
period2 = []
period3 = []
period4 = []
period5 = []


day = [[] for _ in range(7)]

sum_period = []

# open the csv file and read its contents into the lists
with open("CommitCountsDaily.csv") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    reader_copy1, reader_copy2 = tee(reader)
    print(reader)
    print(reader_copy1)
    num_of_periods = len(list(reader_copy1)) - 1
    print(num_of_periods)
    period = [[] for _ in range(num_of_periods)]
    print(len(period))
    print(reader)
    for row in reader_copy2:
        print(row)
        for i in range(1, len(period)):
            period[i].append(float(row[i]))
            print(period[i])
        #period1.append(float(row[1]))
        #period2.append(float(row[2]))
        #period3.append(float(row[3]))
        #period4.append(float(row[4]))
        #period5.append(float(row[5]))
    for i in range(len(period[1])):
        day[i].append(period[1][i])
        day[i].append(period[2][i])
        day[i].append(period[3][i])
        day[i].append(period[4][i])
        day[i].append(period[5][i])

    for i in range(1, len(period)):
        sum_period.append(sum(period[i]))
'''
    sum_period.append(sum(period1))
    sum_period.append(sum(period2))
    sum_period.append(sum(period3))
    sum_period.append(sum(period4))
    sum_period.append(sum(period5))'''
    

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
periods = ["2000-2004", "2005-2009", "2010-2014", "2015-2019", "2020-2023"]

rects = []

x1 = np.arange(len(days))
width = 0.15

fig, ax = plt.subplots()
dif = -len(period)
for i in range(1, len(period)):
    rects.append(ax.bar(x1 + dif*width, period[i], width, label=periods[i-1]))
    dif += 1
count = len(period)
'''
rects1 = ax.bar(x1 - 2*width, period1, width, label=periods[0])
rects2 = ax.bar(x1 - width, period2, width, label=periods[1])
rects3 = ax.bar(x1, period3, width, label=periods[2])
rects4 = ax.bar(x1 + width, period4, width, label=periods[3])
rects5 = ax.bar(x1 + 2*width, period5, width, label=periods[4]) '''

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
dif = -len(day)
for i in range(count, count+len(day)):
    rects.append(ax2.bar(x2 + dif*width, day[i-count], width, label=days[i-count]))
    dif += 1

'''
rects6 = ax2.bar(x2 - 2*width, day[0], width, label=days[0])
rects7 = ax2.bar(x2 - width, day[1], width, label=days[1])
rects8 = ax2.bar(x2, day[2], width, label=days[2])
rects9 = ax2.bar(x2 + width, day[3], width, label=days[3])
rects10 = ax2.bar(x2 + 2*width, day[4], width, label=days[4])
rects11 = ax2.bar(x2 + 3*width, day[5], width, label=days[5])
rects12 = ax2.bar(x2 + 4*width, day[6], width, label=days[6])'''

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

dif = 1
for i in range(count, count+2):
    rects.append(ax2.bar(x2 + dif*width, day[i-count], width, label=days[i-count]))
    dif += 1

'''
rects13 = ax3.bar(x3 - 2*width + offset, day[5], width, label=days[5])
rects14 = ax3.bar(x3 - width + offset, day[6], width, label=days[6]) '''

ax3.set_ylabel('Frequencies')
ax3.set_xlabel('Periods')
ax3.set_title('Frequency by Time Period for each Weekend')
ax3.set_xticks(x3)
ax3.set_xticklabels(periods)
ax3.legend()

count = count + 2

x4 = np.arange(len(periods))
width = 0.3

fig4, ax4 = plt.subplots()
rects.append(ax4.bar(x4, sum_period, width))

ax4.set_ylabel('Total Commits')
ax4.set_xlabel('Period')
ax4.set_title('Total Commits per Period')
ax4.set_xticks(x4)
ax4.set_xticklabels(periods)
ax4.legend()

plt.show()