import pymannkendall as mk
import sys
import argparse
from itertools import tee
import csv

parser = argparse.ArgumentParser(description="A script for implementing Mann Kendall Test")

parser.add_argument("filename", help="The csv file to get the data from")
parser.add_argument("day", help="The day of the week to implement the Mann Kendall Test")

filename = sys.argv[1] # The first argument is the filename
week_day = sys.argv[2] # The second argument is the day of the week
