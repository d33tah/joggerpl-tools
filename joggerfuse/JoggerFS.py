# -*- coding: utf-8 -*-

import errno
import stat
import time
import os
import urllib
import logging

import fuse
fuse.fuse_python_api = (0, 2)

from config import jogger_login, jogger_haslo #potrzebny tylko dla tych 2 danych
from JoggerScraper import JoggerScraper
from common_logger import common_logger
from MWT import MWT

@MWT()
def get_url(url):
    return urllib.urlopen(url).read()

class JoggerFS(fuse.Fuse):
    
    def __init__(self, *args, **kw):
        
        fuse.Fuse.__init__(self, *args, **kw)
        self.jogger_scraper = JoggerScraper(jogger_login, jogger_haslo)
        self.logger = common_logger("JoggerFS")
        

    def getattr(self, path):
        
        self.logger.debug("getattr('%s')" % path)
        
        st = fuse.Stat()
        
        st.st_nlink = 2
        
        st.st_atime = int(time.time())
        st.st_mtime = st.st_atime
        st.st_ctime = st.st_atime
        
        st.st_uid = os.getuid()
        st.st_gid = os.getgid()       
        
        st.st_mode = 0555
        if path in ['/', '/szablon', '/files']:
            st.st_mode |= stat.S_IFDIR
            return st
        else:
            st.st_mode |= stat.S_IFREG
        
        if path.startswith('/files'):
            
            szukany = path[len('/files/'):]
            files = self.jogger_scraper.pobierz_files()
            if not szukany in files:
                return -errno.ENOENT
            st.st_size = files[szukany]['rozmiar']
            
        elif path.startswith('/szablon'):
            
            szukany = path[len('/szablon/'):]
            
            if szukany=='glowna.html':
                bufor = self.jogger_scraper.pobierz_szablon_glowna()
            elif szukany=='komentarze.html':
                bufor = self.jogger_scraper.pobierz_szablon_komentarze()
            elif szukany=='strony.html':
                bufor = self.jogger_scraper.pobierz_szablon_komentarze()
            elif szukany=='logowanie.html':
                bufor = self.jogger_scraper.pobierz_szablon_logowanie()
            else:
                return -errno.ENOENT
            
            st.st_size = len(bufor)    
        else:
            return -errno.ENOENT
            
        return st
    
    def read(self, path, size, offset):
        
        self.logger.debug("read(path='%s', size=%s offset=%s)" % (path, 
            size, offset))
        
        if path.startswith('/files'):
            
            szukany = path[len('/files/'):]
            files = self.jogger_scraper.pobierz_files()
            if not szukany in files:
                return -errno.ENOENT
            return get_url(files[szukany]['url'])[offset:offset+size]
        
        elif path.startswith('/szablon'):
            
            szukany = path[len('/szablon/'):]
            
            if szukany=='glowna.html':
                ret = self.jogger_scraper.pobierz_szablon_glowna()
            elif szukany=='komentarze.html':
                ret = self.jogger_scraper.pobierz_szablon_komentarze()
            elif szukany=='strony.html':
                ret = self.jogger_scraper.pobierz_szablon_komentarze()
            elif szukany=='logowanie.html':
                ret = self.jogger_scraper.pobierz_szablon_logowanie()
            else:
                return -errno.ENOENT
            return ret.encode('utf-8')[offset:offset+size]
        
        return -errno.ENOENT
    
    def readdir(self, path, offset):
        
        self.logger.debug("readdir(path='%s', offset=%s)" % (path, offset))
        root = [fuse.Direntry(x) for x in ('files', 'szablon')]
        szablon = [fuse.Direntry(x) for x in (
                                              'glowna.html', 
                                              'komentarze.html', 
                                              #'strony.html', 
                                              'logowanie.html')]
        if path=='/':
            return root
        elif path=='/szablon':
            return szablon
        elif path=='/files':
            files = self.jogger_scraper.pobierz_files()
            return [fuse.Direntry(x) for x in files.keys()]
        else:
            return -errno.ENOENT