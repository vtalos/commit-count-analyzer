import os
import numpy as np

# Function to calculate standard deviation
def calculate_std_dev(data):
    return np.std(data)

# Function to read commits data from file
def read_commits_data(filename):
    with open(filename, 'r') as file:
        next(file)
        commits_data = [int(line.strip().split(': ')[1]) for line in file]
    return commits_data

# Directory containing the commit files
directory = './commits_data/'

# Create a file to write the results
output_file = open("std_dev_results.txt", "w")

# Iterate over each file
for filename in os.listdir(directory):
    if filename.startswith("commits_by_timezone_") and filename.endswith(".txt"):
        year = int(filename.split("_")[3].split(".")[0])
        commits_data = read_commits_data(os.path.join(directory, filename))
        std_dev = calculate_std_dev(commits_data)
        
        output_file.write(f"Year: {year}, Standard Deviation: {std_dev}\n")

output_file.close()