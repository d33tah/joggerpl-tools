from django import template
from django.template import Context
from django.http import HttpResponse

from models import Wpis

def glowna(request):
    
    surowy = open('szablony/glowna.html').read()
    
    tagi = { 
                   'JOG_TITLE': 'Dee\'s weblog',
                   'ENTRY_SUBJECT': '{{ wpis.tytul }}' 
    }
    
    bezposrednio = { 
                    '<ENTRY_BLOCK>': '{% for wpis in wpisy %}',
                    '</ENTRY_BLOCK>': '{% endfor %}'
    }
    
    for tag in tagi:
        surowy = surowy.replace('<'+tag+'/>',tagi[tag])
        surowy = surowy.replace('&'+tag+';',tagi[tag])
        
    for tag in bezposrednio:
        surowy = surowy.replace(tag,bezposrednio[tag])
    
    wpisy = []
    wpisy += [ Wpis(tytul='testowy') ]
    wpisy += [ Wpis(tytul='testowy2') ]
        
    html = template.Template(surowy).render(Context({'wpisy':wpisy}))
    return HttpResponse(html)
