from pathlib import Path
import os
from decouple import config

# ----------------------------------
# Base Directory
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------
# Secret Key & Debug
# ----------------------------------
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)

# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')
ALLOWED_HOSTS = ['ipbanking.com', 'www.ipbanking.com', '127.0.0.1', 'localhost']


# ----------------------------------
# Application Definition
# ----------------------------------
INSTALLED_APPS = [
    'jet.dashboard',
    'jet',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'django_celery_beat',
    'rest_framework',
    'django_extensions',
    'sslserver',

    # Custom apps
    'accounts',
    'core',
    'transactions',
    'easyaudit',
    'login_history',
    'analytics',
    'banking_system',
    'logger',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # CSRF Middleware (enabled in production)
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]

ROOT_URLCONF = 'banking_system.urls'
AUTH_USER_MODEL = 'accounts.User'

# ----------------------------------
# Templates
# ----------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'banking_system.wsgi.application'

# ----------------------------------
# Database (PostgreSQL)
# ----------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# ----------------------------------
# Password Validation
# ----------------------------------
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

# ----------------------------------
# Internationalization
# ----------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ----------------------------------
# Static Files
# ----------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# ----------------------------------
# Media Files (if used)
# ----------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ----------------------------------
# Security & Session Settings
# ----------------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 1209600

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://your-production-domain.com',  # ✅ Add your real domain here
]

# ----------------------------------
# Login Redirection
# ----------------------------------
LOGIN_REDIRECT_URL = '/'

# ----------------------------------
# Celery Configuration
# ----------------------------------
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# ----------------------------------
# Business Logic Constants
# ----------------------------------
ACCOUNT_NUMBER_START_FROM = 1000000000
MINIMUM_DEPOSIT_AMOUNT = 10
MINIMUM_WITHDRAWAL_AMOUNT = 10

# ----------------------------------
# SSL Config (Optional for Gunicorn + Nginx SSL)
# ----------------------------------
SSL_CERT_PATH = config('SSL_CERT_PATH', default='certs/django_selfsigned.crt')
SSL_KEY_PATH = config('SSL_KEY_PATH', default='certs/django_selfsigned.key')

# ----------------------------------
# Default Primary Key Field Type
# ----------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
