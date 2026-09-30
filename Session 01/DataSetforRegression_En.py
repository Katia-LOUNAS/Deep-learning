# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
plt.rcParams["figure.figsize"] = [12,12]
 
#plt.figure(figsize=(12,12))
 
 
np.random.seed(0)
#DataSet_Given by :  y = f(x)  avec f(x) = x^4 + bx^3 + c 
 
x = np.random.normal(10, 2, 500)
y = x ** 4 + np.random.uniform(-1, 1,500)*(x ** 3) + np.random.uniform(0, 1,500)
 
plt.scatter(x,y)
plt.show()

