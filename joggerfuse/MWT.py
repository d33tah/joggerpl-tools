# -*- coding: utf-8 -*-

import time

from common_logger import common_logger

## {{{ http://code.activestate.com/recipes/325905/ (r5)
class MWT(object):
    """Memoize With Timeout"""
    _caches = {}
    _timeouts = {}
    
    def __init__(self,timeout=3):
        self.timeout = timeout
        self.logger = common_logger('MWT')
        
        
    def collect(self):
        """Clear cache of results which have timed out"""
        for func in self._caches:
            cache = {}
            for key in self._caches[func]:
                if (time.time() - self._caches[func][key][1]) < self._timeouts[func]:
                    cache[key] = self._caches[func][key]
            self._caches[func] = cache
    
    def __call__(self, f):
        self.cache = self._caches[f] = {}
        self._timeouts[f] = self.timeout
        
        def func(*args, **kwargs):
            kw = kwargs.items()
            kw.sort()
            key = (args, tuple(kw))
            try:
                v = self.cache[key]
                if (time.time() - v[1]) > self.timeout:
                    raise KeyError
                else:
                    self.logger.logger.debug('hit the cache: %s' % f.func_name)
            except KeyError:
                v = self.cache[key] = f(*args,**kwargs),time.time()
            return v[0]
        func.func_name = f.func_name
        
        return func
