from matplotlib import pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller
import statsmodels.tsa.arima.model
from pandas import DataFrame
from math import sqrt
from sklearn import mean_squared_error


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

model = statsmodels.tsa.arima.model.ARIMA(endog=data.Commits, order=(1, 0, 0))
res = model.fit()
print(res.summary())
# line plot of residuals
residuals = DataFrame(res.resid)
residuals.plot()
plt.show()
# density plot of residuals
residuals.plot(kind='kde')
plt.show()
# summary stats of residuals

# split into train and test sets
X = data.Commits
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
# walk-forward validation
for t in range(len(test)):
	model =  statsmodels.tsa.arima.model.ARIMA(history, order=(5,1,0))
	model_fit = model.fit()
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
# evaluate forecasts
rmse = sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)
# plot forecasts against actual outcomes
plt.plot(test)
plt.plot(predictions, color='red')
plt.show()