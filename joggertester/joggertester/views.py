# -*- coding: utf-8 -*-

from django import template
from django.template import Context
from django.http import HttpResponse

from models import Wpis

def glowna(request):
    
    surowy = open('szablony/glowna.html').read()
    
    tagi = { 
                   'JOG_TITLE': 'Dee\'s weblog',
                   'HOME': 'http://deetah.jogger.pl/',
                   'RSS': 'http://deetah.jogger.pl/rss/',
                   'JOG': 'deetah',
                   
                   'ENTRY_SUBJECT': '{{ wpis.subject }}',
                   'ENTRY_TITLE': '{{ wpis.subject|escape }}',
                   'ENTRY_ID': '{{ wpis.entry_id }}',
                   'ENTRY_CONTENT_SHORT': '{{ wpis.content_short }}',
                   'ENTRY_DATE_DAY': '{{ wpis.date_day }}',
                   'ENTRY_DATE_MONTH': '{{ wpis.date_month }}',
                   'ENTRY_DATE_YEAR': '{{ wpis.date_year }}',
                   'ENTRY_COMMENT_HREF': '/id/{{ wpis.entry_id }}',
                   'ENTRY_COMMENT_HREF_DESCR': """
                   {% if wpis.comments_blocked %}
                       Komentarze zablokowane
                   {% else %}
                       {% if wpis.komentarz_set %}
                           Są komentarze.
                       {% else %}
                           Nie ma komentarzy.
                       {% endif %} 
                   {% endif %}
                   """
                    
    }
    
    bezposrednio = { 
                    '<ENTRY_BLOCK>': '{% for wpis in wpisy %}',
                    '</ENTRY_BLOCK>': '{% endfor %}',
    
                    '<ADMIN_BLOCK>': '{% if admin_mode %}',
                    '</ADMIN_BLOCK>': '{% endif %}',
                    
                    '<ENTRY_CONTENT_SHORT_EXIST>': '{% if wpis.content_short %}',
                    '</ENTRY_CONTENT_SHORT_EXIST>': '{% endif %}'
    }
    
    for tag in tagi:
        surowy = surowy.replace('<'+tag+'/>',tagi[tag])
        surowy = surowy.replace('&'+tag+';',tagi[tag])
        
    for tag in bezposrednio:
        surowy = surowy.replace(tag,bezposrednio[tag])
    
    wpisy = []
    wpisy += [ Wpis(
                    subject='testowy', 
                    entry_id='3', 
                    content_short='Asdf',
                    date_day = '03',
                    date_month = 'lutego',
                    date_year = '2013',
                    comments_blocked = False,
                    ) 
              ]
    
    wpisy += [ Wpis(
                    subject='testowy', 
                    entry_id='3', 
                    content_short='Asdf',
                    date_day = '03',
                    date_month = 'lutego',
                    date_year = '2013',
                    comments_blocked = True
                    ) 
              ]    
        
    html = template.Template(surowy).render(Context({
             'wpisy' : wpisy,
             'admin_mode' : True
             }
        )
    )
    return HttpResponse(html)
