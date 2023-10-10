import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys
import statsmodels.api as sm

filename = sys.argv[1] # The first argument is the file name
time_block = int(sys.argv[2]) # The second argument is the time block to keep for the linear regression
