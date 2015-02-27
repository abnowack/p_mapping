# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 11:09:28 2015

@author: Aaron

"""

from mcnpy.ptrac import reader as preader
from mcnpy.ptrac import plotter as pplotter
import numpy as np

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

    return False

def parse_ptrac_fissions(filename):
    incident_positions = []
    
    n_history = 0
    with open(filename, 'r') as ptrac:
        # parse headers and formats
        header = preader.ptrac_header(ptrac)
        input_format = preader.ptrac_input_format(ptrac)
        event_format = preader.ptrac_event_format(ptrac)

        for history in preader.parse_ptrac_events(ptrac, event_format):
            is_fission = incident_fission(history)
            if is_fission:
                incident_positions.append([history.events[0].xxx,
                                           history.events[0].yyy,
                                           history.events[0].zzz])
            n_history += 1
    
    return np.array(incident_positions), n_history

if __name__ == '__main__':
    from plot_utils import *
    
    fissions, nps = parse_ptrac_fissions('tmpjtjmnn/ptrac')
    r = np.sqrt(fissions[:, 0]**2. + fissions[:, 1]**2. + fissions[:, 2]**2.)
    plot_radial_bins(r, 1.0, 20, nps)