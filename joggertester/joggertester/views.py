# -*- coding: utf-8 -*-

from django import template
from django.template import Context
from django.http import HttpResponse

from models import Wpis, GrupaLinkow
from slowniki_tagow import tagi, bezposrednio

def renderuj_szablon(nazwa_pliku):
    
    surowy = open(nazwa_pliku).read()
    
    for tag in tagi:
        surowy = surowy.replace('<' + tag + '/>', tagi[tag])
        surowy = surowy.replace('&' + tag + ';', tagi[tag])
        
    for tag in bezposrednio:
        surowy = surowy.replace(tag, bezposrednio[tag])
        
    return surowy

def glowna(request):
    
    surowy = renderuj_szablon('szablony/glowna.html')
    
    html = template.Template(surowy).render(Context({
             'wpisy' : Wpis.objects.all(),
             'grupy_linkow' : GrupaLinkow.objects.all(),
             'admin_mode' : True
             }
        )
    )
    return HttpResponse(html)

def komentarze(request, wpis_id):
    
    if wpis_id.endswith('/'):
        wpis_id = wpis_id[:-1]
        
    surowy = renderuj_szablon('szablony/komentarze.html')
    
    html = template.Template(surowy).render(Context({
             'wpis' : Wpis.objects.get(entry_id = wpis_id),
             'grupy_linkow' : GrupaLinkow.objects.all(),
             'admin_mode' : True
             }
        )
    )
    return HttpResponse(html)
