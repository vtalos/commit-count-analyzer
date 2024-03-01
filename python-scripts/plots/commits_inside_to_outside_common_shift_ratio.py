import matplotlib.pyplot as plt
import sys
import numpy as np
import pandas as pd

filename = sys.argv[1] # The first argument is the file name

data=pd.read_csv(filename)
data = data.iloc[:,1:]
data = np.array(data)
commits_in_9_to_5 = data.T[:,9:17]
avg_commits_in_9_to_5_shift= np.sum(commits_in_9_to_5, axis=1) / 8
commits_outside_9_to_5 = data.T[:, np.r_[0:8, 17:24]]
avg_commits_outside_9_to_5_shift = np.sum(commits_outside_9_to_5, axis=1) /16
fig, ax = plt.subplots()
ax.set_title('Ratio of commits inside and outside the 9 - 5 shift')
ax.set_xlabel('Year')
ax.set_ylabel('Ratio')
ax.set_xticks(range(2004,2024,2))
ax.plot(range(2004, 2024), avg_commits_in_9_to_5_shift / avg_commits_outside_9_to_5_shift, 
        linestyle='-', marker='o', color='blue')
plt.grid(True)
plt.show()