from collections import defaultdict
from git import Repo
import argparse
import csv
import sys

# Handle the arguments
parser = argparse.ArgumentParser(description='Creates a csv containing the commit count per day of the week' \
'for a given interval and repository')
parser.add_argument('start_year', type=int, help='The year commit counting starts')
parser.add_argument('end_year', type=int, help='The year commit counting stops')
parser.add_argument('interval', type=int, help='How many years a single interval contains')
args = parser.parse_args()

repo_path = 'C:\\Users\\zimpr\\OneDrive\\Desktop\\TipMe\\TipMe'  # Replace with repo path
repo = Repo(repo_path)

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Initialize a dictionary to store the commit counts per day
num_of_periods = (args.end_year - args.start_year + 1) // args.interval

commit_counts = defaultdict(lambda: [0] * num_of_periods)

# Calculate the commit counts for each day and period
for commit in repo.iter_commits():
    commit_year = commit.authored_datetime.year
    
    if args.start_year <= commit_year <= args.end_year:
        day_index = commit.authored_datetime.weekday()
        interval_index = (commit_year - args.start_year) // args.interval
        
        if interval_index < 0 or interval_index >= num_of_periods:
            # Handle cases where commit year is outside the specified range
            print("Invalid arguments given")
            sys.exit(1)
        
        commit_counts[day_index][interval_index] += 1


# Write the commit counts in a CSV file
with open('CommitCountsPerDay.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Day'] + [f'{year}-{year+args.interval-1}' for year in range(args.start_year, args.end_year+1, args.interval)])  # Write the year intervals as the first row
    
    for day_index, day in enumerate(days_of_week):
        writer.writerow([day] + [str(count) for count in commit_counts[day_index]])