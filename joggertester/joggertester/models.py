# -*- coding: utf-8 -*-

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
            