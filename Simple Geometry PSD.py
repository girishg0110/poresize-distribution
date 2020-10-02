# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:19:39 2020

@author: giris
"""

import numpy as np
from matplotlib import pyplot as plt

# Point Generation
def generateLattice(density, inGeometry):
    # Input - number of lattice points on x-axis
    # Output - np vector of lattice points that fit within geometry --> within 2-cube
    
    grid = np.zeros((density**3, 3))
    
    t = 0
    for x in np.linspace(-1,1,density):
        for y in np.linspace(-1,1,density):
            for z in np.linspace(-1,1,density):
                if (inGeometry(x,y,z)): 
                    grid[t] = np.array([x,y,z])
                    t += 1
                
    return grid[:t]

# Pore Geometries
def spherical(x,y,z):
    return x**2+y**2+z**2<=1
def cylindrical(x,y,z):
    return x**2+y**2<=1

# Distributions

def psdCumulativeDistribution(poreSizes, probInterval, normalize=False):
    distribution = np.zeros((probInterval,2))
    t=0
    for thresh in np.linspace(0,2,probInterval):
        poreSizes = poreSizes[poreSizes>=thresh]
        distribution[t]=thresh, poreSizes.shape[0]
        t+=1
        
    if (normalize):
        distribution /= np.mean(distribution, axis=1)
        
    return distribution

def psdProbDensity(poreSizes, probInterval, normalize=False):
    distribution = np.zeros((probInterval,2))
    t=0
    for thresh in np.linspace(0,2,probInterval):
        subPoreSizes = poreSizes[poreSizes>=thresh]
        distribution[t]=thresh, poreSizes.shape[0]
        t+=1
        
    if (normalize):
        distribution /= np.mean(distribution, axis=1)
        
    return distribution

# Helper Methods
def maxPoreSize(point):
    return 1+np.linalg.norm(point)

# Driver Methods
def poreSizeCalculation(poreLocations):
    poreSizes = np.zeros((poreLocations.shape[0]))
    t = 0
    for coord in poreLocations:
        poreSizes[t]=maxPoreSize(coord)
        t+=1
    return poreSizes

def psdPlot(distFunction, pointGeneration, pointDensity, probInterval):
    grid = pointGeneration(pointDensity)
    poreSizes = poreSizeCalculation(grid)
    distro = distFunction(poreSizes, probInterval)
    plt.plot(distro)
    print(discreteGradient(distro))
    plt.plot(range(distro.shape[0]), discreteGradient(distro))
    return distro
    
def discreteGradient(probDist):
    grad = np.zeros((probDist.shape[0]))
    for p in range(1, probDist.shape[0]):
        grad[p]=probDist[p][1]-probDist[p-1][1]
    return grad
        