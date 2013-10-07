import os
from time import sleep
import sys
import importlib
import bubo.ticket
import subprocess
import inspect

# Parallelism type
using = 'serial'

# SMP using ipython
if using == 'ipython':
    #print '[bubo.parallel]: starting ipython cluster...'
    #subprocess.call('ipcluster-2.7 start -n 4 --daemonize --quiet', shell=True); sleep(7)
    from IPython.parallel import Client    
    rc = Client()
    dview = rc[:]
elif using == 'serial':
    dview = None
    pass
else:
    raise


class Vectorize(object):
    def __init__(self, f, view):
        self.view = view
        self.f = f
        self.f_tkt = bubo.ticket.FunctionTicket(f)
        
    def __call__(self, *args, **kwargs):
        if dview is None:
            return map(self.f, args[0]) 
        else:
            return self.view.apply(self.f_tkt, *args, **kwargs)


def vectorize(f):
    return Vectorize(f, dview)

