import os
from os.path import dirname, join

from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = dirname(dirname(dirname(__file__)))

SECRET_KEY = os.getenv(
    "SECRET_KEY", default='django-insecure-)lg*r+g30=z!0d1v_9do=oi_lx(qkpvyt@8fomhs)1u(1&1i*9')

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
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework_simplejwt',
    'rest_framework_mongoengine',
    'drf_yasg',
    'base',
    'api_users',
    'api_auth',
    'api_pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.exception.ExceptionMiddleware'
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
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
API_HOST = os.getenv("API_HOST", default="localhost:8000")
DEFAULT_HOST = os.getenv("DEFAULT_HOST", default="localhost:8000")

AUTH_USER_MODEL = 'api_users.User'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

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
DATABASE_ROUTERS = ['core.utils.db_routers.DatabaseRouter',]

# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
    },
    'db_users': {
        "ENGINE": 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME_01", default="mydb"),
        "USER": os.getenv("DB_USER_01", default="mydb"),
        "PASSWORD": os.getenv("DB_PASSWORD_01", default="mydb"),
        "HOST": os.getenv("DB_HOST_01", default="mydb"),
        "PORT": os.getenv("DB_PORT_01", default="mydb"),
        "OPTIONS": {"charset": "utf8mb4"},
    },
    'db_tasks': {
        "ENGINE": 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME_02", default="mydb"),
        "USER": os.getenv("DB_USER_02", default="mydb"),
        "PASSWORD": os.getenv("DB_PASSWORD_02", default="mydb"),
        "HOST": os.getenv("DB_HOST_02", default="mydb"),
        "PORT": os.getenv("DB_PORT_02", default="mydb"),
        "OPTIONS": {"charset": "utf8mb4"},
    },
    'nosql': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

from mongoengine import connect

MONGO_DB_URI = os.getenv("MONGO_DB_URI", default = "mongodb://root:root@mongo:27017")

connect(host=MONGO_DB_URI)

CACHE_TTL = 60 * 1500

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", default="redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_IGNORE_RESULT = True
CELERY_BROKER_URL = os.environ.get('CELERY_URL')
CELERYD_HIJACK_ROOT_LOGGER = False
REDIS_CHANNEL_URL = os.environ.get('REDIS_CHANNEL_URL')

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
