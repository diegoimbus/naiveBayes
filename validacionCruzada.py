# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 23:57:35 2018

@author: LONOVO
"""
from scipy.io import arff
import pandas as pd
import math
import numpy as np

#leer el dataset

data = arff.loadarff('clasificacion-drug.arff')
df = pd.DataFrame(data[0])

Drugscrossed = df.sort_values('Drug')