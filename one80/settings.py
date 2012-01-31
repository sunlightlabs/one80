# Django settings for one80 project.
import datetime
import json
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIASYNC = {
    'BACKEND': 'mediasync.backends.s3',
    'AWS_BUCKET': "assets.sunlightfoundation.com",
    'AWS_PREFIX': "one80/static",
    'DOCTYPE': 'xhtml',
    'CACHE_BUSTER': datetime.datetime.now().strftime('%s'), #only ok with 1 web head!!
    'SERVE_REMOTE': True,
    'JOINED': {
        'css/joined.css': [
            'css/style.css',
            'css/annotation.css',
        ],
        'js/joined.js': [
            'js/vendor/jquery.min.js',
            'js/vendor/jquery-ui.min.js',
            'js/vendor/jquery.annotate.js',
            'js/vendor/moment.js',
            'js/app.js',
        ],
    },
}

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
    'django_extensions',
    'debug_toolbar',
    'mediasync',
    'social_auth',
    'south',
    # 'whoosh',
    'haystack',
    'one80',
    'one80.auth',
    'one80.committees',
    'one80.people',
    'one80.photos',
    'one80.search',
    'template_repl',
)

INTERNAL_IPS = ('127.0.0.1',)

AUTH_PROFILE_MODULE = 'auth.UserProfile'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/login/complete/'
LOGOUT_URL = '/logout/'
FACEBOOK_EXTENDED_PERMISSIONS = ['email',]
COMPLETE_PROFILE_MESSAGE = 'You\'re almost done, we just need an email address or phone number to complete your profile.'
ADMIN_COMPLETE_PROFILE_MESSAGE = 'Your profile is not complete. Go here to add an email address or phone nubmer.'

# search
HAYSTACK_SITECONF = 'one80.search_sites'
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_XAPIAN_PATH = '%s/data/xapian/one80_index' % PROJECT_ROOT

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