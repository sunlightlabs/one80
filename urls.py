from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'one80.auth.views.login_begin', name='login'),
    url(r'^login/complete/$', 'one80.auth.views.login_complete', name='login_complete'),
    url(r'^logout/$', 'one80.auth.views.logout_begin', name='logout'),
    url(r'^logout/complete/$', 'django.contrib.auth.views.logout', {'next_page': '/180/', 'redirect_field_name': 'next'}, name='logout_complete'),
    url(r'^profile/$', 'one80.auth.views.profile', name='profile'),
    url(r'^', include('social_auth.urls')),

    url(r'^committee/(?P<slug>[\w-]+)/$', 'one80.committees.views.committee_detail', name='committee_detail'),

    url(r'^(?P<slug>[\w-]+)/$', 'one80.committees.views.hearing_detail', name='hearing_detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<photo_id>\d+)/$', 'one80.photos.views.photo_detail', name='photo_detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<photo_id>\d+)/annotations.json$', 'one80.photos.views.photo_annotations', name='photo_annotations'),
    url(r'^annotation/(?P<annot_id>\d+)/approve/$', 'one80.photos.views.approve_annotation', name='annotation_approve'),
    url(r'^annotation/(?P<annot_id>\d+)/delete/$', 'one80.photos.views.delete_annotation', name='annotation_delete'),

    # google site verification
    url(r'^google28b165dcee3ec76d.html$', direct_to_template, {'template': 'google_site_verification.html'}),

    # homepage
    url(r'^$', 'one80.views.index', name='index'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
            }),
    )