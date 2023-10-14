import os
from celery.schedules import crontab
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path

import django.core.cache.backends.filebased

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_evop.apps.AppEvopConfig',
    'captcha',
    'api_evop.apps.ApiEvopConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'energy_values.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'energy_values.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'evop',
        'USER': os.getenv('USER_PSQL'),
        'PASSWORD': os.getenv('PASSWORD_DB'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = [os.path.join(BASE_DIR, 'static')]
STATICFILES_DIR = []

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('ADMIN_EMAIL')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SERVER_EMAIL = EMAIL_HOST_USER

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_FONT_SIZE = 40
CAPTCHA_IMAGE_SIZE = (140, 70,)
CAPTCHA_BACKGROUND_COLOR = '#160848'
CAPTCHA_FOREGROUND_COLOR = '#fdc073'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# LOGIN_REDIRECT_URL='/'
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                      'LOCATION': os.path.join(BASE_DIR, 'evop_cache')
                      }
          }

REST_FRAMEWORK = {'DEFAULT_RENDERER_CLASSES':
                      ['rest_framework.renderers.JSONRenderer',
                       'rest_framework.renderers.BrowsableAPIRenderer'],  # <-if not-->only GET (not delete,put,patch)
                  'DEFAULT_PERMISSION_CLASSES': [
                      'rest_framework.permissions.AllowAny',
                  ],
                  'DEFAULT_AUTHENTICATION_CLASSES': [
                      'rest_framework_simplejwt.authentication.JWTAuthentication',  # # jwt-token authentication
                      'rest_framework.authentication.TokenAuthentication',  # token authentication
                      'rest_framework.authentication.BasicAuthentication',  # session authentication
                      'rest_framework.authentication.SessionAuthentication',  # session authentication
                  ],
                  'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
                  }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Energy values of products(EVOP) API",
    "DESCRIPTION": "Here you can not only study all the endpoints of the application,"
                   "but also immediately test them in action, send any request and get an answer.",
    "VERSION": "1.0.0",  # версия проекта
    "SERVE_INCLUDE_SCHEMA": False,  # исключить эндпоинт /schema
    "SWAGGER_UI_SETTINGS": {"filter": True, 'deepLinking': True, },  # включить поиск по тегам
    "CONTACT": {"name": "Dmitry Marhalik", "email": "dmitrymarhalik@gmail.com"},
    "COMPONENT_SPLIT_REQUEST": True
}

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Africa/Nairobi'

CELERY_BEAT_SCHEDULE = {  # scheduler configuration
    'Update_Products_In_The_DB': {
        'task': 'app_evop.tasks.update_products_in_the_db',
        'schedule': crontab('10', '12', day_of_month='31',
                            month_of_year='8')},
    'Update_Dishes_In_The_DB': {
        'task': 'app_evop.tasks.update_dishes_in_the_db',
        'schedule': crontab('01', '12', day_of_month='31',
                            month_of_year='8')}
}
# sudo lsof -t -i tcp:8000 | xargs kill -9  --------- reset port