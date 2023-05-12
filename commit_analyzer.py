import csv
import numpy as np
from scipy.stats import chi2_contingency

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




