# -*- coding: utf-8 -*-

from django import template
from django.template import Context
from django.http import HttpResponse
from django.db.models import Count
from django.conf import settings

from models import Wpis, GrupaLinkow, Kategoria
from slowniki_tagow import tagi, bezposrednio

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

def renderuj_szablon(nazwa_pliku):
    
    surowy = open(nazwa_pliku).read()
    
    for tag in tagi:
        surowy = surowy.replace('<' + tag + '/>', tagi[tag])
        surowy = surowy.replace('&' + tag + ';', tagi[tag])
        
    for tag in bezposrednio:
        surowy = surowy.replace(tag, bezposrednio[tag])
        
    return surowy

def glowna(request):
    
    surowy = renderuj_szablon(settings.PROJECT_DIR + '/szablony/glowna.html')
    
    html = template.Template(surowy).render(Context({
             'wpisy' : Wpis.objects.all(),
             'grupy_linkow' : GrupaLinkow.objects.all(),
             'admin_mode' : True,
             'kategorie': Kategoria.objects.all().annotate(entries=Count('wpis')),
             }
        )
    )
    return HttpResponse(html)

def komentarze(request, wpis_id):
    
    if wpis_id.endswith('/'):
        wpis_id = wpis_id[:-1]
        
    surowy = renderuj_szablon(settings.PROJECT_DIR + '/szablony/komentarze.html')
    
    html = template.Template(surowy).render(Context({
             'wpis' : Wpis.objects.get(entry_id = wpis_id),
             'grupy_linkow' : GrupaLinkow.objects.all(),
             'admin_mode' : True,
             'zalogowany': 'deetah',
             'ostatni_nickid': 'deetah',
             'ostatni_url': 'http://deetah.jogger.pl',
             'wpisana_tresc': '',
             'kategorie': Kategoria.objects.all().annotate(entries=Count('wpis')),
             }
        )
    )
    return HttpResponse(html)
