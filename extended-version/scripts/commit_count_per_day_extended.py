from collections import defaultdict
from git import Repo
import argparse
import csv
import os

parser = argparse.ArgumentParser(description='Creates a CSV containing commit count per day of the week '
                                              'for a given interval and repository')
parser.add_argument('start_year', type=int, help='The year commit counting starts')
parser.add_argument('end_year', type=int, help='The year commit counting stops')
parser.add_argument('interval', type=int, help='How many years a single interval contains')
parser.add_argument('contents', type=str, choices=["proportions", "total"],
                    help='The contents of the CSV (proportions or total)')
parser.add_argument('repos_path', type=str, help='The path for the file that contains the cloned repo')
args = parser.parse_args()

def write_counts(args, commit_counts, days_of_week, branch):
     # Calculate and write the commit counts in a CSV file
    file= branch + 'DayCounts.csv'
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_row = ['Day'] + [f'{year}-{year+args.interval-1}' for year in range(args.start_year, args.end_year+1, args.interval)]
        # header_row = ['Day'] + ['{}-{}'.format(year, year+args.interval-1) for year in range(args.start_year, args.end_year+1, args.interval)]
        writer.writerow(header_row)

        for day_index, day in enumerate(days_of_week):
            writer.writerow([day] + [str(count) for count in commit_counts[day_index]])

def write_proportions(args, commit_counts, days_of_week, num_of_periods, branch):
     # Calculate and write the commit percentages in a CSV file
    file= branch + 'DayPercentages.csv'
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header_row = ['Day'] + [f'{year}-{year+args.interval-1}' for year in range(args.start_year, args.end_year+1, args.interval)]
        #header_row = ['Day'] + ['{}-{}'.format(year, year+args.interval-1) for year in range(args.start_year, args.end_year+1, args.interval)]
        writer.writerow(header_row)

        for day_index, day in enumerate(days_of_week):
            percentages = []
            for interval in range(num_of_periods):
                total_commits_interval = sum(commit_counts[other_day][interval] for other_day in range(len(days_of_week)))
                percentage = commit_counts[day_index][interval] / total_commits_interval * 100 if total_commits_interval != 0 else 0
                percentages.append(percentage)
            writer.writerow([day] + percentages)


# Handle invalid arguments for start and end year
if args.start_year > args.end_year:
    parser.error("Invalid arguments: start_year must be before end_year")

# Handle invalid argument for interval
if args.interval <= 0:
    parser.error("Invalid argument: interval must be a positive integer")

# Create a list containing every week day
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Calculate the number of periods
num_of_periods = (args.end_year - args.start_year + 1) // args.interval
commit_counts = defaultdict(lambda: [0] * num_of_periods)
repository= 'unix-history-repo'
branches = ['Research-V7-Snapshot-Development', 'BSD-4_3-Snapshot-Development']
repo_path = os.path.join(args.repos_path, repository)
repo = Repo(repo_path)
for branch in branches:
    repo.git.checkout(branch)
    # Iterate through every commit
    for commit in repo.iter_commits():
        commit_year = commit.authored_datetime.year
        # Handle commits in the specified range
        if args.start_year <= commit_year <= args.end_year:
            day_index = commit.authored_datetime.weekday() # Get the index of the day the commit was made
            # Calculate the column where the specific commit will be added in the CSV
            interval_index = (commit_year - args.start_year) // args.interval
            # Handle cases where commit year is outside the specified range
            if interval_index < 0 or interval_index >= num_of_periods:
                parser.error("Invalid arguments given")
            if 0 <= interval_index < num_of_periods:
                commit_counts[day_index][interval_index] += 1
    if args.contents == 'proportions':
        write_proportions(args, commit_counts, days_of_week, num_of_periods, branch)
    else:
        write_counts(args, commit_counts, days_of_week, branch)
