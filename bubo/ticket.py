import os
import sys
import importlib
import types
from bubo.util import Stopwatch

class FunctionTicket(object):
    _modulename = None
    _funcname = None    
    runtime = None
    synctime = None
    
    def __init__(self, func):
        if type(func) is types.FunctionType and func.__module__ == '__main__':
            raise ValueError('function is not importable on clients - modulename must be not be __main__')            
        elif type(func) is types.FunctionType:
            self._modulename = func.__module__
            self._funcname = func.__name__        
        else:
            raise ValueError('not a function - object is type ' + str(func))
        
    def __repr__(self):
        return str('<bubo.function \'' + str(self._modulename) + '.' + str(self._funcname) + '\'>')
    
    def __call__(self, *args, **kwargs):
        module = importlib.import_module(self._modulename)
        with Stopwatch() as stopwatch:        
            (syncargs, synckwargs) = self.synchronize(args, kwargs)
        synctime = stopwatch.elapsed            
        with Stopwatch() as stopwatch:
            result = getattr(module, self._funcname)(*syncargs, **synckwargs)
        _runtime = stopwatch.elapsed

    def synchronize(self, args, kwargs):
        syncargs = list(args)
        synckwargs = kwargs
        return (syncargs, synckwargs)
    
