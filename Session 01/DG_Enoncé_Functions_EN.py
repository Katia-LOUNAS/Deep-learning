
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 15:29:19 2024

@author: pierre
"""

def f(x):
    return (x-1)**2+(1/x-2)**2

def df(x):
    return 2*(x-1) + 2*(1/x-2)*(-1/x**2)

def descente1(f, df, a, alpha=1e-2, eps=1e-9, maxIter=1000):
    # Find the minimum of a function f by gradient descent
    # df must be the derivative of f
    # uses the analytical derivative of f, which is provided by df
    # a is the initial value
    # alpha is the learning rate which determines the speed of descent (default 1/100)
    # eps is the desired precision (default 1/1000000000)
    # maxIter is the maximum number of iterations (default 1000)
    

    return a

def descente2(f, a, lr=1e-2, eps=1e-9, maxIter=1000):
    # find the minimum of a function f by gradient descent with numerical derivative
    # uses a numerical approximation of this derivative
    # a is the initial value
    # alpha is the learning rate which determines the speed of descent (default 1/100)
    # eps is the desired precision (default 1/1000000000)
    # maxIter is the maximum number of iterations (default 1000)    
    



    return a



print(descente1(f, df, 1))

print(descente2(f, 1))