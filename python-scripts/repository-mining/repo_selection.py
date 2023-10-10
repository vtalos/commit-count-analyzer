import csv
import subprocess
import re
import urllib
import requests
import os
import datetime
import time
import calendar

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



def commit_count(project, sha='master', token=None):
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
        commit_count = int(dict(urllib.parse.parse_qsl(qs))['page']) # Get the number of commits by the last page
    return commit_count

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

repos = []
filtered_repos = []
final_repos = []
auth_token = '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'
# reads the csv file that contains the repositories from Github Search mining tool
with open("github_search_results.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        repo = row[1]
        repos.append(repo)
file.close()

for repo in repos:
    # Get the masters' sha in order to find the number of commits
    repo_url = 'https://github.com/' + repo
    process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    sha = re.split(r'\t+', stdout.decode('utf-8'))[0]
    commit_number = commit_count(repo, sha, auth_token)
    if commit_number > 50000 :
        filtered_repos.append(repo)
    
for repo in filtered_repos:
    repo_url = 'https://github.com/' + repo
    process = subprocess.Popen(["git", "ls-remote", repo_url], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    sha = re.split(r'\t+', stdout.decode('utf-8'))[0]
    owner = repo.split("/")[0]
    repo_name = repo.split("/")[1]
    year = get_contributors_years(owner, repo_name)
    if year < datetime.datetime(2005, 1, 1) and enough_contributors(owner, repo_name) :
        if monthly_commit_count(repo, sha, auth_token) < 20 :
            final_repos.append(repo)
            print(repo)
            