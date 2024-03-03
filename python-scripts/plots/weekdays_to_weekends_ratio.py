import matplotlib.pyplot as plt
import sys
import numpy as np
import pandas as pd

filename = sys.argv[1] # The first argument is the file name
data=pd.read_csv(filename)
data=data.iloc[:,1:]
data=np.array(data)
weekdays = data.T[:,0:5]  # First five columns are weekdays
weekends = data.T[:,5:]  # Last two columns are weekends
avg_n_of_commits_weekdays = np.sum(weekdays, axis=1)/5
avg_n_of_commits_weekends = np.sum(weekends, axis=1)/2
fig, ax = plt.subplots()
ax.set_title('Ratio of Average Weekday Commits to Average Weekend Day Commits')
ax.set_xlabel('Year')
ax.set_ylabel('Ratio')
ax.set_xticks(range(2004,2024,2))
weekdays_line = plt.plot(range(2004, 2024), avg_n_of_commits_weekdays / avg_n_of_commits_weekends, 
        linestyle='-', marker='o', color='blue')
plt.grid(True)
plt.show()
