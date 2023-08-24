import csv
import subprocess
import os

os.chdir('The_Dir_You_Want_To_Work_With') #change directory, if needed
# Define the path to the repository folder
repo_path = 'php-src.git'

# Define the start and end years for the interval
start_year = 2000
end_year = 2004

# Delete the file if it exists
if os.path.exists('HourlyCommits.csv'):
    os.remove('HourlyCommits.csv')

# Define the hour labels
hour_labels = [f'{hour:02d}:00-{hour:02d}:59' for hour in range(24)]

# Initialize an empty dictionary to store the commit counts per hour
commit_counts = {}

# Initialize a list to store the interval labels
interval_labels = []

# Iterate over the years in the interval
while end_year <= 2024:
    interval_label = f'{start_year}-{end_year}'
    interval_labels.append(interval_label)

    # Execute the git log command to retrieve the commit timestamps
    cmd = f'git -C {repo_path} log --all --since="{start_year}-01-01" --until="{end_year + 1}-01-01" --format="%cd" --date=format:"%H"'
    output = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')

    # Count the commits per hour
    for timestamp in output:
        hour = int(timestamp)
        commit_counts.setdefault(hour, []).append(interval_label)

    start_year += 5
    end_year += 5

# Write the results to a CSV file
with open('HourlyCommits.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([''] + interval_labels)  # Write the interval labels as the first row

    for hour_label in hour_labels:
        row = [hour_label]
        for interval_label in interval_labels:
            count = commit_counts.get(hour_labels.index(hour_label), []).count(interval_label)
            row.append(count)
        writer.writerow(row)