import os
import sys
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_URL = 'https://djangogirls.org'

DEBUG = os.getenv('DJANGO_DEBUG') != 'FALSE'

if DEBUG:
    SECRET_KEY = 'hello!'
else:
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'django_date_extensions',
    'django_unused_media',
    'django_extensions',
    'storages',
    'markdown_deux',
    'easy_thumbnails',
    'captcha',
    'django_countries',
    'gulp_rev',

    'core',
    'applications',
    'organize',
    'patreonmanager',
    'story',
    'sponsor',
    'coach',
    'contact',
    'pictures',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'djangogirls.urls'

WSGI_APPLICATION = 'djangogirls.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')

DATABASES = {}
DATABASES['default'] = dj_database_url.config(
    default='postgres://postgres:{}@localhost:5432/djangogirls'.format(POSTGRES_PASSWORD)
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'core.context_processors.statistics',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

# Custom

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

AUTH_USER_MODEL = 'core.User'

THUMBNAIL_PRESERVE_EXTENSIONS = True
THUMBNAIL_ALIASES = {
    '': {
        'coach': {'size': (160, 160), 'crop': "smart"},
        'sponsor': {'size': (204, 204), 'crop': False}
    },
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
DJANGO_GULP_REV_PATH = os.path.join(BASE_DIR, 'static/rev-manifest.json')
LOGIN_URL = 'admin:login'

if 'GITHUB_ACTIONS' in os.environ:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/source')]
    RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
    SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
elif DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/local')]
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/build')]


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

SENTRY_DSN = os.environ.get('SENTRY_DSN')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )

MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_APIKEY')

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND",
                               "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = "hello@djangogirls.org"

SLACK_API_KEY = os.environ.get('SLACK_API_KEY')

if 'test' in sys.argv:
    SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
else:
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')

# Using new No Captcha reCaptcha with SSL
NOCAPTCHA = True

STORE_DISCOUNT_CODE = os.environ.get('STORE_DISCOUNT_CODE')

TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')

NOSE_ARGS = []

# Optionally enable coverage reporting
if os.environ.get('COVERAGE') == 'TRUE':
    NOSE_ARGS += [
        '--with-coverage',
        '--cover-package=core,applications,patreonmanager',
    ]

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": "escape",
    },
    "trusted": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": False,
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG

# Mapbox maps to use on the Events map
MAPBOX_MAP_ID = 'olasitarska.m8nged0f'

APPEND_SLASH = True

JOBS_EMAIL_USER = os.environ.get('JOBS_EMAIL_USER')
JOBS_EMAIL_PASSWORD = os.environ.get('JOBS_EMAIL_PASSWORD')

MEETUPS_EMAIL_USER = os.environ.get('MEETUPS_EMAIL_USER')
MEETUPS_EMAIL_PASSWORD = os.environ.get('MEETUPS_EMAIL_PASSWORD')

CODEMIRROR_PATH = "vendor/codemirror/"


GAPPS_ADMIN_SDK_SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
GAPPS_PRIVATE_KEY_ID = os.environ.get('GAPPS_PRIVATE_KEY_ID', '')
GAPPS_PRIVATE_KEY = os.environ.get('GAPPS_PRIVATE_KEY', '')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
