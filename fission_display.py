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

Ex: 2 - Collision
    
"""

from ptrac_reader import ptrac_reader as preader
from ptrac_reader import ptrac_plotter as pplotter

def incident_fission(history):
    ''' Indicate whether source neutron underwent fission
        Elastic and Inelastic scattering is allowed
        Terminates if encounters
            type == 5000
            ntyn != 18-21
                allowed if
                ntyn = [1, 2, -99, 50-91]
            type / 1000 == 2 (not original neutron)
    '''
    for ev in history.events:
        # source
        if ev.type == 1000:
            continue
        # remove termination (no fission) and bank events (extra neutrons made)
        if ev.type == 5000 or ev.type / 1000 == 2:
            return False
        if hasattr(ev, 'ntyn'):
            # fission
            if ev.ntyn >= 18 and ev.ntyn <= 21:
                return True
            # allowed scatters before fission
            if ev.ntyn in [1, 2, -99] or (ev.ntyn >= 50 and ev.ntyn <= 91):
                continue
#        else:
            # unhandled cases, surface events
#            print 'unhandled'

    print 'exited loop'
    print ev
    return False

if __name__ == '__main__':
    with open('ptrac', 'r') as ptrac:
        # parse headers and formats
        header = preader.ptrac_header(ptrac)
        input_format = preader.ptrac_input_format(ptrac)
        event_format = preader.ptrac_event_format(ptrac)

        for history in preader.parse_ptrac_events(ptrac, event_format):
            print incident_fission(history)

#        for i in xrange(23):
#            history = preader.parse_ptrac_events(ptrac, event_format)
##        print history
#        print incident_fission(history)
##        print history
#        pplotter.plot_events(history.events)