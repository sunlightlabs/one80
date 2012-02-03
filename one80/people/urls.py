from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('one80.people.views',
    url(r'^leaderboard/$', 'leaderboard', name='leaderboard'),
    url(r'^suggest.json$', 'search_json', name='people_search'),
    url(r'^(?P<slug>[\w\d-]+)/$', 'person_detail', name='person_detail'),
)