First Attempt at P Mapping Input Deck
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
NPS 100
PTRAC FILE=ASC WRITE=ALL
SDEF 
C SDEF ERG=2.0 RAD=D1 CEL=10
C SI1 0 1.0
