# Django settings for one80 project.
import json
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

# DEFAULT_FILE_STORAGE = 'one80.s3utils.MediaRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = "assets.sunlightfoundation.com"
S3_URL = "http://assets.sunlightfoundation.com/one80/"
COMPRESS_URL = S3_URL + 'static/'
COMPRESS_STORAGE = 'one80.s3utils.StaticRootS3BotoStorage'
STATICFILES_STORAGE = COMPRESS_STORAGE
STATIC_ROOT = '.static_cache'
STATIC_URL = COMPRESS_URL
ADMIN_MEDIA_PREFIX = '/static/admin/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# MEDIASYNC = {
#     'BACKEND': 'mediasync.backends.s3',
#     'AWS_BUCKET': "assets.sunlightfoundation.com",
#     'AWS_PREFIX': "one80/static",
#     'DOCTYPE': 'html5',
#     'CACHE_BUSTER': datetime.datetime.now().strftime('%s'), #only ok with 1 web head!!
#     'SERVE_REMOTE': True,
#     'PROCESSORS': (
#         'mediasync.processors.slim.css_minifier',
#         'mediasync.processors.slim.js_minifier',
#     ),
#     'JOINED': {
#         'css/joined.css': [
#             'css/style.css',
#             'css/annotation.css',
#         ],
#         'js/joined.js': [
#             'js/vendor/jquery.min.js',
#             'js/vendor/jquery-ui.min.js',
#             'js/vendor/jquery.ba-throttle-debounce.js',
#             'js/vendor/jquery.annotate.custom.js',
#             'js/vendor/jquery.jsonSuggest-2.js',
#             'js/vendor/jquery.carouFredSel-5.5.0.js',
#             'js/vendor/jquery.scrollExtend.js',
#             'js/vendor/jquery.placeholder.js',
#             'js/vendor/moment.js',
#             'js/vendor/jquery.mouseover-gallery.js',
#             'js/app.js',
#         ],
#     },
# }

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'one80.middleware.CompletedProfileMiddleware',
)

ROOT_URLCONF = 'one80.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'social_auth.context_processors.social_auth_by_type_backends',
    'one80.context_processors.authentication_services',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'django_extensions',
    'debug_toolbar',
    'compressor',
    'storages',
    'social_auth',
    'south',
    'whoosh',
    'haystack',
    'postmark',
    'gunicorn',
    'genericadmin',
    'one80',
    'one80.auth',
    'one80.committees',
    'one80.events',
    'one80.people',
    'one80.photos',
    'one80.search',
)

INTERNAL_IPS = ('127.0.0.1',)

AUTH_PROFILE_MODULE = 'auth.UserProfile'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/login/complete/'
LOGOUT_URL = '/logout/'
FACEBOOK_EXTENDED_PERMISSIONS = ['email', ]
COMPLETE_PROFILE_MESSAGE = 'You\'re almost done, we just need an email address or phone number to complete your profile.'
ADMIN_COMPLETE_PROFILE_MESSAGE = 'Your profile is not complete. Go here to add an email address or phone number.'

PAGINATE = 15

# search
DEFAULT_SEARCH_MODELS = (
    'public events',
    'hearings',
    )
FACET_FIELDS = ('annotations', 'hearings', 'public events', 'committees', 'people')
HAYSTACK_SITECONF = 'one80.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = '%s/data/whoosh/one80_index' % PROJECT_ROOT
HAYSTACK_SEARCH_RESULTS_PER_PAGE = PAGINATE

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}


# Finally, import local settings if they exist.
try:
    from local_settings import *
except ImportError:
    # this could be heroku, don't barf yet
    if 'LOCAL_SETTINGS' in os.environ.keys():
        from django.conf import settings
        settings.__dict__.update(json.loads(os.environ['LOCAL_SETTINGS']))
    else:
        sys.stderr.write("Unable to load local settings. Make sure local_settings.py exists and is free of errors.\n")
