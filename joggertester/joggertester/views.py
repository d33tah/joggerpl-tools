# -*- coding: utf-8 -*-

from django import template
from django.template import Context
from django.http import HttpResponse

from models import Wpis, GrupaLinkow

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
                   'ENTRY_COMMENT_HREF_DESCR': 
                       """
                           {% if wpis.comments_blocked %}
                               Komentarze zablokowane
                           {% else %}
                               {% if wpis.komentarz_set.all %}
                                   Są komentarze. 
                                   ({{ wpis.komentarz_set.all|length }})
                               {% else %}
                                   Nie ma komentarzy.
                               {% endif %} 
                           {% endif %}
                       """,
                       
                   'LINK_HREF': '{{ link.href }}',
                   'LINK_HREF_DESCR': '{{ link.href_descr }}',
                   'LINK_GROUP_DESCR': '{{ grupa.descr }},' 
    }
    
    bezposrednio = { 
                    '<ENTRY_BLOCK>': '{% for wpis in wpisy %}',
                    '</ENTRY_BLOCK>': '{% endfor %}',
    
                    '<ADMIN_BLOCK>': '{% if admin_mode %}',
                    '</ADMIN_BLOCK>': '{% endif %}',
                    
                    '<ENTRY_CONTENT_SHORT_EXIST>': '{% if wpis.content_short %}',
                    '</ENTRY_CONTENT_SHORT_EXIST>': '{% endif %}',
                    
                    '<LINK_BLOCK>': '{% for link in grupa.link_set.all %}',
                    '</LINK_BLOCK>': '{% endfor %}',
                    
                    '<LINK_GROUP_BLOCK>': '{% for grupa in grupy_linkow %}',
                    '</LINK_GROUP_BLOCK>': '{% endfor %}',
    }
    
    for tag in tagi:
        surowy = surowy.replace('<' + tag + '/>', tagi[tag])
        surowy = surowy.replace('&' + tag + ';', tagi[tag])
        
    for tag in bezposrednio:
        surowy = surowy.replace(tag, bezposrednio[tag])
    
    html = template.Template(surowy).render(Context({
             'wpisy' : Wpis.objects.all(),
             'grupy_linkow' : GrupaLinkow.objects.all(),
             'admin_mode' : True
             }
        )
    )
    return HttpResponse(html)
