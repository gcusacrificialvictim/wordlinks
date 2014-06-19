from django.conf.urls import patterns, url

from learn import views

urlpatterns = patterns('',
        # eg: /learn/
        url(r'^$', views.index, name='index'),
        # eg: /learn/word/
        url(r'^(?P<word>[a-zA-Z]+)/$', views.learn_word, name='learn_word'),
)