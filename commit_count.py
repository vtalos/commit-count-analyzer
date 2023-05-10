import csv

filename = 'trifo.csv'
with open(filename, 'r') as f:
    reader = csv.reader(f)
    #next(reader)
    counts = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}
    total_commits = 0
    for row in reader:

        lines = row[0].split('\n')  # Split the text into separate lines
        number = [line.split()[0] for line in lines]  # Extract the day abbreviation from each line
        days = [line.split()[1] for line in lines]
        counts[days[0].strip()] += int(number[0])
        print(number[0])
        total_commits = total_commits + int(number[0])

    print(total_commits)
    proportions = {day: count / total_commits if total_commits != 0 else 1 for day, count in counts.items()}
    print(proportions)

