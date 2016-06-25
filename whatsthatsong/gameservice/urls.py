from django.conf.urls import patterns, include, url

UUID_REGEX_PATTERN = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

PROSPECT_UUID_URL_PARAMETER = r'(?P<prospect_uuid>' + UUID_REGEX_PATTERN + r')'

urlpatterns = patterns('gameservice.views',
    url(r'^$', 'game_ui', name='game_ui'),
)
