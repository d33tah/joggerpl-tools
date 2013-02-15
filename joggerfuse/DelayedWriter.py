# -*- coding: utf-8 -*-

import threading
import time

from common_logger import common_logger

class DelayedWriter:
    
    def __init__(self):
        self.paths = {}
        self.logger = common_logger('DelayedWriter')
        
    def register(self, path, fun_read, fun_write):
        self.logger.debug('register(path="%s")' % path)
        self.paths[path] = {}
        self.paths[path]['fun_read'] = fun_read
        self.paths[path]['fun_write'] = fun_write
        
    def write(self, path, offset, _buffer):
        
        self.logger.debug('write(path="%s")' % path)
        
        if not 'buffer' in self.paths[path]:
            self.paths[path]['buffer'] = self.paths[path]['fun_read']()
            
        tmp = list(self.paths[path]['buffer'])
        tmp[offset:offset+len(_buffer)] = list(_buffer)
        self.paths[path]['buffer'] = ''.join(tmp)
        
        self.paths[path]['last_update'] = time.time()
        threading.Timer(1.0, lambda: self.schedule(path)).start()
        
    def schedule(self, path):
        
        self.logger.debug('schedule(path="%s")' % path)
         
        if time.time() - self.paths[path]['last_update'] > 1.0:
            self.logger.info('schedule(path="%s"): saving' % path)
            self.paths[path]['fun_write'](self.paths[path]['buffer'])
            del self.paths[path]['buffer']
