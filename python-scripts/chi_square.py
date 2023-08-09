import csv
from itertools import tee
from scipy.stats import chi2_contingency
import numpy as np
import sys
import argparse

parser = argparse.ArgumentParser(description="A script for implementing chi square test")

parser.add_argument("filename", help="The csv file to get the data from")
parser.add_argument("day", help="The day of the week to implement the chi square test")
