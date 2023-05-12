import csv
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

# create empty lists for each time period
period1 = []
period2 = []
period3 = []
period4 = []
period5 = []

# open the csv file and read its contents into the lists
with open("percentages.csv") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    for row in reader:
        period1.append(float(row[0]))
        period2.append(float(row[1]))
        period3.append(float(row[2]))
        period4.append(float(row[3]))
        period5.append(float(row[4]))

# create a contingency table of observed frequencies
observed_freq = np.array([period1, period2, period3, period4, period5])

# perform the chi-square test
chi2_stat, p_val, dof, expected_freq = chi2_contingency(observed_freq)

print("Chi-square statistic:", chi2_stat)
print("P-value:", p_val)

# check the p-value and print a message based on the results
if p_val < 0.05:
    print("The null hypothesis can be rejected. There is a statistically significant relationship between the time period and the observed frequency.")
else:
    print("The null hypothesis cannot be rejected. There is no statistically significant relationship between the time period and the observed frequency.")

# plot the frequencies for each category
categories = ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5", "Category 6", "Category 7"]
x = np.arange(len(categories))
width = 0.2

fig, ax = plt.subplots()
rects1 = ax.bar(x - 2*width, period1, width, label='Period 1')
rects2 = ax.bar(x - width, period2, width, label='Period 2')
rects3 = ax.bar(x, period3, width, label='Period 3')
rects4 = ax.bar(x + width, period4, width, label='Period 4')
rects5 = ax.bar(x + 2*width, period5, width, label='Period 5')

# add some labels and titles
ax.set_ylabel('Frequency')
ax.set_title('Frequency by Category and Time Period')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()

plt.show()


