from decouple import config
from datetime import timedelta
import os
from pathlib import Path
from pprint import pprint
from celery.schedules import crontab
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_filters',
    'corsheaders',
    'rest_framework',
    'djoser',
    # 'silk',
    # 'debug_toolbar',
    # 'rest_framework_swagger',
    # 'playground',
    # 'store',
    # 'core',
    # 'tags',
    # 'likes',
    'blog',
    'orders',
    # --USER MANAGEMENT,
    'rest_framework_simplejwt',
    'UserManagement',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.twitter',
    #
    # 'rest_auth',
    # 'rest_auth.registration',
    # 'rest_framework.authtoken',
    # generating openapi3 schema and documentation
    'drf_spectacular',
]

# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_UNIQUE_EMAIL = True

# LOGIN_REDIRECT_URL = '/UserManagement(app name)/profile(url name)/'

# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
# TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP_ID': GOOGLE_CLIENT_ID,
#         'APP_SECRET': GOOGLE_CLIENT_SECRET,
#         'SCOPE': ['profile', 'email'],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     },
#     'twitter': {
#         'KEY': TWITTER_CONSUMER_KEY,
#         'SECRET': TWITTER_CONSUMER_SECRET,
#     },
# }

# from ..google.settings_secret import *  # noqa

AUTHENTICATION_BACKENDS = [
    # ...
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # 'silk.middleware.SilkyMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# if settings.DEBUG:
#     MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

ROOT_URLCONF = 'PortfolioBackend.urls'

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

WSGI_APPLICATION = 'PortfolioBackend.wsgi.application'

# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

from ..cdn.storage_conf import *  # noqa


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # for generating api (openapi 3) schema through drf-spectacular
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# for generating api (openapi 3) schema through drf-spectacular
SPECTACULAR_SETTINGS = {
    # giving a title to our project for the api schema generation
    "TITLE": "PortfolioBackend",
    'DESCRIPTION': 'QandeelKhan.com portfolio project documentation',
    'VERSION': '1.0.0',
    # more settings goes here....
}

AUTH_USER_MODEL = 'UserManagement.User'


DJOSER = {
    'SERIALIZERS': {
        'user_create': 'UserManagement.serializers.UserCreateSerializer',
        'current_user': 'UserManagement.serializers.UserSerializer',
    }
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1)
}

DEFAULT_FROM_EMAIL = 'com.qandeelhaider@gmail.com'

ADMINS = [
    ('Haider', 'com.qandeelhaider@gmail.com')
]

CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'playground.tasks.notify_customers',
        'schedule': 5,
        'args': ['Hi World'],
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO')
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} ({levelname}) - {name} - {message}',
            'style': '{'
        }
    }
}

# -----SIMPLEJWT
SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=24),
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

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}

PASSWORD_RESET_TIMEOUT = 900  # 900 Sec = 15min

# for react origin
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
X_FRAME_OPTIONS = 'DENY'

# -----CORS

# For development purposes.
CORS_ORIGIN_ALLOW_ALL = True
# but in django 4
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = ["https://qandeelkhan.com", "https://www.qandeelkhan.com", "http://0.0.0.0:8000",
                 "http://localhost:8000", "http://localhost:3000", "http://0.0.0.0:8000", "http://portfolio-backend:8000", "portfolio-backend", "localhost:8000", "127.0.0.1:8000", "localhost", "127.0.0.1"]
PASSWORD_RESET_TIMEOUT = 900  # 900 Sec = 15min
# For development purposes.

# we whitelist localhost:3000 because that's where frontend will be served
# CORS_ORIGIN_WHITELIST = ['*']
CORS_ORIGIN_WHITELIST = ["https://qandeelkhan.com", "https://www.qandeelkhan.com", "http://0.0.0.0:8000",
                         "http://localhost:8000", "http://localhost:3000", "http://0.0.0.0:8000"]

# for react origin
# SECURE_CONTENT_TYPE_NOSNIFF = False
# SECURE_BROWSER_XSS_FILTER = False
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# X_FRAME_OPTIONS = 'DENY'
# CSRF_TRUSTED_ORIGINS = ["*"]
CORS_ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CSRF_TRUSTED_ORIGINS = ['https://qandeelkhan.com', "https://www.qandeelkhan.com", "http://0.0.0.0:8000",
                        "http://localhost:8000", "http://localhost:3000", "http://0.0.0.0:8000"]
# As of Django 4.0, the values in the CSRF_TRUSTED_ORIGINS setting must start with a scheme (usually http:// or https://)
