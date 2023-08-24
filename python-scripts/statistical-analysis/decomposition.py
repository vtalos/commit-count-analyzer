import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Read the CSV file
data = pd.read_csv('CommitCountsOverall.csv')

# Encode weekdays as pseudonumbers
weekday_dict = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
data['Day'] = data['Day'].map(weekday_dict)
# Reshape the data
data_reshaped = data.melt(id_vars='Day', var_name='Period', value_name='Observations')
print(data_reshaped)
# Perform seasonal decomposition on the reshaped data
decomposition = sm.tsa.seasonal_decompose(data_reshaped['Observations'], model='additive', period=7)
decomposition.plot()
print(decomposition.seasonal)
plt.show()