import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import adfuller

# Read the CSV file
data = pd.read_csv("C:\\Users\\karyo\Dropbox\\PC\\Desktop\\Έρευνα\\Scripts\\commit-count-analyzer\\python-scripts\\CommitCountsPerDay.csv")

# Encode weekdays as pseudonumbers
weekday_dict = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
data['Day'] = data['Day'].map(weekday_dict)
# Reshape the data with Day(1..7) / Year / Number of Commits formation
data_reshaped = data.melt(id_vars='Day', var_name='Period', value_name='Commits')

data_reshaped['Period']=data_reshaped['Period'].str.split('-').str.get(0)
print(data_reshaped)

# Perform seasonal decomposition on the reshaped data
decomposition = sm.tsa.seasonal_decompose(data_reshaped['Commits'], model='additive', period=7)
decomposition.plot()

#More graphs for the Seasonal Component
df_pivot = pd.pivot_table(data_reshaped, values='Commits', index='Day', columns='Period', aggfunc='mean')
df_pivot.plot(figsize=(12,8))
plt.legend().remove()
plt.xlabel('Day')
plt.ylabel('Commits')

#Stationarity of data check
result = adfuller(data_reshaped['Commits'])
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Test Statistics Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))

#Auto Correlation check
data_reshaped.drop(['Day', 'Commits'], axis=1, inplace=True)
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14,6), sharex=False, sharey=False)
ax1 = plot_acf(data_reshaped, lags=50, ax=ax1)
ax2 = plot_pacf(data_reshaped, lags=50, ax=ax2)


