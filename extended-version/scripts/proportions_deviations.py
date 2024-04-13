import os

def read_commit_data(filename):
    """
    Reads commit data from a file and returns it as a dictionary.

    Args:
    - filename: Name of the file containing commit data

    Returns:
    - commit_data: A dictionary where keys are timezones and values are commit counts
    """
    commit_data = {}
    total_commits = 0  # Total number of commits for the year
    with open(filename, 'r') as file:
        next(file)
        for line in file:
            timezone, commits = line.strip().split(':')
            commits = int(commits)
            commit_data[int(timezone)] = commits
            total_commits += commits
    return commit_data, total_commits

def calculate_proportions(commit_data):
    """
    Calculates the proportions of commits for each timezone within a year.

    Args:
    - commit_data: Dictionary containing commit data for a year

    Returns:
    - proportions: A dictionary where keys are timezones and values are proportions of commits
    """
    total_commits = sum(commit_data.values())
    proportions = {timezone: commits / total_commits for timezone, commits in commit_data.items()}
    return proportions

def calculate_deviation(current_data, previous_data):
    """
    Calculates the deviation in commit proportions between the current year and the previous year.

    Args:
    - current_data: Dictionary containing commit proportions for the current year
    - previous_data: Dictionary containing commit proportions for the previous year

    Returns:
    - deviation: A dictionary where keys are timezones and values are deviations in commit proportions
    """
    deviation = {}
    for timezone, proportion in current_data.items():
        if timezone in previous_data:
            deviation[timezone] = proportion - previous_data[timezone]
        else:
            deviation[timezone] = proportion
    return deviation

def main():
    # Define the range of years to iterate over
    years = range(2004, 2024)
    previous_data = None
    for year in years:
        filename = f'commits-data/commits_by_timezone_{year}.txt'
        if not os.path.exists(filename):
            print(f"File {filename} not found. Skipping...")
            continue
        current_commit_data, current_total_commits = read_commit_data(filename)
        current_proportions = calculate_proportions(current_commit_data)
        
        if previous_data:
            deviation = calculate_deviation(current_proportions, previous_data)
            print(f'Deviation in commit proportions for {year}: {deviation}')
        previous_data = current_proportions

if __name__ == "__main__":
    main()