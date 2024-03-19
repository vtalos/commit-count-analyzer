# Example data for three groups
from scipy.stats import kruskal
import sys
import pandas as pd
import numpy as np

filename = sys.argv[1]
data=pd.read_csv(filename)
data=data.iloc[:,1:]
data=np.array(data)
groups=[0]*len(data)
for i in range(0, len(data)):
    groups[i]=data[i] # groups contain the number of commits for each Day/Hour
for i in range(0, len(data)):
    for j in range(0, len(data[i])):
        if i>j:
            statistic, p_value = kruskal(groups[i], groups[j])
            print("Kruskal-Wallis Test:")
            print("H statistic:", statistic)
            print("p-value:", p_value)
            alpha = 0.05
            if p_value < alpha:
                print(f'Reject null hypothesis: There are significant differences between the groups {i} and {j}.')
            else:
                print(f'Fail to reject null hypothesis: There are no significant differences between the groups {i} and {j}.')