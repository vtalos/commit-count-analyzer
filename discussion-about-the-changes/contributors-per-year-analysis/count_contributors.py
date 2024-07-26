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
parser.add_argument('repos', type=str, help='Directory containing repository names')
parser.add_argument('repos_path', type=str, help='The path for the file that contains the cloned repos')

args = parser.parse_args()


# Read the file and split the lines to get repository names
with open(args.repos, 'r') as file:
    repo_list = [line.strip() for line in file.readlines()]

# Calculate the number of periods
num_of_periods = (args.end_year - args.start_year + 1) // args.interval

contributors_per_year = defaultdict(int)
commit_counts = defaultdict(lambda: [0] * num_of_periods)


# Count total commits for all repos
for repository in repo_list:
    non_utc0_commits = defaultdict(bool)
    print(repository)
    repo_path = os.path.join(args.repos_path, repository)
    repo = Repo(repo_path)

    # Iterate through every commit
    for commit in repo.iter_commits():
        contributor = commit.author.email

        #change value just for the first occurence, to count contributors properly
        if commit.authored_datetime.strftime('%z') != "+0000" and non_utc0_commits[contributor] == False:
            non_utc0_commits[contributor] = True
            year=commit.authored_datetime.year
            if year <= args.end_year and year >= args.start_year:
                contributors_per_year[year] += 1

# Write the dictionary to a text file
with open('contributors_per_year.txt', 'w') as file:
    for year, contributors in contributors_per_year.items():
        file.write(f"{year}: {contributors}\n")

