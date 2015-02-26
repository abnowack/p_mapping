# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 12:49:11 2015

@author: Aaron
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mcnp_wrapper import *
from fission_display import *

def radial_bins(r, n):
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

input_card = \
"""First Attempt at P Mapping Input Deck
C CELL CARDS
10 100 -18.74 -1
20 0          -1

C SURFACE CARDS
1 SO {RADIUS}

M100 92235 {F235} 92238 {F238}
MODE N
IMP:N 1 0
PHYS:N 100 0 0 J J J 0 -1 J J J 0 0
FMULT 92235 METHOD=5
NPS {NPS}
PTRAC FILE=ASC WRITE=ALL MAX=50000000
C UNFIROMLY SAMPLING IN SPHERE
SDEF ERG=2.0 POS=0 0 0 RAD=D1 CEL=10
SI1 0 {RADIUS}
SP1 -21 2
RAND SEED={SEED}
"""

enrichment = [0.935, 0.90, 0.80, 0.70, 0.60]
colors = ['b', 'g', 'r', 'c', 'm']
params = {'NPS': 100000, 'RADIUS': 5.0, 'F235': 0.9, 'F238': 0.1, 
          'SEED': 8675309}
          
n_radial_bins = 20
n_phi_bins = 20

radial_bins = radial_bins(params['RADIUS'], n_radial_bins)
phi_bins = np.linspace(0, 2*np.pi, n_phi_bins)
radial_mesh, phi_mesh = np.meshgrid(radial_bins, phi_bins)

nbins = n_radial_bins * n_phi_bins

fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))

with run_mcnp(input_card, params=params, cores=4) as (status, mcnp_dir):  
    fissions, nhistory = parse_ptrac_fissions(mcnp_dir + '\\ptrac')
    r = np.sqrt(fissions[:, 0]**2. + fissions[:, 1]**2. + fissions[:, 2]**2.)
    phi = np.arctan2(fissions[:,1], fissions[:,0]) + np.pi
    
    hist, xedges, yedges = np.histogram2d(r, phi, bins=[radial_bins, phi_bins])
    
    hist = hist / float(nhistory) * nbins
    
    print radial_mesh.shape, phi_mesh.shape, hist.shape
    
    quadmesh = ax.pcolormesh(yedges, xedges, hist)
    
#    plt.plot(ubins, np.concatenate([norm_vals, [norm_vals[-1]]]), drawstyle='steps-post')
    
    print fissions.shape[0] / float(nhistory)

#plt.ylim(ymin=0)
#plt.xlabel('Radius (cm)')
#plt.ylabel('p (fission probability)')
#plt.legend(loc='best')
plt.colorbar(quadmesh,ax=ax)
plt.show()