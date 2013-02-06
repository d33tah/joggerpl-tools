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
                   
                   'ENTRY_SUBJECT': '{{ wpis.subject }}',
                   'ENTRY_TITLE': '{{ wpis.subject|escape }}',
                   'ENTRY_ID': '{{ wpis.entry_id }}'
                    
    }
    
    bezposrednio = { 
                    '<ENTRY_BLOCK>': '{% for wpis in wpisy %}',
                    '</ENTRY_BLOCK>': '{% endfor %}',
    
                    '<ADMIN_BLOCK>': '{% if admin_mode %}',
                    '</ADMIN_BLOCK>': '{% endif %}'
    }
    
    for tag in tagi:
        surowy = surowy.replace('<'+tag+'/>',tagi[tag])
        surowy = surowy.replace('&'+tag+';',tagi[tag])
        
    for tag in bezposrednio:
        surowy = surowy.replace(tag,bezposrednio[tag])
    
    wpisy = []
    wpisy += [ Wpis(subject='testowy', entry_id='3') ]
    wpisy += [ Wpis(subject='testowy', entry_id='4') ]
        
    html = template.Template(surowy).render(Context({
             'wpisy' : wpisy,
             'admin_mode' : False
             }
        )
    )
    return HttpResponse(html)
