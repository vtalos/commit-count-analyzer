import csv
import numpy as np
import matplotlib.pyplot as plt
from itertools import tee
import sys

filename = sys.argv[1] # The first argument is the file name
day = sys.argv[2] # The second argument is the preferred day
# day list contains the number of commits for each week day in every time period
day = [[] for _ in range(7)]