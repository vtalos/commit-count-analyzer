from git import Repo
import argparse
from collections import defaultdict
import csv

# Handle the arguments
parser = argparse.ArgumentParser(description='Creates a csv containing the commit count per day of the week' \
'for a given interval and repository')
parser.add_argument('start_year', type=int, help='The year commit counting starts')
parser.add_argument('end_year', type=int, help='The year commit counting stops')
parser.add_argument('interval', type=int, help='How many years a single interval contains')
args = parser.parse_args()