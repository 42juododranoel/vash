import os

from django.utils.translation import gettext_lazy as _

ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = True if os.environ.get('DJANGO_DEBUG') == 'True' else False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USE_TZ = True
USE_L10N = True
USE_I18N = True
TIME_ZONE = 'UTC'
APPEND_SLASH = False
ROOT_URLCONF = 'vash.urls'
WSGI_APPLICATION = 'vash.wsgi.application'

STATIC_URL = '/static/'
STATIC_ROOT = '/resources/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/resources/media'
MEDIA_FOLDER_TEMPORARY = f'{MEDIA_ROOT}/temporary'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    'polymorphic',
    'rest_framework',
    'django_filters',
    'constance',
    'constance.backends.database',
    'easy_thumbnails',
    'filer',
    'mptt',
    'django_ace',
    'softhyphen',

    'page',
    'template',
    'snippet',
    'vash.apps.VashConfig'
]

CONSTANCE_ADDITIONAL_FIELDS = {
    'select_language_field': [
        'django.forms.fields.ChoiceField', {
            'widget': 'django.forms.Select',
            'choices': (('en', 'English'), ('ru', 'Russian'))
        }
    ],
}
frontend_options_help_text = _('Used in picture tag to generate sizes attribute')
CONSTANCE_CONFIG = {
    'SITE_NAME': ('', _('Displayed in og:site_name')),
    'SITE_DOMAIN': ('', _('Displayed in og:url, og:image, and og:image:secure_url')),
    'SITE_LOCALE': ('en_EN', _('Displayed in og:locale')),
    'SITE_LANGUAGE': ('en', _('Used for typographing and hyphenating'), 'select_language_field'),
    'IS_HTTPS_ENABLED': (True, _('Used in og:url, og:image, and og:image:secure_url'), bool),
    'FRONTEND_COLUMNS_COUNT': (16, frontend_options_help_text, int),
    'FRONTEND_BREAKPOINT_SM': (0, frontend_options_help_text, int),
    'FRONTEND_BREAKPOINT_MD': (960, frontend_options_help_text, int),
    'FRONTEND_BREAKPOINT_LG': (1400, frontend_options_help_text, int),
}
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [MEDIA_ROOT],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
}

FILER_DEBUG = DEBUG
FILER_ENABLE_LOGGING = True
FILER_CANONICAL_URL = 'share/'

ACE_WIDGET_OPTIONS = {
    'mode': 'html',
    'theme': 'xcode',
    'width': '100%',
    'wordwrap': True,
    'tabsize': 2,
}
