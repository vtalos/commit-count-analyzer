from collections import defaultdict
from git import Repo
import argparse
import os
import subprocess
import re

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('start_year', type=int, help='The year commit counting starts')
parser.add_argument('end_year', type=int, help='The year commit counting stops')
parser.add_argument('repos', type=str, help='File containing repository names')
parser.add_argument('repos_path', type=str, help='Path to the directory containing cloned repos')

args = parser.parse_args()

# Validate arguments
if args.start_year > args.end_year:
    parser.error("Invalid arguments: start_year must be before end_year")

# Read repository list
with open(args.repos, 'r') as file:
    repo_list = [line.strip() for line in file]

def count_inserted_lines(commit_hash):
    try:
        result = subprocess.run(
            ['git', 'log', '-p', '--pretty=full', commit_hash],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
        inserted_lines = len(re.findall(r'^\+[^+]', output, re.MULTILINE))
        return inserted_lines
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving commit info: {e}")
        return 0

def save_commit_details(repo, inserted_lines, contributor_name, year):
    with open('git_log.txt', 'a') as f:
        f.write(f'{repo} {inserted_lines} {contributor_name} {year}\n')

# Process each repository
for repository in repo_list:
    print(f"Processing repository: {repository}")
    repo_path = os.path.join(args.repos_path, repository)
    repo = Repo(repo_path)

    non_utc0_commits = defaultdict(lambda: False)
    
    # Iterate through commits once to check for non-UTC0
    for commit in repo.iter_commits():
        contributor = commit.author.name
        year = commit.authored_datetime.year
        if commit.authored_datetime.strftime('%z') != "+0000":
            non_utc0_commits[(contributor, year)] = True

    # Iterate through commits again to process those flagged as non-UTC0
    for commit in repo.iter_commits():
        contributor = commit.author.name
        year = commit.authored_datetime.year
        if non_utc0_commits[(contributor, year)]:
            inserted_lines = count_inserted_lines(commit.hexsha)
            save_commit_details(repository, inserted_lines, commit.author.name, year)
