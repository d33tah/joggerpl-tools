from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from joggertester import views

urlpatterns = patterns('',
    url(r'^$', views.glowna, name='main'),
    url(r'^id/(.*)$', views.komentarze, name='komentarze'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
