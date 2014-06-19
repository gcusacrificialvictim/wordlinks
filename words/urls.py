from django.conf.urls import patterns, url

from words import views

urlpatterns = patterns('',
        # eg: /words/
        url(r'^$', views.index, name='index'),

        # eg: /words/5/
        # url(r'(?P<word_id>\d+)/$', views.detail_id, name='detail'),

        # eg: /words/example/
        url(r'(?P<word_string>[a-z]+)/$', views.detail_string, name='detail'),
)