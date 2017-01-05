from django.conf.urls import patterns, include, url

urlpatterns = patterns('gameservice.views',
    url(r'^$', 'game_ui', name='game_ui'),
)
