from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wordlinks.views.home', name='home'),
    # url(r'^wordlinks/', include('wordlinks.foo.urls')),

    url(r'^learn/', include('learn.urls', namespace='learn')),
    url(r'^words/', include('words.urls', namespace='words')),
    url(r'^puzzles/', include('puzzles.urls', namespace='puzzles')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
