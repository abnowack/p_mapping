Cylinder Assembly with No Relector
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