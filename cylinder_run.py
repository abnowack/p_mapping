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

def radial_bins(r_min, r_max, n):
    bins = np.arange(n+1)
    bins = float(r_min)**2 + bins*(float(r_max)**2-float(r_min)**2)/float(n)
    return np.sqrt(bins)

no_reflector_card = \
"""Cylinder Assembly
C CELL CARDS
10 100  -18.74  -1 2       $ CYLINDER SHELL
20   0         (-3 1 ):-2  $ SURROUNDING MEDIUM
30   0           3         $ NULL SPACE

1 RCC 0 0 0 0 0 10 5 $ OUTER
2 RCC 0 0 0 0 0 10 4 $ INNER
3 SO  100            $ UNIVERSE

M100 92235 0.935 92238 0.065
MODE N
IMP:N 1 1 0
PHYS:N 100 0 0 J J J 0 -1 J J J 0 0
FMULT 92235 METHOD=5
NPS 500000
PTRAC FILE=ASC WRITE=ALL MAX=50000000
C UNFIROMLY SAMPLING IN CYLINDER
SDEF ERG=2.0 AXS=0 0 1 POS=0 0 0 RAD=D1 EXT=D2 CEL=10
SI1 4 5
SP1 -21 2
SI2 0 10
SP2 0 1
RAND SEED=8675309
"""

reflector_card = \
"""Cylinder Assembly
C CELL CARDS
10 100 -18.74  -1 2        $ CYLINDER ASSEMBLY
20   0        (-3 1 4 ):-2 $ SURROUNDING MEDIUM
30 200 -19.25  -4          $ BOX
40   0          3          $ NULL SPACE

1 RCC   0 0 0 0 0 10 5 
2 RCC   0 0 0 0 0 10 4 
3 SO  100 
C 4 RPP  -5 5 5 6 0 10 
4 RPP  -5 5 -6 -5 0 10 

C ENRICHED URANIUM, DENSITY=18.74 G/CM^3
M100 92235 0.935 92238 0.065
C TUNGSTEN, DENSITY=19.25 G/CM^3
M200 074180 0.0012
     074182 0.2650
     074183 0.1431
     074184 0.3064
     074186 0.2843
MODE N
IMP:N 1 1 1 0
PHYS:N 100 0 0 J J J 0 -1 J J J 0 0
FMULT 92235 METHOD=5
NPS 500000
PTRAC FILE=ASC WRITE=ALL MAX=50000000
C UNFIORMLY SAMPLING IN CYLINDER
SDEF ERG=2.0 AXS=0 0 1 POS=0 0 0 RAD=D1 EXT=D2 CEL=10
SI1 4 5
SP1 -21 2
SI2 0 10
SP2 0 1
RAND SEED=8675309
"""
  
n_radial_bins = 5
n_phi_bins = 20

radial_bins = radial_bins(4., 5., n_radial_bins)
phi_bins = np.linspace(0, 2*np.pi, n_phi_bins)
radial_mesh, phi_mesh = np.meshgrid(radial_bins, phi_bins)

nbins = n_radial_bins * n_phi_bins

fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))

with run_mcnp(no_reflector_card, params={}, cores=4) as (status, mcnp_dir):  
    fissions, nhistory = parse_ptrac_fissions(mcnp_dir + '\\ptrac')
    r = np.sqrt(fissions[:, 0]**2. + fissions[:, 1]**2.)
    phi = np.arctan2(fissions[:,1], fissions[:,0]) + np.pi
    
    hist, xedges, yedges = np.histogram2d(r, phi, bins=[radial_bins, phi_bins]) 
    hist = hist / float(nhistory) * nbins

    quadmesh = ax.pcolormesh(yedges, xedges, hist)
    print fissions.shape[0] / float(nhistory)

plt.colorbar(quadmesh,ax=ax)
plt.show()