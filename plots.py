import csv
import numpy as np
import matplotlib.pyplot as plt

# create empty lists for each time period
period1 = []
period2 = []
period3 = []
period4 = []
period5 = []

day = [[] for _ in range(7)]

# open the csv file and read its contents into the lists
with open("CommitCountsDaily.csv") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row

    for row in reader:
        period1.append(float(row[1]))
        period2.append(float(row[2]))
        period3.append(float(row[3]))
        period4.append(float(row[4]))
        period5.append(float(row[5]))
        
    for i in range(len(period1)):
        day[i].append(period1[i])
        day[i].append(period2[i])
        day[i].append(period3[i])
        day[i].append(period4[i])
        day[i].append(period5[i])
    

# plot the frequencies for each category
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
periods = ["2000-2004", "2005-2009", "2010-2014", "2015-2019", "2020-2023"]

x1 = np.arange(len(days))
width = 0.15

fig, ax = plt.subplots()
rects1 = ax.bar(x1 - 2*width, period1, width, label=periods[0])
rects2 = ax.bar(x1 - width, period2, width, label=periods[1])
rects3 = ax.bar(x1, period3, width, label=periods[2])
rects4 = ax.bar(x1 + width, period4, width, label=periods[3])
rects5 = ax.bar(x1 + 2*width, period5, width, label=periods[4])

# add labels and titles for the first plot
ax.set_ylabel('Frequency')
ax.set_title('Frequency by Category and Time Period')
ax.set_xticks(x1)
ax.set_xticklabels(days)
ax.legend()

# create new x values for the second plot
x2 = np.arange(len(periods))
width = 0.1

fig2, ax2 = plt.subplots()
rects6 = ax2.bar(x2 - 2*width, day[0], width, label=days[0])
rects7 = ax2.bar(x2 - width, day[1], width, label=days[1])
rects8 = ax2.bar(x2, day[2], width, label=days[2])
rects9 = ax2.bar(x2 + width, day[3], width, label=days[3])
rects10 = ax2.bar(x2 + 2*width, day[4], width, label=days[4])
rects11 = ax2.bar(x2 + 3*width, day[5], width, label=days[5])
rects12 = ax2.bar(x2 + 4*width, day[6], width, label=days[6])

ax2.set_ylabel('')
ax2.set

plt.show()