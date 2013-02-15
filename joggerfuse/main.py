#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import os
import thread
import signal
import logging

from JoggerFS import JoggerFS
from common_logger import common_logger
main_logger = common_logger('main')

def do_testing():
    global main_logger
    main_logger.debug('do_testing')
    print(tuple(os.walk('katalog')))

def sleep_until_ctrc():
    global main_logger
    main_logger.debug('sleep_until_ctrc')
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break

def umount_fuse(signum = None, frame = None, exit_after_attempt = True):
    global main_logger
    main_logger.info('Unmounting...')
    os.system("fusermount -u katalog")
    main_logger.info('Done.')
    if exit_after_attempt:
        sys.exit(0)

if __name__ == '__main__':
    
    if len(sys.argv)<2:
        sys.argv += ['-f', 'katalog']
        testing = True
        
    fs = JoggerFS()
    fs.parse(errex=1)
    
    #logging.getLogger('JoggerFS').setLevel(logging.INFO)
    logging.getLogger('MWT').setLevel(logging.INFO)

    main_logger.info("Will try to mount the FUSE bindings.")
    thread.start_new_thread(lambda: fs.main(), tuple())
    signal.signal(signal.SIGINT, umount_fuse)
    signal.signal(signal.SIGTERM, umount_fuse)
    
    if sys.stdout.isatty():
        sleep_until_ctrc()
    elif testing:
        time.sleep(2)
        do_testing()
        
    umount_fuse(exit_after_attempt = False)
    