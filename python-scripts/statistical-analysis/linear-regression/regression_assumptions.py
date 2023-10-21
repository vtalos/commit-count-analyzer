import csv
from itertools import tee
import numpy as np
import sys
import argparse
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
import scipy.stats as stats
import statsmodels.api as sm

parser = argparse.ArgumentParser(description="A script for checking if linear regression assumptions are meeted for a set of data")

parser.add_argument("filename", help="The csv file to get the data from")
parser.add_argument("day", help="The day of the week to implement the linear regression")

filename = sys.argv[1] # The first argument is the filename
week_day = sys.argv[2] # The second argument is the day of the week