# -*- coding: utf-8 -*-

import logging

from MWT import MWT
import mechanize
from lxml import html
from common_logger import common_logger


"""
This file is part of joggerfuse.

Joggerfuse is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Joggerfuse is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""


class JoggerScraper(mechanize.Browser):
    
    def __init__(self):
        mechanize.Browser.__init__(self)
        self.logger = common_logger('JoggerScraper')
        
    def set_login(self, jogger_login, jogger_haslo):
        self.login, self.haslo = jogger_login, jogger_haslo
        
    def __do_get(self, url):
        drzewo = html.fromstring(self.open(url).read())
        if drzewo.xpath('//form//input [@name="login_jabberid"]'):
            self.__zaloguj()
            drzewo = html.fromstring(self.open(url).read())
        return drzewo
        
    def __zaloguj(self):
        self.logger.debug('zaloguj')
        self.select_form(nr=0)
        self.form['login_jabberid'] = self.login
        self.form['login_jabberpass'] = self.haslo
        self.submit()
    
    @MWT()
    def pobierz_files(self):
        self.logger.debug('pobierz_files')
        ret = {}
        drzewo = self.__do_get('https://login.jogger.pl/templates/files/')
        for plik in drzewo.xpath('//td/a'):
            nazwa_pliku = plik.text_content()
            # wielkosc jest dwa td'ki na prawo od nazwy pliku
            wielkosc = int(plik.getparent().getnext().getnext().text_content())
            ret[nazwa_pliku] = {}
            ret[nazwa_pliku]['rozmiar'] = wielkosc
            ret[nazwa_pliku]['url'] = plik.get('href')
        return ret
    
    def __zwroc_textarea(self, url):
        drzewo = self.__do_get(url)
        textarea = drzewo.xpath('//textarea')
        assert(len(textarea) == 1)
        return textarea[0].text_content()
        
    @MWT()
    def pobierz_szablon_glowna(self):
        self.logger.debug('pobierz_szablon_glowna')
        return self.__zwroc_textarea('https://login.jogger.pl/templates/edit/')
    
    @MWT()
    def pobierz_szablon_komentarze(self):
        self.logger.debug('pobierz_szablon_komentarze')
        return self.__zwroc_textarea('https://login.jogger.pl/templates/edit/' + \
                                     '?file=comments')
        
    @MWT()
    def pobierz_szablon_strony(self):
        self.logger.debug('pobierz_szablon_strony')
        raise NotImplementedError()  # są czary-mary z URLem
                                    # który trzeba najpierw odwiedzić
                                    
    @MWT()
    def pobierz_szablon_logowanie(self):
        self.logger.debug('pobierz_szablon_logowanie')
        return self.__zwroc_textarea('https://login.jogger.pl/templates/edit/' + \
                                     '?file=login')
        
    def zmien_szablon_glowna(self, _buffer):
        self.logger.debug('zmien_szablon_glowna: %s' % _buffer)
        self.__do_get('https://login.jogger.pl/templates/edit/')
        self.select_form(nr=0)
        self.form['templatesContent'] = _buffer
        self.submit()
    
    def zmien_szablon_komentarze(self, _buffer):
        self.logger.debug('zmien_szablon_komentarze: %s' % _buffer)
        self.__do_get('https://login.jogger.pl/templates/edit/?file=comments')
        self.select_form(nr=0)
        self.form['templatesContent'] = _buffer
        self.submit()
    
    def zmien_szablon_strony(self, _buffer):
        self.logger.debug('zmien_szablon_strony: %s' % _buffer)
        raise NotImplementedError()
    
    def zmien_szablon_logowanie(self, _buffer):
        self.logger.debug('zmien_szablon_logowanie: %s' % _buffer)
        self.__do_get('https://login.jogger.pl/templates/edit/?file=login')
        self.select_form(nr=0)
        self.form['templatesContent'] = _buffer
        self.submit()
