from django.contrib import admin
from models import Kategoria, Wpis, Komentarz, Trackback, Link, GrupaLinkow

class KategoriaAdmin(admin.ModelAdmin):
    pass

class WpisAdmin(admin.ModelAdmin):
    pass

class KomentarzAdmin(admin.ModelAdmin):
    pass

class TrackbackAdmin(admin.ModelAdmin):
    pass

class LinkAdmin(admin.ModelAdmin):
    pass

class GrupaLinkowAdmin(admin.ModelAdmin):
    pass


admin.site.register(Kategoria, KategoriaAdmin)
admin.site.register(Wpis, WpisAdmin)
admin.site.register(Komentarz, KomentarzAdmin)
admin.site.register(Trackback, TrackbackAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(GrupaLinkow, GrupaLinkowAdmin)
