import numpy as np
import argparse


parser = argparse.ArgumentParser(description="A script for calculating Cohen's h between two time periods for a specific day")
parser.add_argument("filename", help="The txt file to get the data from")
args = parser.parse_args()

def read_data(filename):
    data = {}
    with open(filename, 'r') as file:
        for line in file:
            year, value = line.split(': ')
            data[int(year)] = float(value)
    return data

def calculate_cohens_h(data, group1_years, group2_years):
    group1 = [data[year] for year in group1_years]
    group2 = [data[year] for year in group2_years]

    mean1 = np.mean(group1)
    mean2 = np.mean(group2)

    sd1 = np.std(group1, ddof=1)  
    sd2 = np.std(group2, ddof=1)

    pooled_sd = np.sqrt((sd1**2 + sd2**2) / 2)
    cohens_h = (mean2 - mean1) / pooled_sd

    return cohens_h

def main():
    filename = args.filename
    data = read_data(filename)

    group1_years = range(2004, 2014)  
    group2_years = range(2014, 2024)  

    cohens_h = calculate_cohens_h(data, group1_years, group2_years)
    
    print(f"Cohen's h: {cohens_h:.4f}")

if __name__ == "__main__":
    main()
