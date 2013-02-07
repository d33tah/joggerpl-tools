# -*- coding: utf-8 -*-

from django import template
from django.template import Context
from django.http import HttpResponse

from models import Wpis, GrupaLinkow

def renderuj_szablon(nazwa_pliku):
    
    surowy = open(nazwa_pliku).read()
    
    tagi = { 
                   'JOG_TITLE': 'Dee\'s weblog',
                   'HOME': '/',
                   'RSS': '/rss/',
                   'JOG': 'deetah',
                   
                   'ENTRY_SUBJECT': '{{ wpis.subject }}',
                   'ENTRY_TITLE': '{{ wpis.subject|escape }}',
                   'ENTRY_ID': '{{ wpis.entry_id }}',
                   'ENTRY_CONTENT_SHORT': '{{ wpis.content_short }}',
                   'ENTRY_DATE_DAY': '{{ wpis.date_day }}',
                   'ENTRY_DATE_MONTH': '{{ wpis.date_month }}',
                   'ENTRY_DATE_YEAR': '{{ wpis.date_year }}',
                   'ENTRY_COMMENT_HREF': '/id/{{ wpis.entry_id }}/',
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
                   'LINK_GROUP_DESCR': '{{ grupa.descr }}',
                   
                   'COMMENT_CLASS': "{% if forloop.counter|divisibleby:2 %}{{tryb}}2{% else %}{{tryb}}1{% endif %}",
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
                    
                    '<COMMENT_BLOCK>': 
                       """
                       {% with tryb="comment" %}
                       {% for komentarz in wpis.komentarz_set.all %}
                       """,
                    '</COMMENT_BLOCK>': '{% endfor %}{% endwith %}', 
                    
                    '<TRACKBACK_BLOCK>': 
                       """
                       {% with tryb="trackback" %}
                       {% for komentarz in wpis.trackback_set.all %}
                       """,
                    '</TRACKBACK_BLOCK>': '{% endfor %}{% endwith %}', 
    }
    
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
