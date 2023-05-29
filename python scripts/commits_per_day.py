import csv
import subprocess
from collections import defaultdict
import os

# Define the path to the repository folder
repo_path = 'php-src.git' 

# Define the start and end years for the interval
start_year = 2000
end_year = 2004

# Delete the file if it exists
if os.path.exists('CommitCounts.csv'):
    os.remove('CommitCounts.csv')

# Define the days of the week
days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Initialize a dictionary to store the commit counts per day
commit_counts = defaultdict(lambda: [0] * 5)

# Iterate over the years in the interval
while end_year <= 2024:
    # Execute the git log command to retrieve the commit timestamps
    cmd = f'git -C {repo_path} log --all --since="{start_year}-01-01" --until="{end_year + 1}-01-01" --format="%cd" --date=format:"%a"'
    output = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')

    # Count the commits per day within the interval
    for timestamp in output:
        day = timestamp.strip()
        commit_counts[day][(start_year - 2000) // 5] += 1

    start_year += 5
    end_year += 5

# Write the results to a CSV file
with open('CommitCounts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([''] + [f'{year}-{year+4}' for year in range(2000, 2019, 5)]+[f'2020-2023'])  # Write the year intervals as the first row
    
    for day in days_of_week:
        writer.writerow([day] + commit_counts[day])