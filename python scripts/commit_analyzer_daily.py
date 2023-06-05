import csv
from itertools import tee
from scipy.stats import chi2_contingency
import numpy as np

days = 7
period = []

# open the csv file and read its contents into the lists
with open("CommitCountsDaily.csv") as csvfile:
    reader = csv.reader(csvfile)
    periods = next(reader)  # skip header row
    reader_copy1, reader_copy2 = tee(reader)
    num_of_periods = len(periods)
    period = [[] for _ in range(num_of_periods)]
    
    for row in reader_copy2:
        for i in range(1, len(period)):
            period[i].append(float(row[i]))

# create a contingency table of observed frequencies
cont_table = []
for i in range(1, len(period)):
    cont_table.append(period[i])

observed_freq = np.transpose(cont_table)

#observed_freq = np.array(cont_table)
print(observed_freq)

# perform the chi-square test
chi2_stat, p_val, dof, expected_freq = chi2_contingency(observed_freq)

print("Chi-square statistic:", chi2_stat)
print("P-value:", p_val)

# check the p-value
if p_val < 0.05:
    print("The null hypothesis can be rejected. There is a statistically significant relationship between the time period and the observed frequency.")
else:
    print("The null hypothesis cannot be rejected. There is no statistically significant relationship between the time period and the observed frequency.")



