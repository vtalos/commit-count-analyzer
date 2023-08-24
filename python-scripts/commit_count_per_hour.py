from collections import defaultdict
from git import Repo
import argparse
import csv
import sys
import os
from datetime import time


parser = argparse.ArgumentParser(description='Creates a CSV containing the commit count per hour'
                                             'for a given interval and repository')
parser.add_argument('start_year', type=int, help='The year commit counting starts')
parser.add_argument('end_year', type=int, help='The year commit counting stops')
parser.add_argument('interval', type=int, help='How many years a single interval contains')
parser.add_argument('contents', type=str, choices=["proportions", "total"],
                    help='The contents of the CSV (proportions or total)')
parser.add_argument('--repos', type=str, default='repos', help='Directory containing repositories')
args = parser.parse_args()

if args.start_year > args.end_year:
    parser.error("Invalid arguments: start_year must be before end_year")

if args.interval <= 0:
    parser.error("Invalid argument: interval must be a positive integer")

repo_list = [f for f in os.listdir(args.repos) if os.path.isdir(os.path.join(args.repos, f))]

num_of_periods = (args.end_year - args.start_year + 1) // args.interval
commit_counts = defaultdict(lambda: [0] * num_of_periods)

for repository in repo_list:
    repo_path = os.path.join(args.repos, repository)
    repo = Repo(repo_path)

    for commit in repo.iter_commits():
        commit_year = commit.authored_datetime.year

        if args.start_year <= commit_year <= args.end_year:
            commit_time = commit.authored_datetime.time()
            hour_index = commit_time.hour
            interval_index = (commit_year - args.start_year) // args.interval

            if 0 <= interval_index < num_of_periods:
                commit_counts[hour_index][interval_index] += 1            