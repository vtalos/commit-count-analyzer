from matplotlib import pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller

# Read the CSV file
data = pd.read_csv("..\\csv-files\\CommitCountsPerDayInterval4.csv")
# Drop the header row
data= data.drop(data.index[0])
# Drop the first row
data = data.iloc[1:]
# Reshape the data with Day(1..7) / Year / Number of Commits formation
data = data.melt(id_vars='Day', var_name='Period', value_name='Commits')
#remove 'Day' and 'Period' Column
data=data.drop('Day',axis=1)
data=data.drop('Period',axis=1)
plot_acf(data.Commits)

f=plt.figure()
ax1=f.add_subplot(121)
ax1.set_title('1st Order Differencing')
ax1.plot(data.Commits.diff())
ax2=f.add_subplot(122)
plot_acf(data.Commits.diff().diff().dropna(),ax=ax2)


f=plt.figure()
ax1=f.add_subplot(121)
ax1.set_title('2nd Order Differencing')
ax1.plot(data.Commits.diff().diff())
ax2=f.add_subplot(122)
plot_acf(data.Commits.diff().dropna(), ax=ax2)


#if each p-value is less than 0.05 the data is stationary, computes d
result=adfuller(data.Commits.dropna())
print('p-value:',result[1])
result=adfuller(data.Commits.diff().dropna())
print('p-value:',result[1])
