
from collections import defaultdict
from git import Repo
import argparse
import os
import re
parser = argparse.ArgumentParser(description='Counts the average number of inserted lines per year')
parser.add_argument('start_year', type=int, help='The year commit counting starts')
parser.add_argument('end_year', type=int, help='The year commit counting stops')
parser.add_argument('repos', type=str, help='Directory containing repository names')
parser.add_argument('repos_path', type=str, help='The path for the file that contains the cloned repos')
args = parser.parse_args()

# Read the file and split the lines to get repository names
with open(args.repos, 'r') as file:
    repo_list = [line.strip() for line in file.readlines()]

# Calculate the number of periods
num_of_periods = args.end_year - args.start_year + 1

inserted_lines_per_year = defaultdict(int)
commits_per_year = defaultdict(int)

for repository in repo_list:
    non_utc0_commits = defaultdict(bool)
    print(repository)
    repo_path = os.path.join(args.repos_path, repository)
    repo = Repo(repo_path)

    # Iterate through every commit
    for commit in repo.iter_commits():
        contributor = commit.author.email
        if commit.authored_datetime.strftime('%z') != "+0000":
            non_utc0_commits[contributor] = True
            
        if non_utc0_commits[contributor] == True:
            result = repo.git.log("-1",commit, "--stat")

            # Use regex to find lines that match the desired pattern and extract insertions count
            # for the --stat sum-up line
            pattern = r'(\d+ file[s]? changed), (\d+) insertions\(\+\)'
            match_string = re.search(pattern, result)

            # zero inserted lines
            if match_string is None:
                insertions_counts=0
            # Extract the insertions number from the matched patterns
            else:
                insertions_counts = match_string.group(2)
            
            

            year = commit.authored_datetime.year
            if year <= args.end_year and year >= args.start_year:
                inserted_lines_per_year[year] += int(insertions_counts)
                commits_per_year[year] += 1

# Write the dictionary to a text file
with open('inserted_lines_per_year.txt', 'w') as file:
    for year, insertions in inserted_lines_per_year.items():
        file.write(f"{year}: {insertions/commits_per_year[year]}\n")
        

    
