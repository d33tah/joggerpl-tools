# -*- coding: utf-8 -*-

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
    'ENTRY_CONTENT': '{{ wpis.content }}',
    
    'LINK_HREF': '{{ link.href }}',
    'LINK_HREF_DESCR': '{{ link.href_descr }}',
    'LINK_GROUP_DESCR': '{{ grupa.descr }}',
    
    'COMMENT_CLASS': "{% if forloop.counter|divisibleby:2 %}{{tryb}}2{% else %}{{tryb}}1{% endif %}",
    'COMMENT_CONTENT': '{% autoescape off %}{{ komentarz.content }}{% endautoescape %}',
    'COMMENT_NICK': '{{ komentarz.nick }}',
    'COMMENT_DATE': '{{ komentarz.date }}',
    'COMMENT_HOUR': '{{ komentarz.hour }}',
    'COMMENT_ID': '{{ komentarz.id }}',
    'COMMENT_NUMBER': '{{ forloop.counter }}',
    
    'COMMENT_FORM_ACTION': '/id/{{ wpis.entry_id }}/',
    'COMMENT_FORM_NICKID': '{{ ostatni_nick }}', #TODO: pamiętać poprzedni stan
    'COMMENT_FORM_NICKURL': '{{ ostatni_url }}',  #TODO: pamiętać poprzedni stan
    'COMMENT_FORM_BODY': '{{ wpisana_tresc }}',
        
    'LOGGED_USER_NAME': '{{ zalogowany }}',
    
    'HEADER': 
"""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="pl">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="robots" content="noindex, nofollow">
<title>Jogger :: [Twój JID]</title>
<link rel="StyleSheet" href="/files/style.css" type="text/css">
</head>
<body>""",

    'FOOTER':
"""</body>
</html>""",

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
    
    '<COMMENT_ALLOWED_BLOCK>': '{% if not wpis.comments_blocked %}',
    '</COMMENT_ALLOWED_BLOCK>': '{% endif %}',
    
    '<COMMENT_NONE_BLOCK>': '{% if wpis.comments_blocked %}',
    '</COMMENT_NONE_BLOCK>': '{% endif %}',
    
    '<COMMENT_BLOCK_NOT_EXIST>': '{% if not wpis.komentarz_set.all %}',
    '</COMMENT_BLOCK_NOT_EXIST>': '{% endif %}',
    
    '<COMMENT_BLOCK_EXIST>': '{% if wpis.komentarz_set.all %}',
    '</COMMENT_BLOCK_EXIST>': '{% endif %}',
    
    '<TRACKBACK_BLOCK>': 
    """
    {% with tryb="trackback" %}
    {% for komentarz in wpis.trackback_set.all %}
    """,
    '</TRACKBACK_BLOCK>': '{% endfor %}{% endwith %}', 
    
    '<TRACKBACK_BLOCK_EXIST>': '{% if wpis.trackback_set.all %}',
    '</TRACKBACK_BLOCK_EXIST>': '{% endif %}',
    
    '<TRACKBACK_BLOCK_NOT_EXIST>': '{% if not wpis.trackback_set.all %}',
    '</TRACKBACK_BLOCK_NOT_EXIST>': '{% endif %}',

    '<COMMENT_FORM_NOUSER_BLOCK>': '{% if not zalogowany %}',
    '</COMMENT_FORM_NOUSER_BLOCK>': '{% endif %}',
    
    '<COMMENT_LOGGED_BLOCK>': '{% if zalogowany %}',
    '</COMMENT_LOGGED_BLOCK>': '{% endif %}',    

    '<NOUSER_BLOCK>': '{% if not zalogowany %}',
    '</NOUSER_BLOCK>': '{% endif %}',
    
    '<LOGGED_USER_BLOCK>': '{% if zalogowany %}',
    '</LOGGED_USER_BLOCK>': '{% endif %}',    
        
#TODO: HACKI. NIE MAM ZIELONEGO POJĘCIA CO TE TAGI WŁAŚCIWIE MIAŁYBY ROBIĆ.
    
    '<COMMENT_FORM_BLOCK>': '',
    '</COMMENT_FORM_BLOCK>': '',    
    
    '<COMMENT_FORM_NOTIFY_START_BLOCK>': '',
    '</COMMENT_FORM_NOTIFY_START_BLOCK>': '',    
    
    '<COMMENT_FORM_NOTIFY_STOP_BLOCK>': '',
    '</COMMENT_FORM_NOTIFY_STOP_BLOCK>': '',    

}

