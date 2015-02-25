# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 13:24:03 2015

@author: Aaron
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mcnp_wrapper import *
from fission_display import *

def uniform_bins(r, n):
    c = (r / n)**(1./3.)
    bins = np.ndarray((n+1))
    for i in xrange(len(bins)):
        bins[i] = c * np.power(i, 1./3.)
    return bins

def plot_radial_bins(r, radius, nbins, nps, *args, **kwargs):
    plot_args = {'color': 'blue', 'alpha': 0.5, 'linewidth': 2}
    eplot_args = {'color': 'blue', 'alpha': 0.5, 'linewidth': 2,
                  'ecolor': 'blue'}
                  
    for key, val in kwargs.iteritems():
        if plot_args.has_key(key):
            plot_args[key] = val
            
    for key, val in kwargs.iteritems():
        if eplot_args.has_key(key):
            eplot_args[key] = val
            
    ubins = uniform_bins(radius, nbins)
    vals = np.histogram(r, bins=ubins)[0].astype(float)
    error = np.sqrt(vals) / float(nps) * nbins
    norm_vals = vals / float(nps) * nbins
    
    plt.plot(ubins, np.concatenate([norm_vals, [norm_vals[-1]]]), drawstyle='steps-post', **plot_args)    
    plt.errorbar((ubins[1:]+ubins[:-1])/2., norm_vals, yerr=error, fmt='none', **eplot_args)

    plt.ylim(ymin=0)
    plt.show()

input_card = \
"""First Attempt at P Mapping Input Deck
C CELL CARDS
10 100 -18.74 -1
20 0          -1

C SURFACE CARDS
1 SO 1.0

M100 92235 0.935 92238 0.065
MODE N
IMP:N 1 0
PHYS:N 100 0 0 J J J 0 -1 J J J 0 0
FMULT 92235 METHOD=5
NPS {NPS}
PTRAC FILE=ASC WRITE=ALL MAX=50000000
C UNFIROMLY SAMPLING IN SPHERE
SDEF ERG=2.0 POS=0 0 0 RAD=D1 CEL=10
SI1 0 1.0
SP1 -21 2

"""

params = {'NPS': 1000000}

with run_mcnp(input_card, params=params) as (status, mcnp_dir):
    fissions, nhistory = parse_ptrac_fissions(mcnp_dir + '\\ptrac')
    r = np.sqrt(fissions[:, 0]**2. + fissions[:, 1]**2. + fissions[:, 2]**2.)
    plot_radial_bins(r, 1.0, 20, nhistory)

    print fissions.shape[0] / float(nhistory)