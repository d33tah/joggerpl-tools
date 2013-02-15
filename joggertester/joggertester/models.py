# -*- coding: utf-8 -*-

"""
This file is part of joggertester.

Joggertester is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Joggertester is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from django.db import models
from django.template.defaultfilters import slugify

class Kategoria(models.Model):
    href_descr = models.CharField(max_length=128)
    title =  models.CharField(max_length=1024)
    #TODO: ojciec_id
    
    def href(self):
        href_descr = self.href_descr
        return '/kategoria/' + slugify(href_descr)
    
    class Meta:
        verbose_name_plural = "kategorie"


class Wpis(models.Model):
    subject = models.CharField(max_length=1024)
    content_short = models.CharField(max_length=10240)
    content = models.CharField(max_length=1024000)
    entry_id = models.CharField(max_length=32)
    date_day = models.CharField(max_length=32)
    date_month = models.CharField(max_length=32)
    date_year = models.CharField(max_length=32)
    comments_blocked = models.BooleanField()
    kategoria_id = models.ForeignKey('Kategoria')
    class Meta:
        verbose_name_plural = "wpisy"
            
class Komentarz(models.Model):
    wpis_id = models.ForeignKey('Wpis')
    content = models.CharField(max_length=10240)
    nick = models.CharField(max_length=64)
    date = models.CharField(max_length=64)
    hour = models.CharField(max_length=32)
    comment_id = models.CharField(max_length=32)
    class Meta:
        verbose_name_plural = "komentarze"
        
class Trackback(models.Model):
    wpis_id = models.ForeignKey('Wpis')
    class Meta:
        verbose_name_plural = "trackbacki"
        
class GrupaLinkow(models.Model):
    descr = models.CharField(max_length=1024)
    class Meta:
        verbose_name_plural = "grupy linków"
            
class Link(models.Model):
    grupa_linkow_id = models.ForeignKey('GrupaLinkow')
    href = models.CharField(max_length=1024)
    href_descr = models.CharField(max_length=1024)
    class Meta:
        verbose_name_plural = "linki"
            