# -*- coding: utf-8 -*-
"""
Created on Wed Feb 25 11:29:31 2015

@author: Aaron
"""

import subprocess
import tempfile
import os

class MCNPWrapper(object):
    def __init__(self, randseed=1):
        self.seed = randseed
    
    def __call__(self, card, params, cores=1, **kwargs):
        self.seed += 1
        
        params['seed'] = self.seed
        card = card.format(**params)
        
        args = ['tasks', cores]
        
        # create temp folder
        temp_dir = tempfile.mkdtemp(dir='.')
        with f as open(temp_dir + '\\input.i'):
            f.write(card)
        
        args += ['i=input.i']

        # mcnp doesn't use errorcodes or stderr, so Popen doesnt add features
        # stick with simpler check_output and parse stdout
        mcnp = subprocess.check_output(['mcnp6'] + args, shell=True,
                                       dir=temp_dir)
        
        # check for errors in stdout
        if 'bad trouble' in mcnp or 'fatal error' in mcnp:
            print 'Error in MCNP outout'
            print mcnp
            return False, temp_dir
        
        return True, temp_dir
        