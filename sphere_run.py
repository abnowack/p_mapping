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
    c = r / (n**(1./3.))
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
    
with open('input_cards/sphere.i', 'r') as cardfile:
    card = cardfile.read()

enrichment = [0.935, 0.90, 0.80, 0.70, 0.60]
colors = ['b', 'g', 'r', 'c', 'm']
params = {'NPS': 10000, 'RADIUS': 5.0, 'F235': 0.9, 'F238': 0.1, 
          'SEED': 8675309}
nbins = 20

ubins = uniform_bins(params['RADIUS'], nbins)

for i, enrich in enumerate(enrichment):
    with run_mcnp(card, params=params, cores=4) as (status, mcnp_dir):
        # update params
        params['F235'], params['F238'] = enrich, 1. - enrich
        params['SEED'] += 2
        label_str = '{:.2%} U235'.format(enrich) 
        
        fissions, nhistory = parse_ptrac_fissions(mcnp_dir + '\\ptrac')
        r = np.sqrt(fissions[:, 0]**2. + fissions[:, 1]**2. + fissions[:, 2]**2.) 
        
        vals = np.histogram(r, bins=ubins)[0].astype(float)
        error = np.sqrt(vals) / float(nhistory) * nbins
        norm_vals = vals / float(nhistory) * nbins
        
        plt.plot(ubins, np.concatenate([norm_vals, [norm_vals[-1]]]), drawstyle='steps-post', color=colors[i], label=label_str)
        plt.errorbar((ubins[1:] + ubins[:-1])/2., norm_vals, yerr=error, fmt='none', ecolor=colors[i])
        
        print fissions.shape[0] / float(nhistory)

plt.ylim(ymin=0)
plt.xlabel('Radius (cm)')
plt.ylabel('p (fission probability)')
plt.legend(loc='best')
plt.show()