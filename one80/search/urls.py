from django.conf.urls.defaults import patterns, url
from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

sqs = SearchQuerySet().facet('result_type')

urlpatterns = patterns('one80.search.views',
    url(r'^$', 'search', {'searchqueryset': sqs}, name='search'),
    url(r'^(?P<result_type>[\w]+)/$', 'narrowed_search', {'searchqueryset': sqs}, name='narrowed_search'),
)