from django.conf.urls import patterns, url

from puzzles import views

urlpatterns = patterns('',
        # eg: /puzzles/
        url(r'^$', views.puzzle_get, name='index'),

        # eg: /puzzles/5/
        url(r'^(?P<puzzle_id>\d+)/$', views.puzzle_id, name='puzzle'),

        # eg: /puzzles/random/
        url(r'^random/$', views.puzzle_random, name='random'),

        # eg: /puzzles/_create/word/
        url(r'^_create/(?P<word>[a-zA-Z]+)/$', views.puzzle_create, name='create'),

        # eg: /puzzles/_get/
        url(r'^_get/$', views.puzzle_get, name='get'),

        # eg: /puzzles/left/right/
        url(r'^(?P<left>[a-zA-Z]+)/(?P<right>[a-zA-Z]+)/$', views.puzzle_by_words, name='puzzle_by_words'),

        # eg: /puzzles/5/answer
        url(r'^(?P<puzzle_id>\d+)/answer/$', views.answer, name='answer'),
)
