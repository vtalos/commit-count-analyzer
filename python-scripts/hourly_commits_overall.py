import csv,subprocess,sys,argparse,re,os

parser= argparse.ArgumentParser(description='Creates a csv for the hourly commits' \
'per interval for the given repositories')
parser.add_argument('start_year', help='The year commit counting starts')
parser.add_argument('end_year', help='The year commit counting stops')
parser.add_argument('interval', help='How many years a single interval contains')

# Define the paths to the repository folder
repos = []

# Regular expression pattern
pattern = re.compile(r'.*\.git.*')

for root, dirs, files in os.walk('.'):
    for dir_name in dirs:
        if re.match(pattern, dir_name): 
            repos.append(dir_name)
interval=int(sys.argv[3])

# Define the hour labels
hour_labels = [f'{hour:02d}:00-{hour:02d}:59' for hour in range(24)]

# Initialize an empty dictionary to store the commit counts per hour
commit_counts = {}

# Initialize a list to store the interval labels
interval_labels = []
for repo in repos:
    # Define the start and end years for the interval
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])
    # Iterate over the years in the interval
    while start_year + interval - 1 <= end_year:
        interval_label = f'{start_year}-{start_year+interval-1}'
        interval_labels.append(interval_label)

        # Execute the git log command to retrieve the commit timestamps
        cmd = f'git -C {repo} log --all --since="{start_year}-01-01" --until="{start_year + interval}-01-01" --format="%cd" --date=format:"%H"'
        output = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')

        # Count the commits per hour
        for timestamp in output:
            hour = int(timestamp)
            #if the hour key does not exist, insert hour with an empty array
            #for every hour append how many interval_labels it is associated with.
            commit_counts.setdefault(hour, []).append(interval_label) 
        start_year += interval
    # Write the results to a CSV file
with open('HourlyCommitsOverall.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([''] + interval_labels)  # Write the interval labels as the first row

    for hour_label in hour_labels:
        row = [hour_label]
        for interval_label in interval_labels:
            #for every hour in the commit counts,find how many appearances 
            # of the certain interval it has
            count = commit_counts.get(hour_labels.index(hour_label), []).count(interval_label)
            row.append(count)
        writer.writerow(row)

# Calculate the column (day) totals
# Count how many times a particular interval label exists in commit[counts]
column_totals = [sum(commit_counts[hour].count(interval_label) for hour in range(24)) for interval_label in interval_labels]

# Calculate the percentages
percentages = []
for j in range(len(interval_labels)):
    interval_percentages = [commit_counts[hour].count(interval_labels[j]) / column_totals[j] for hour in range(24)]
    percentages.append(interval_percentages)

# Write the percentages to a new CSV file
with open('HourlyCommitsPercentagesOverall.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([''] + interval_labels)  # Write the interval labels as the first row

    for i, hour_label in enumerate(hour_labels):
        row = [hour_label]
        for j, interval_label in enumerate(interval_labels):
            percentage = percentages[j][i]
            row.append(percentage)
        writer.writerow(row)