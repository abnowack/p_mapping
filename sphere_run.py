# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 13:24:03 2015

@author: Aaron
"""

from mcnp_wrapper import *

input_card = \
"""First Attempt at P Mapping Input Deck
C CELL CARDS
10 100 -18.74 -1
20 0          -1

C SURFACE CARDS
1 SO 1.0

M100 92235 1
MODE N
IMP:N 1 0
PHYS:N 100 0 0 J J J 0 -1 J J J 0 0
FMULT 92235 METHOD=5
NPS 100000
PTRAC FILE=ASC WRITE=ALL MAX=500000
C UNFIROMLY SAMPLING IN SPHERE
SDEF ERG=2.0 POS=0 0 0 RAD=D1 CEL=10
SI1 0 1.0
SP1 -21 2

"""

with run_mcnp(input_card) as (status, mcnp_dir):
    with open(mcnp_dir + '\\ptrac', 'r') as ptrac:
        print ptrac.readline()
        print ptrac.readline()
        print ptrac.readline()
