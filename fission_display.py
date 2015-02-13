# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 11:09:28 2015

@author: Aaron

Still need to exclude (n,Xn) occuring before (n,f)
Probably best to see if (n,Xn) present and make sure (n,f) occurred first

[ ] Track reactions of first branch, does first branch = incident and scattered
    neutron?
[ ] Test if first branch undergoes fission, otherwise skip
[ ] Loop over entire file without specifying length
[ ] Return initial positions of neutrons which undergo fission, contribute to p
[ ] Create 3D Plot (x,y,z), 2D Plot (x,y), 1D Plot (r)
[ ] Extend for multithreading, job management for accurate statistics
"""

from ptrac_reader import ptrac_reader as preader
from ptrac_reader import ptrac_plotter as pplotter

def is_fission(history):
    rxn = [ev.ntyn for ev in history.events if hasattr(ev, 'ntyn')]
    return any([n >= 18 and n <= 21 for n in rxn])

def is_nXn(history):
    rxn = [ev.ntyn for ev in history.events if hasattr(ev, 'ntyn')]
    return any([(n >= 11 and n <= 17) or (n >= 22 and n <= 91) for n in rxn])

if __name__ == '__main__':
    with open('ptrac', 'r') as ptrac:
        # parse headers and formats
        header = preader.ptrac_header(ptrac)
        input_format = preader.ptrac_input_format(ptrac)
        event_format = preader.ptrac_event_format(ptrac)

        # extend to all events in file
        for i in xrange(99):
            history = preader.parse_ptrac_events(ptrac, event_format)
            print i, is_fission(history), is_nXn(history)
        
        # parse a single event
#        while history = preader.parse_ptrac_events(ptrac, event_format):
#        for i in range(105):
#            history = preader.parse_ptrac_events(ptrac, event_format)
#            print i, nbranches(history)
#        
#        for i in xrange(7):
#            history = preader.parse_ptrac_events(ptrac, event_format)
#        print history
#        print nbranches(history)
#        pplotter.plot_events(history.events, False, False)