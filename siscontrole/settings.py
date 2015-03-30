"""
Django settings for siscontrole project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
import django.db.models.options as options

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=huhp_5ctp)=w$l5*b)+wp1iu$-u5xo&zgl)^cwi8hprx$=wpe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'bootstrap_form',
    'crop_image',
    'datatableview',
    'dashboard_view',
    'sorl.thumbnail',
    'django_localflavor_br',
    'django_select2',
    'bootstrap3_datetime',
    'main',
    'financial',

)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'main/templates'),
    os.path.join(BASE_DIR, 'crop_image/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS.__add__((
    'django.core.context_processors.request',
))

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)



options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('gender', )


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'siscontrole.urls'

WSGI_APPLICATION = 'siscontrole.wsgi.application'

LOGIN_URL = '/login/'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.dirname(os.path.dirname(__file__))+'/locale',
    os.path.dirname(os.path.dirname(__file__))+'/siscontrole/locale',
    os.path.dirname(os.path.dirname(__file__))+'/main/locale',
    os.path.dirname(os.path.dirname(__file__))+'/crop_image/locale',
    os.path.dirname(os.path.dirname(__file__))+'/bootstrap_form/locale',
    os.path.dirname(os.path.dirname(__file__))+'/financial/locale',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    '/'
)

MEDIA_ROOT = os.path.dirname(os.path.dirname(__file__))+ '/uploaded_images/'
MEDIA_URL = '/uploaded_images/'

DEFAULT_IMAGE = '/static/images/default.jpg'

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (u'gender', )

AUTO_RENDER_SELECT2_STATICS = False


try:
    from local_settings import *
except ImportError:
    pass