import csv
from itertools import tee
import numpy as np
import sys
import argparse
import statsmodels.api as sm
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="A script for implementing linear regression")

parser.add_argument("filename", help="The csv file to get the data from")
parser.add_argument("day", help="The day of the week to implement the linear regression")

filename = sys.argv[1] # The first argument is the filename
week_day = sys.argv[2] # The second argument is the day of the week

day_total = []
all_commits = [[] for _ in range(7)]
sum_period = []

# Open the csv file and read its contents into the lists
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    periods = next(reader)  # Skip header row
    # Copy the reader
    reader_copy1, reader_copy2 = tee(reader)
    num_of_periods = len(periods)
    period = [[] for _ in range(num_of_periods)]

    # Append the number of commits for each day in each period
    for row in reader_copy2:
        for i in range(1, len(period)):
            period[i].append(float(row[i]))
    # Append for each week day the number of commits for every period
    for i in range(len(period[1])):
        total_commits = 0
        for j in range(1, len(period)):
            all_commits[i].append(period[j][i]) # Calculate the total number of commits for each day
            total_commits += period[j][i]
        day_total.append(total_commits)
    # Calculate total commits for each period
    for i in range(1, len(period)):
        sum_period.append(sum(period[i]))

per = range(1, len(periods))
periods = periods[1:len(periods)]
data = all_commits[int(week_day)]

# Add a constant term for the intercept
X = sm.add_constant(per)
y = np.array(data)

# Fit the linear regression model
model = sm.OLS(y, X).fit()

# Print the model summary
print(model.summary())

# Create a scatter plot of the data points
plt.scatter(per, y, label="Data Points")

# Plot the linear regression line
regression_line = model.params[0] + model.params[1] * np.array(per)
plt.plot(per, regression_line, color='red', label="Regression Line")

plt.xlabel("Period")
plt.ylabel("Number of Commits")
plt.title("Linear Regression Analysis")
plt.legend()
plt.grid(True)
plt.show()