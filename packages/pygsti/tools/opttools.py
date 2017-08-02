from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************

'''
This module defines tools for optimization and profiling
'''
from functools   import partial, wraps
from time        import time
from contextlib  import contextmanager
from collections import defaultdict
from datetime    import datetime

# note that this decorator ignores **kwargs
def cache_by_hashed_args(obj):
    cache = obj.cache = {}

    @wraps(obj)
    def memoizer(*args, **kwargs):
        if len(kwargs) > 0:
            raise ValueError('Cannot currently memoize on kwargs')
        try:
            if args not in cache:
                cache[args] = obj(*args, **kwargs)
            return cache[args]
        except TypeError:
            print('Warning: arguments for cached function could not be cached')
            return obj(*args, **kwargs)
    return memoizer


@contextmanager
def timed_block(label, timeDict=None, printer=None, verbosity=2, roundPlaces=6, preMessage=None, formatStr=None):
    def put(message):
        if printer is None:
            print(message)
        else:
            printer.log(message, verbosity)

    if preMessage is not None:
        put(preMessage.format(label))
    start = time()
    try:
        yield
    finally:
        end = time()
        t = end - start
        if timeDict is not None:
            if isinstance(timeDict, defaultdict):
                timeDict[label].append(t)
            else:
                timeDict[label] = t
        else:
            if formatStr is not None:
                label = formatStr.format(label)
            put('{} took {} seconds\n'.format(label, str(round(t, roundPlaces))))

def self_profiling_cache(f, call_key=str, *args, **kwargs):
    if len(kwargs) > 0:
        raise ValueError('Cannot currently memoize on kwargs')
    times = dict()
    with timed_block('hash', times):
        key = call_key(args)
    with timed_block('call', times):
        cache[key] = f(*args, **kwargs)
    print(times['call'] - times['hash'])
    return cache[key]

def time_hash():
    return str(datetime.now())
