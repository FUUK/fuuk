# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = None

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = ('modeltranslation',
                  'django.contrib.admin',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.humanize',
                  'django.contrib.messages',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.staticfiles',
                  'email_obfuscator',
                  'markdownx',
                  'fuuk.common',
                  'fuuk.fuflatpages',
                  'fuuk.people')
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'fuuk/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                'fuuk.people.context_processors.news_list',
            ),
            'debug': DEBUG,
        },
    },
]

ROOT_URLCONF = 'fuuk.urls'

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/fuuk.db',
    }
}

LANGUAGE_CODE = 'en'
LANGUAGES = (('en', u'English'),
             ('cs', u'Česky'))
TIME_ZONE = 'Europe/Prague'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#XXX: Remove these
LOCALE_PATHS = (os.path.join(BASE_DIR, 'fuuk/locale'), )

# Markdownx settings
MARKDOWNX_MARKDOWN_EXTENSIONS = (
    'markdown.extensions.tables',
    'markdown.extensions.attr_list'
)
