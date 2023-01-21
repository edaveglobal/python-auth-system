from datetime import timedelta
import os
from pathlib import Path
from dotenv import load_dotenv
import logging.config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY DEBUG: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY', ''))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG', False))

PROTOCOL = "http"
DOMAIN = "localhost:3000"

if not DEBUG:
    PROTOCOL = "https"
    DOMAIN = "https://gathpay-auth-qb9l6.ondigitalocean.app/"

CSRF_TRUSTED_ORIGINS = ['https://gathpay-auth-qb9l6.ondigitalocean.app']

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'gathpay-auth-qb9l6.ondigitalocean.app']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'djcelery_email',
    'accounts',
    'contactus'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'auth_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # os.path.join(BASE_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'auth_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': str(os.getenv('DATABASE_NAME')),
        'USER': str(os.getenv('DATABASE_USER')),
        'PASSWORD': str(os.getenv('DATABASE_PASSWORD')),
        'HOST': str(os.getenv('DATABASE_HOST')),
        'PORT': str(os.getenv('DATABASE_PORT'))
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_EMAIL_TASK_CONFIG = {
    'name': 'djcelery_email_send',
    'ignore_result': False,
}


    
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    #     'rest_framework.throttling.ScopedRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '5/day',
    #     'user': '10/day',
    #     'register-account': '2/day'
    # }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Logging Configuration
logging.basicConfig(level=(logging.DEBUG))

# Clear prev config
LOGGING_CONFIG = None

# Get loglevel from env
LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', 'info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s \
            [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console',]
        },
    },
})

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_HOST_USER = '6bbf84eeff5d0b'
# EMAIL_HOST_PASSWORD = '4da21a3b1535ca'
# EMAIL_PORT = '2525' 

CELERY_EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', '') 
EMAIL_HOST = str(os.getenv('EMAIL_HOST', ''))
EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER', ''))
EMAIL_PORT = str(os.getenv('EMAIL_PORT', ''))
EMAIL_USE_TLS = bool(os.getenv('EMAIL_USE_TLS', False))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD', ''))
# EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', 60))

def get_cache():
  try:
    servers = os.getenv('MEMCACHIER_SERVERS')
    username = os.getenv('MEMCACHIER_USERNAME')
    password = os.getenv('MEMCACHIER_PASSWORD')
    return {
      'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'TIMEOUT': 60*10,
        'LOCATION': servers,
        'OPTIONS': {
          'username': username,
          'password': password,
        }
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'}
    }

CACHES = get_cache()