from django.conf.urls import patterns, include, url

urlpatterns = patterns('gamecontroller.views',
    url(r'^$', 'game_controller', name='game_controller'),
)
