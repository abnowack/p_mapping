# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 12:49:11 2015

@author: Aaron

"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mcnpy.mcnp_wrapper import *
from fission_display import *

def radial_bins(r_min, r_max, n):
    bins = np.arange(n+1)
    bins = float(r_min)**2 + bins*(float(r_max)**2-float(r_min)**2)/float(n)
    return np.sqrt(bins) 
  
#with open('input_cards/cylinder_no_reflect.i', 'r') as cardfile:
with open('input_cards/cylinder_reflect.i', 'r') as cardfile:
    card = cardfile.read()

n_radial_bins = 5
n_phi_bins = 20

radial_bins = radial_bins(4.445, 6.35, n_radial_bins)
phi_bins = np.linspace(-np.pi, np.pi, n_phi_bins)
radial_mesh, phi_mesh = np.meshgrid(radial_bins, phi_bins)

nbins = n_radial_bins * n_phi_bins

with run_mcnp(card, cores=4, clean=False) as (status, mcnp_dir):  
    fissions, nhistory = parse_ptrac_fissions(mcnp_dir + '\\ptrac')
    r = np.sqrt(fissions[:, 0]**2. + fissions[:, 1]**2.)
    phi = np.arctan2(fissions[:,1], fissions[:,0])
    
    hist, xedges, yedges = np.histogram2d(r, phi, bins=[radial_bins, phi_bins]) 
    hist = hist / float(nhistory) * nbins

fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
quadmesh = ax.pcolormesh(yedges, xedges, hist)
print fissions.shape[0] / float(nhistory)

plt.colorbar(quadmesh,ax=ax)
plt.show()