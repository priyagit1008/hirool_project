"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import logging
from kombu import (
    Queue,
    Exchange,
)
# from py_commons.common.logger import MyLogger

# override the default with custom logger class
# logging.setLoggerClass(MyLogger)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2)huh6&33c9l00jlva!us%lq@np#n0e=*(j5pt_2*42@&a4b%i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'filters',
    'rangefilter',
    'django_extensions',
    'corsheaders',
    # 'crispy_forms',
]

LOCAL_APPS = [
    'accounts',
    'misc',
    'candidate',
    'gunicorn',
    'clients',
    'interview',
    'libs',



]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# INSTALLED_APPS += ('kombu.transport.django', )

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'reversion.middleware.RevisionMiddleware'
# ]


# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]


# MIDDLEWARE_CLASSES = (
# 'django.contrib.sessions.middleware.SessionMiddleware',
# 'django.middleware.common.CommonMiddleware',
# 'django.middleware.csrf.CsrfViewMiddleware',
# 'django.contrib.auth.middleware.AuthenticationMiddleware',
# 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
# 'django.contrib.messages.middleware.MessageMiddleware',
# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
# 'django.middleware.security.SecurityMiddleware',
# )


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]

X_FRAME_OPTIONS = 'ALLOWALL'

# 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# export LANG ="en_US.UTF-8"
LANG="en_AU.UTF-8"





ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "",
    }
}

# Custom Auth User

AUTH_USER_MODEL = 'accounts.User'

# Restframework Settings

REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DATE_INPUT_FORMATS' : '%d-%m-%Y',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
       # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',

    ],

    'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAuthenticated',
    'rest_framework.permissions.AllowAny',
    'accounts.users.permissions.HiroolReadOnly',
    'accounts.users.permissions.HiroolReadWrite',

),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

}

# Admin Login URL

ADMIN_LOGIN_URL = '/HS456GAG4FAYJSTT0O/hire-admin'
LOGIN_URL = ADMIN_LOGIN_URL

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR + '/static/'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Sentry Raven Config
RAVEN_CONFIG = {
    'dsn': '',
    'release': '1.0.0',
    'name': 'Leads API Service',
    'environment': '',
}

# Logging Config
# LOGGING_DIR = '/var/log/hire_api/'
LOGGING_DIR = '/tmp/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(process)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'api_info': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'api_info.log'),
            'formatter': 'verbose',
        },
        'api_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'api_error.log'),
            'formatter': 'verbose',
        },
        'auth': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'auth.log'),
            'formatter': 'verbose',
        },
        'command': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'command.log'),
            'formatter': 'verbose',
        },
        'audit': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'audit.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['api_info', 'api_error', 'sentry'],
            'level': 'INFO',
        },
        'api': {
            'handlers': ['api_info', 'api_error', 'sentry'],
            'level': 'INFO',
        },
        'auth': {
            'handlers': ['auth', 'sentry'],
            'level': 'INFO',
        },
        'command': {
            'handlers': ['command', 'sentry'],
            'level': 'INFO',
        },
        'audit': {
            'handlers': ['audit', 'sentry'],
            'level': 'INFO',
        },
    },
}


# Celery Config
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "max_retries": 3,
    "interval_start": 0,
    "interval_step": 0.3,
    "interval_max": 1,
}

CELERY_IGNORE_RESULT = True

CELERY_QUEUES = (
    Queue(
        'hire_1',
        Exchange('hire_1'),
        routing_key='hire_1'
    ),
)

CELERY_ROUTES = {
    'libs.tasks.test_task': {
        'queue': 'hire_1',
        'routing_key': 'hire_1',
    },
    
}
# app.conf.broker_transport_options = {'visibility_timeout': 3600}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# AWS Config
AWS_CONFIG = {
    "S3": {
        "BUCKET_NAME": "",
        "REGION": "ap-south-1",
        "ACCESS_KEY": "",
        "SECRET_KEY": "",
        "FOLDERS": {
            "damages": "hire/damages/images/",
        },
    }
}

DATADOG_TRACE = {
    'DEFAULT_SERVICE': 'hire-api',
    'DEFAULT_DATABASE_PREFIX': 'hire-api',
    'TAGS': {
        'name': 'hire-api',
    }
}

CONSUMER_API_CONFIG = {
    'HOST': '',
    'HEADERS': {
        'Authorization': '',
    },
    'URLS': {
    }
}

# Elastic-search Config
ELASTIC_SEARCH_CONFIG = {
    "HOSTS": ["127.0.0.1"],
    "INDEX": "",
}

# SMS Config
SMS_CONFIG1 = {
    'HOST': 'http://www.smsintegra.com/',
    'URL': 'api/smsapi.aspx',
    'SUCCESS_KEYWORD': '100',
    'SEND_TO_KEYWORD': 'mobile',
    'PARAMS': {
                'uid': '',
                'pwd': '',
                'sid': '',
                'type': 0
                }
}


OTP_CONFIG = {
    'MESSAGE': '[#] Use {otp} as your otp to verify your my account. axmuAPCc1ko',
    'ALLOWED_LOGIN_ATTEMPTS': 4,
}

# CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379   '



# Google Maps Config
GOOGLE_MAP_CONFIG = {
    "KEY": "",
    "HOST": "https://maps.googleapis.com/maps/api/",
    "URLS": {
        "DISTANCE_MATRIX": "distancematrix/json?origins={origin}&"
                           "destinations={destination}&key={key}"
    }
}

# Redis Config
REDIS_CONFIG = {
    "HOST": "",
    "PORT": 6379,
    "DB": 0,
    "PASSWORD": "",
}


SMS_CONFIG = {
    "HOST" : ""
}

# ANYMAIL = {

#    "SENDGRID_API_KEY":"<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>"
# }

# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'priyapatil1421997.com'
# EMAIL_HOST_PASSWORD = 'priyaaru'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'priyapatil1421997@gmail.com'
EMAIL_HOST_PASSWORD ='priyaaru'
