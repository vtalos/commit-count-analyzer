import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys
import statsmodels.api as sm

filename = sys.argv[1] # The first argument is the file name
time_block = int(sys.argv[2]) # The second argument is the time block to keep for the linear regression

hours = []

# Open the csv file and read its contents into the lists
with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    periods = next(reader)  # Skip header row
    # Copy the reader
    reader_copy1, reader_copy2, reader_copy3 = tee(reader, 3)
    num_of_periods = len(periods)
    period = [[] for _ in range(num_of_periods)]

    for row in reader_copy2:
        for i in range(1, len(period)):
            period[i].append(float(row[i]))

    # Split day in 1-hour blocks
    for row in reader_copy3:
        hours.append(row[0])

data = []

for per in period:
    if len(per) > 0:
        data.append(per[time_block])

p = range(1, len(periods))

# Add a constant term for the intercept
X = sm.add_constant(p)
y = np.array(data)

# Fit the linear regression model
model = sm.OLS(y, X).fit()

# Print the model summary
print(model.summary())

# Create a scatter plot of the data points
plt.scatter(p, y, label="Data Points")

# Plot the linear regression line
regression_line = model.params[0] + model.params[1] * np.array(p)
plt.plot(p, regression_line, color='red', label="Regression Line")

plt.xlabel("Period")
plt.ylabel("Number of Commits")
plt.title(f"Linear Regression Analysis for time block {hours[time_block]}")
plt.legend()
plt.grid(True)
# Set integer ticks for the x-axis
plt.xticks(np.arange(min(p), max(p) + 1, step=1), map(int, np.arange(min(p), max(p) + 1, step=1)))
plt.show()
