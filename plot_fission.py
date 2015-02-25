# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 11:19:05 2015

@author: Aaron
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def uniform_bins(r, n):
    c = (r / n)**(1./3.)
    bins = np.ndarray((n+1))
    for i in xrange(len(bins)):
        bins[i] = c * np.power(i, 1./3.)
    return bins

def plot_radial_bins(r, radius, nbins, nps, *args, **kwargs):
    ubins = uniform_bins(radius, nbins)
    vals = np.histogram(r, bins=ubins)[0]
    vals = vals.astype(float) / nps * nbins
    plt.plot(ubins, np.concatenate([vals, [vals[-1]]]), drawstyle='steps-post', color='b', alpha=0.5)
#    error = np.sqrt(bins) / float(nps) / nbins
#    plt.errorbar((edges[1:]+edges[:-1])/2., vals, yerr=error, fmt='none', color='b', alpha=0.5, linewidth=2)
    plt.ylim(ymin=0)
    plt.show()