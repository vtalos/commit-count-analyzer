import csv,subprocess,argparse,sys,re,os
from collections import defaultdict

parser= argparse.ArgumentParser(description='Creates a csv for the commits per day of the week' \
'for given interval and repositories')
parser.add_argument('start_year', help='The year commit counting starts')
parser.add_argument('end_year', help='The year commit counting stops')
parser.add_argument('interval', help='How many years a single interval contains')

repo_paths = []

# Regular expression pattern
pattern = re.compile(r'.*\.git.*')

for root, dirs, files in os.walk('.'):
    for dir_name in dirs:
        if re.match(pattern, dir_name): 
            repo_paths.append(dir_name)

 # Define the days of the week
days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

#how many years an interval has
interval= int(sys.argv[3])
capacity=round(((int(sys.argv[2])+1)-int(sys.argv[1]))/interval)
# Initialize dictionaries to store the commit counts and total commits per week
commit_counts = defaultdict(lambda: [0] * capacity)
percentages = defaultdict(lambda: [0] * capacity)

# Iterate over the repositories
for repo_path in repo_paths:
    
    # Define the start and end years for the interval
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])

    # Iterate over the years in the interval
    while start_year+interval-1 <= end_year:
        print(start_year+interval-1 )
        # Execute the git log command to retrieve the commit timestamps
        cmd = f'git -C {repo_path} log --all --since="{start_year}-01-01" --until="{start_year + interval}-01-01" --format="%cd" --date=format:"%a"'
        output = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')

        # Count the commits per day within the interval and update total commits per week
        for timestamp in output:
            day = timestamp.strip()
            commit_counts[day][(start_year - 2000)//interval] += 1
        start_year += interval

    # Write the commit counts to a CSV file
with open('CommitCountsOverall.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Day'] + [f'{year}-{year+interval}' for year in range(int(sys.argv[1]), end_year+1, interval)])  # Write the year intervals as the first row
    for day in days_of_week:
        writer.writerow([day] + commit_counts[day])

# Calculate and write the commit percentages to a new CSV file
with open('CommitPercentagesOverall.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Day'] + [f'{year}-{year+4}' for year in range(int(sys.argv[1]), end_year+1, interval)])  # Write the year intervals as the first row
    for day in days_of_week:
        percentages = []  # Create an empty list to store the percentages for the current day
        for interval in range(5):
            total_commits_week = sum(commit_counts[other_day][interval] for other_day in days_of_week)
            percentage = commit_counts[day][interval] / total_commits_week * 100 if total_commits_week != 0 else 0
            percentages.append(percentage)  # Append each percentage as a separate element
        writer.writerow([day] + percentages)  # Write the day and the list of percentages to the CSV file