import matplotlib.pyplot as plt
import networkx as nx
import os
import json
import GraphFunctions as gh
import imp
import math
import numpy as np
import itertools as it
import string
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import generators

# locations of data
data_folder = os.path.join('..','data')
graph_folder = os.path.join('..','graphs')

# loading data
def loadCleaned(path = os.path.join(data_folder,'cleaned.json')):
    """Loads the cleaned data"""
    with open(path, 'rt') as fp:
        return json.load(fp)
def loadNumbersToPage (path = os.path.join(data_folder,'number_to_page.json')):
    with open(path, 'rt') as fp:
        return json.load(fp)
def loadPageToNumbers(path = os.path.join(data_folder,'page_to_number.json')):
    with open(path, 'rt') as fp:
        return json.load(fp)

# check any problems in loading the data
assert len(cleaned) == 77432

# graph utils

def resize_alpha(size, p1, p2, max):
    """
    given size and max s.t. \'size\' <= \'max\', returns a different size depending on the relative position of size  w.r.t \'p1\' and \'p2\'
    """
    if size <= p1:
        return math.pow(size/max, 4)
    elif p1 <= size <= p2:
        return size / max
    else:
        return math.pow(size/max, 1/4)

def resize(size, p1, p2):
    """
    given \'size\' returns a different size depending on the relative position of size w.r.t \'p1\' and \'p2\'
    """
    if size <= p1:
        return .2 * size
    elif p1 <= size <= p2:
        return .4 * size
    else:
        return 1.2* size


