import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
    'suit',
    #'suit_redactor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    'raven.contrib.django.raven_compat',
    'django_date_extensions',
    'storages',
    'markdown_deux',
    'djrill',
    'django_nose',
    'easy_thumbnails',
    'captcha',
    'django_countries',
    'bootstrap3_datetime',
    'ckeditor',
    'gulp_rev',

    'core',
    'applications',
    'jobs',
    'patreonmanager.apps.PatreonManagerConfig',
)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'djangogirls.urls'

WSGI_APPLICATION = 'djangogirls.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {}
DATABASES['default'] = dj_database_url.config(
    default='postgres://postgres:@localhost:5432/djangogirls')

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

SUIT_CONFIG = {
    'ADMIN_NAME': 'Django Girls',
    'SEARCH_URL': '/admin/core/event/',
    'MENU': (
        {'label': 'Users & Groups', 'icon':'icon-user', 'models': ('core.user', 'auth.group')},
        {'label': 'Events', 'icon':'icon-star', 'models': (
            'core.event', 'core.eventpage', 'core.eventpagecontent',
            'core.eventpagemenu', 'core.postmortem',
        )},
        {'label': 'Application Form', 'app': 'applications', 'icon':'icon-tasks'},
        {'label': 'Submitted Applications', 'url': '/admin/applications/form/submissions/', 'icon':'icon-user'},
        {'app': 'flatpages', 'icon':'icon-file'},
        {'label': 'Blog & Django Stories', 'icon':'icon-comment', 'models': ('core.Story',)},
        {'app': 'jobs', 'icon':'icon-briefcase'},
        {'app': 'patreonmanager', 'icon':'icon-gift', 'models': ('patron', 'payment', 'reward')},
        {'label': 'Organizer\'s Manual', 'icon':'icon-bookmark', 'url': 'http://organize.djangogirls.org/'},
        {'label': 'Organizer\'s FAQ', 'icon':'icon-bookmark', 'url': 'http://organize.djangogirls.org/faq/'},
        {'label': 'Organizer\'s Google Group', 'icon':'icon-bookmark', 'url': 'https://groups.google.com/forum/#!forum/django-girls-organizers'},
        {'label': 'Organizer\'s Slack', 'icon':'icon-bookmark', 'url': 'https://djangogirls.slack.com/'},
        {'label': 'Support', 'icon':'icon-question-sign', 'url': 'https://groups.google.com/forum/#!forum/django-girls-organizers'},
    )
}

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

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/local')]
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/build')]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN')
}

MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_APIKEY')

MANDRILL_API_KEY = os.environ.get('MANDRILL_APIKEY')
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND",
                               "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = "hello@djangogirls.org"

SLACK_API_KEY = os.environ.get('SLACK_API_KEY')

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
# Using new No Captcha reCaptcha with SSL
NOCAPTCHA = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=core,applications,jobs',
    '--with-progressive',
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
SSLIFY_DISABLE = DEBUG

# Mapbox maps to use on the Events map
MAPBOX_MAP_ID = 'olasitarska.m8nged0f'

APPEND_SLASH = True

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
    		 ['-', 'Bold', 'Italic', 'Underline'],
             ['-', 'Link', 'Unlink'],
             ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-'],
        ],
    },
}

JOBS_EMAIL_USER = os.environ.get('JOBS_EMAIL_USER')
JOBS_EMAIL_PASSWORD = os.environ.get('JOBS_EMAIL_PASSWORD')

MEETUPS_EMAIL_USER = os.environ.get('MEETUPS_EMAIL_USER')
MEETUPS_EMAIL_PASSWORD = os.environ.get('MEETUPS_EMAIL_PASSWORD')

if 'OPBEAT_SECRET_TOKEN' in os.environ:
    INSTALLED_APPS += (
        'opbeat.contrib.django',
    )
    OPBEAT = {
        'ORGANIZATION_ID': os.environ['OPBEAT_ORGANIZATION_ID'],
        'APP_ID': os.environ['OPBEAT_APP_ID'],
        'SECRET_TOKEN': os.environ['OPBEAT_SECRET_TOKEN'],
    }
    MIDDLEWARE_CLASSES = (
        'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    ) + MIDDLEWARE_CLASSES

CODEMIRROR_PATH = "vendor/codemirror/"
