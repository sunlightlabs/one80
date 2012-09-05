from one80.settings import PROJECT_ROOT

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

EMAIL_BACKEND = "postmark.backends.PostmarkBackend"
EMAIL_FROM = ""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

HAYSTACK_WHOOSH_PATH = '%s/data/whoosh/one80_index' % PROJECT_ROOT


AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''
S3_URL = ''
COMPRESS_URL = S3_URL + ''
COMPRESS_STORAGE = ''
STATICFILES_STORAGE = COMPRESS_STORAGE
STATIC_URL = COMPRESS_URL
COMPRESS_ENABLED = True

TIME_ZONE = 'America/New_York'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
)

AUTHENTICATION_SERVICES = (
    ('twitter', 'http://twitter.com'),
    ('facebook', 'http://facebook.com'),
    ('google', 'http://google.com'),
    ('yahoo', 'http://yahoo.com'),
)

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
FACEBOOK_APP_ID = ''
FACEBOOK_API_SECRET = ''
GOOGLE_CONSUMER_KEY = ''
GOOGLE_CONSUMER_SECRET = ''
GOOGLE_DISPLAY_NAME = ''
BING_APIKEY = ''
LINKEDIN_APIKEY = ''
LINKEDIN_API_SECRET = ''
LINKEDIN_REQUEST_TOKEN = ''
LINKEDIN_REQUEST_TOKEN_SECRET = ''
LINKEDIN_ACCESS_TOKEN = ''
LINKEDIN_ACCESS_TOKEN_SECRET = ''
POSTMARK_API_KEY = ''

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'print_to_screen': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'print_to_screen'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
