from ntpath import join
import os
import environ
from os.path import exists, dirname, join
from pathlib import Path

from oauth.tokens import signed_token_generator

from ..scopes import scopes,default_scopes
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = dirname(dirname(dirname(__file__)))

SECRET_KEY = os.getenv("SECRET_KEY",default='django-insecure-)lg*r+g30=z!0d1v_9do=oi_lx(qkpvyt@8fomhs)1u(1&1i*9')

DEBUG = os.getenv("DEBUG", default=True)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework_api_key",
    'oauth2_provider',
    'rest_framework',
    'rest_framework_swagger',
    'drf_yasg',
    'base',
    'oauth',
    'api_users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    # "DEFAULT_PERMISSION_CLASSES": ["oauth.permissions.CustomTokenScope"],
    "DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.IsAuthenticated"]
}

OIDC_RSA_PRIVATE_KEY_FILE = os.getenv("OIDC_RSA_PRIVATE_KEY_FILE", default="")

OIDC_RSA_PRIVATE_KEY_FILE = (
    join(BASE_DIR, OIDC_RSA_PRIVATE_KEY_FILE)
    if not OIDC_RSA_PRIVATE_KEY_FILE.startswith("/")
    else OIDC_RSA_PRIVATE_KEY_FILE
)

with open(OIDC_RSA_PRIVATE_KEY_FILE) as f:
    OIDC_RSA_PRIVATE_KEY = f.read()


AUTH_USER_MODEL = "api_users.User"

OAUTH2_PROVIDER_APPLICATION_MODEL = "oauth.Application"
OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = "oauth.AccessToken"
OAUTH2_PROVIDER_ID_TOKEN_MODEL = "oauth.IDToken"
OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = "oauth.RefreshToken"
OAUTH2_PROVIDER_GRANT_MODEL = "oauth.Grant"

AUTHENTICATION_BACKENDS = (
    "oauth.backends.CustomOAuth2Backend",
    "django.contrib.auth.backends.ModelBackend",
)
OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": OIDC_RSA_PRIVATE_KEY,
    "SCOPES": scopes,
    "DEFAULT_SCOPES": default_scopes,
    "SCOPES_BACKEND_CLASS": "oauth.settings_scopes.SettingsScopes",
    "OAUTH2_VALIDATOR_CLASS": "oauth.oauth_validators.CustomOAuth2Validator",
    "ACCESS_TOKEN_GENERATOR": signed_token_generator(
        OIDC_RSA_PRIVATE_KEY, 
    ),
    "REFRESH_TOKEN_GENERATOR": "oauthlib.oauth2.rfc6749.tokens.random_token_generator",
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,
    "REFRESH_TOKEN_GRACE_PERIOD_SECONDS": 4000,
    
}

DEFAULT_CLIENT_SECRET = os.getenv("DEFAULT_CLIENT_SECRET", default="DEFAULT_CLIENT_SECRET")

DEFAULT_CLIENT_ID = os.getenv("DEFAULT_CLIENT_ID", default="DEFAULT_CLIENT_ID")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", default=587)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL", default="Django-example <noreply@domain.com>"
)

# Database
DATABASE_ROUTERS = ['core.utils.db_routers.NonRelRouter', ]

# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DB_NAME = os.getenv("DB_NAME", default="mydb")
DATABASES = {
    'default': {
        "ENGINE": os.getenv("SQL_ENGINE", default="django.db.backends.mysql"),
        'NAME': DB_NAME,
        "USER": os.getenv("DB_USER", default="mydb"),
        "PASSWORD": os.getenv("DB_PASSWORD", default="mydb"),
        "HOST": os.getenv("DB_HOST", default="mydb"),
        "PORT": os.getenv("DB_PORT", default="mydb"),
        "OPTIONS": {"charset": "utf8mb4"},
    },
    # "nonrel": {
    #     "ENGINE": "djongo",
    #     "NAME": os.environ.get('MONGO_DB_NAME'),
    #     "CLIENT": {
    #         "host": os.environ.get('MONGO_DB_HOST'),
    #         "port": int(os.environ.get('MONGO_DB_PORT')),
    #         "username": os.environ.get('MONGO_DB_USERNAME'),
    #         "password": os.environ.get('MONGO_DB_PASSWORD'),
    #     },
    #     'TEST': {
    #         'MIRROR': 'default',
    #     },
    # }
}

CACHE_TTL = 60 * 1500

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL",default="redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
