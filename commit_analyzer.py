import csv

# create empty lists for each time period
period1 = []
period2 = []
period3 = []
period4 = []
period5 = []

# open the csv file and read its contents into the lists
with open("percentages.csv") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    for row in reader:
        period1.append(float(row[0]))
        period2.append(float(row[1]))
        period3.append(float(row[2]))
        period4.append(float(row[3]))
        period5.append(float(row[4]))

print(period1)






