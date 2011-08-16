from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^180/(?P<slug>[\w\-]+)/$', 'one80.committees.views.hearing_detail', name='hearing_detail'),
    url(r'^180/(?P<slug>[\w\-]+)/(?P<photo_id>\d+)/$', 'one80.photos.views.photo_detail', name='photo_detail'),
    url(r'^$', 'one80.views.index', name='index'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
            }),
       )