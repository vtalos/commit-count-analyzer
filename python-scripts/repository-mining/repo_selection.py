import csv
import subprocess
import re
import urllib
import requests
import os
import datetime
import time
import calendar
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description='Given the CSV from GHS, returns the repos '
        'that must be mined')
parser.add_argument('num_threads', type=int, help='The number of threads that will filter the repos')
parser.add_argument('file_input', type=str, help='The CSV from GHS that fits our criteria')
parser.add_argument('file_output', help='The txt file that contains the repos to be mined', default='script_results.txt')
args = parser.parse_args()

def monthly_commit_count(project, sha='master', token=None):

    # PAT
    token = token or os.environ.get('GITHUB_API_TOKEN')

   # project commits url
    url = f'https://api.github.com/repos/{project}/commits'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'token {token}',
    }
    params = {
        'sha': sha,
        'per_page': 1, # 1 page per commit
    }
    years=list(range(2004,2023))
    months = range(1,13)
    per_month = 1 # Count commits per one month
    not_dense = 0 # The number of months that have under 100 commits
    for year in years:
        for month in months:
            start_date = datetime.datetime(int(year), int(month), 1)
            params['since'] = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            _, days_in_month = calendar.monthrange(year, month)
            end_date = start_date + datetime.timedelta(days_in_month)
            params['until'] = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')

            resp = requests.request('GET', url, params=params, headers=headers)

            if (resp.status_code // 100) != 2:
                raise Exception(f'invalid github response: {resp.content}')
            # check the resp count, just in case there are 0 commits
            commit_count = len(resp.json())
            last_page = resp.links.get('last')
            # if there are no more pages, the count must be 0 or 1
            if last_page:
                # extract the query string from the last page url
                qs = urllib.parse.urlparse(last_page['url']).query
                # extract the page number from the query string
                commit_count = int(dict(urllib.parse.parse_qsl(qs))['page'])  # Get the number of commits by the last page
            if commit_count < 100:
                not_dense = not_dense + 1 # if this month has under 100 commits, increase the not_dence months by one
    return not_dense




def enough_contributors(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    # Redo the request, so the status code 202 may change to 200.
    # Don't do the request more than 4 times
    j = 0
    while response.status_code == 202 and j <= 4:
        time.sleep(5)
        response = requests.get(url, headers=headers)
        j = + 1

    contributors = []
    page = 1
    per_page = 100
    while True:
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            contributors += response.json()
            if page > 2:
                return True
            if len(response.json()) < per_page:
                break
            page += 1
            time.sleep(1)
        else:
            print("Failed to retrieve contributors:", response.status_code)
            break
    return False

def get_contributors_years(owner, repo):
    """Receives the owner of a repo and the repo 
    name and return the timestamp of the first commit """

    url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    #Redo the request, so the status code 202 may change to 200.
    #Don't do the request more than 4 times
    j=0
    while response.status_code == 202 and j<=4:
        time.sleep(5)
        response=requests.get(url, headers=headers)
        j =+ 1

    if response.status_code == 200:
        contributors = response.json()
        #retrieves the data of the first commit in the repo

        for contributor in contributors:
            weeks = contributor["weeks"]
            first_week = weeks[0]
            first_commit_date = datetime.datetime.fromtimestamp(first_week["w"])
        return first_commit_date
    
    if response.status_code == 202:
        print("Status code 202")
        # Returns March 18, 2022. It is a random date that will not fit 
        # the condition in order to be appended to the filtered_repos list
        return datetime.datetime.fromtimestamp(1647768000)   
    
def process_chunk(chunk,auth_token):
    for repo in chunk:
        repo_url = 'https://github.com/' + repo
        print(repo)
        process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        sha = re.split(r'\t+', stdout.decode('utf-8'))[0]
        owner = repo.split("/")[0]
        repo_name = repo.split("/")[1]
        year = get_contributors_years(owner, repo_name)
        if year== None:
            print(repo)
        if year < datetime.datetime(2005, 1, 1) and enough_contributors(owner, repo_name) :
            if monthly_commit_count(repo, sha, auth_token) < 20 :
                final_repos.append(repo)
    return final_repos

start_time = time.time()
repos = []
filtered_repos = []
final_repos = []
auth_token = 'GITHUB_TOKEN'
file= args.file_input
n_threads=args.num_threads
# reads the csv file that contains the repositories from Github Search mining tool
with open(file, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        repo = row[1]
        repos.append(repo)
file.close()

# Split the data into chunks.
chunks = [repos[i:i + len(repos) // n_threads] for i in range(0, len(repos), len(repos) // n_threads)]
# Create a thread pool
executor = ThreadPoolExecutor(max_workers=args.num_threads)
# Submit the chunks to the thread pool for processing.
results = []
for chunk in chunks:
  future = executor.submit(process_chunk, chunk, auth_token)
  results.append(future)
# Wait for all of the chunks to finish processing.
for future in results:
  try:
    result = future.result()
  except Exception as e:
    print(e)
    if args.file_output:
        file = args.file_output
    else:
        file= 'script_results.txt'
  else:
      if file in dir:
          with open(file, "r") as f:
            data = f.read()
            if len(data)>0:
                f.truncate(0)
      with open(file, "w") as file:
            file.write(f"{result}\n")
            file.close()

# Close the thread pool.
executor.shutdown(wait=True)
end_time = time.time()
# Calculate the execution time in seconds.
execution_time = end_time - start_time

# Print the execution time.
print(f"Execution time: {execution_time:.2f} seconds")

          