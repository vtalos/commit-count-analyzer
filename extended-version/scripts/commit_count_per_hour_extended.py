from collections import defaultdict
from git import Repo
import argparse
import csv
import os
from datetime import time


parser = argparse.ArgumentParser(description='Creates a CSV containing the commit count per hour'
                                             'for a given interval and repository')
parser.add_argument('start_year', type=int, help='The year commit counting starts')
parser.add_argument('end_year', type=int, help='The year commit counting stops')
parser.add_argument('interval', type=int, help='How many years a single interval contains')
parser.add_argument('contents', type=str, choices=["proportions", "total"],
                    help='The contents of the CSV (proportions or total)')
parser.add_argument('repos_path', type=str, help='The path for the file that contains the cloned repo')

args = parser.parse_args()


def write_counts(args, commit_counts, branch):
    # Calculate and write the commit counts in a CSV file
    file= branch + 'HourCounts.csv'
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        hours = [time(hour=h) for h in range(24)]
        header_row = ['Hour'] + [f'{year}-{year+args.interval-1}' for year in range(args.start_year, args.end_year+1, args.interval)]
        writer.writerow(header_row)

        for hour_index, hour in enumerate(hours):
            writer.writerow([hour.strftime('%H:%M')] + [str(count) for count in commit_counts[hour_index]])

def write_proportions(args, commit_counts, branch):
    # Calculate and write the commit percentages in a CSV file
    file= branch + 'HourPercentages.csv'
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        hours = [time(hour=h) for h in range(24)]
        header_row = ['Hour'] + [f'{year}-{year+args.interval-1}' for year in range(args.start_year, args.end_year+1, args.interval)]
        writer.writerow(header_row)

        for hour_index, hour in enumerate(hours):
            percentages = []
            for interval in range(num_of_periods):
                total_commits_interval = sum(commit_counts[other_hour][interval] for other_hour in range(24))
                percentage = commit_counts[hour_index][interval] / total_commits_interval * 100 if total_commits_interval != 0 else 0
                percentages.append(percentage)
            writer.writerow([hour.strftime('%H:%M')] + percentages)

# Check argument validity
if args.start_year > args.end_year:
    parser.error("Invalid arguments: start_year must be before end_year")

if args.interval <= 0:
    parser.error("Invalid argument: interval must be a positive integer")

# Calculate the number of periods
num_of_periods = (args.end_year - args.start_year + 1) // args.interval
commit_counts = defaultdict(lambda: [0] * num_of_periods)

# Count total commits for all repos
repository = 'unix-history-repo'
branches = ['Research-V7-Snapshot-Development', 'BSD-4_3-Snapshot-Development']
repo_path = os.path.join(args.repos_path, repository)
repo = Repo(repo_path)
for branch in branches:
    repo.git.checkout(branch)
    # Iterate through every commit
    for commit in repo.iter_commits():
        commit_year = commit.authored_datetime.year

        # Get the commits in the requested range
        if args.start_year <= commit_year <= args.end_year:
            commit_time = commit.authored_datetime.time()
            hour_index = commit_time.hour
            interval_index = (commit_year - args.start_year) // args.interval

            # Handle cases where commit year is outside the specified range
            if interval_index < 0 or interval_index >= num_of_periods:
                parser.error("Invalid arguments given")

            # Increase the commit count in the current hour and period by 1
            if 0 <= interval_index < num_of_periods:
                commit_counts[hour_index][interval_index] += 1
    if args.contents == 'proportions':
        write_proportions(args, commit_counts, branch)
    else:
        write_counts(args, commit_counts, branch)  
