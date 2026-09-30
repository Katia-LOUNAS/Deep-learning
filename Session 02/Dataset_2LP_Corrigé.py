# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 12:50:25 2025

@author: Uzarralde
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles

# Génération des données
X, y = make_circles(n_samples=100, noise=0.1, factor=0.3, random_state=0)

# Affichage des dimensions
print('Dimensions de X:', X.shape)
print('Dimensions de y:', y.shape)

# Correction du scatter plot
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='summer')
plt.show()
#parametres = neural_network(X, y, n1= ?, n_iter= ?, learning_rate= ? )
# n1 = number of neurons
