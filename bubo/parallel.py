import os
from time import sleep
import sys
import importlib
import subprocess
import inspect
import types
from bubo.util import Stopwatch, print_update
from IPython.parallel import Client                    
import time

def parallelize(f, using='ipython', parallel=None):
    if parallel is None or using is None:
        return f
    elif using == 'ipython':
        return VectorizeIPython(f, parallel=parallel)
    elif using == 'multiprocessing':
        return VectorizeMultiprocessing(f, parallel=parallel)
    else:
        raise IOError('Invalid vectorization mode "%s" ' % using)

class Vectorize(object):
    _func = None
    _parallel = None

class VectorizeIPython(Vectorize):
    _directview = None
    
    def __init__(self, func, parallel=None):
        self._func = func
        self._parallel = parallel
        self._directview = self.connect()
        
    def __call__(self, *args):
        if args is not None:
            syncargs = list(args)
            for (k, arg) in enumerate(args):
                if (arg is None) or (len(arg) == 1):
                    syncargs[k] = [arg]*self._parallel
                elif len(arg) == self._parallel:
                    pass
                else:
                    raise IOError('invalid parallel argument list length - got %d, expected %d' % (len(arg), self._parallel))
        else:
            syncargs = [None]*self._parallel
        result = self._directview.map_async(self._func, *syncargs)

        print '[bubo.parallel]: ---------------- begin %s ----------------' % self._func.__name__               
        self.wait(result)
        result.display_outputs()
        print '[bubo.parallel]: ---------------- end %s ------------------' % self._func.__name__       
        return result.get()

    def wait(self, result, timeout=None, interval=1):
        """interactive wait, printing progress at regular intervals - modified from ipython wait_interactive()"""
        if timeout is None:
            timeout = -1
        N = len(result)
        tic = time.time()
        while not result.ready() and (timeout < 0 or time.time() - tic <= timeout):
            result.wait(interval)
            #print_update("%i/%i bubo.parallel tasks finished after %4i s" % (result.progress, N, result.elapsed))
        #print '\n',
        
    def connect(self, timeout_in_sec=15):
        """Try to connect to cluster for timeout seconds"""
        #self.spindown()
        for k in range(timeout_in_sec):
            try:
                self._directview = Client()
                self._directview = self._directview[:]
                print '\n'  # success if we get here 
                return self._directview
            except:
                if k == 0:
                    print('[bubo.parallel]: starting ipython cluster with %d workers...' % self._parallel),
                    self._dview = self.spinup(self._parallel)
                else:
                    sys.stdout.write("."),                    
                sleep(1)
            sys.stdout.flush()
        raise IOError('could not connect to ipython engines')
            
    def spinup(self, parallel):
        subprocess.call('ipcluster-2.7 start -n %d --daemonize --quiet' % parallel, shell=True); 
        
    def spindown(self):
        #print '[bubo.parallel]: stopping ipython cluster with %d workers ...' % self._parallel
        subprocess.call('ipcluster-2.7 stop --quiet', shell=True); 

