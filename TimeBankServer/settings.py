"""
Django settings for TimeBankServer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j^v(2p1!-88gtv)@@fq^0va5l658$p1fo(fu=6v)a&nv#cussf'

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
    'server',
    'rest_framework',
    'rest_framework_swagger',
    #'rest_framework.authtoken'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TimeBankServer.urls'

WSGI_APPLICATION = 'TimeBankServer.wsgi.application'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Heroku Settings start

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

if os.getenv('DATABASE_URL') is not None:
    DATABASES = {'default': dj_database_url.config()}
else:
# Heroku Settings end
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'TimeBank.sqlite',
            }
    }
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'it_IT'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = True

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

AUTH_USER_MODEL = 'server.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    )
}

SWAGGER_SETTINGS={
    "apiVersion": "0.1",
    "swaggerVersion": "1.2",
    "apis": [
        {
            "path": "/categories",
            "description": "Operations about pets"
        },
        {
            "path": "/user",
            "description": "Operations about user"
        },
        {
            "path": "/store",
            "description": "Operations about store"
        }
    ],
    "authorizations": {
        "basicAuth": {
            "type": "basicAuth",
            "passAs": "header",

        }
    },
    "info": {
        "title": "TimeBank Server v2.0",
        "description": "This is a simple TimeBank server.  You can find out more about this project "
                       "at <a href=\"https://github.com/mariotsi/TimeBank-v2.0_back-end\">GitHub</a>.<br/>"
                       "This project uses Basic HTTP Authorization because is intended to use on SSL",
        "contact": "simone@mariotti.me",
        "license": "GPLv3",
        "licenseUrl": "https://github.com/mariotsi/TimeBank-v2.0_back-end/blob/master/LICENSE.md"
    }
}