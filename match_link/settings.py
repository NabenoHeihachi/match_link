"""
Django settings for MATCH LINK.
"""

from pathlib import Path
import environ
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# ----- General settings -----
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG_MODE')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# ----- Application definition setting -----
AUTH_USER_MODEL = 'app_account.AccountModel'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'app_document',
    'app_matching',
    'app_profile',
    'app_account',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'match_link.urls'


# ----- Template setting -----
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ----- wsgi application -----
WSGI_APPLICATION = 'match_link.wsgi.application'


# ----- Database setting -----
DATABASES = {
    "default": dj_database_url.config(
        default=env('DATABASE_URL'),
        conn_max_age=600
    )
}


# ----- Password validation setting -----
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


# ----- Internationalization setting -----
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True


# ----- Static files (CSS, JavaScript, Images) setting -----
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ----- Media files setting -----
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ----- Default primary key field type -----
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ----- Security setting -----
LOGIN_URL = "app_account:login"
SESSION_COOKIE_AGE = 60 * 60 * 2
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSRF_COOKIE_NAME = "csrf_token"

if env.bool('IS_PRODUCTION'):
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 86400
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
else:
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_PRELOAD = False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False

# ----- axes setting -----
AXES_FAILURE_LIMIT = 4
AXES_COOLOFF_TIME = 1
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_PARAMETERS = ["username"]
AXES_LOCKOUT_TEMPLATE = "lockout.html"


# ----- Log setting -----
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'timelog': {
            'format': '[%(asctime)s][%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },

    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, f'logs/info.log'),
            'formatter': 'timelog',
            'when': 'midnight', 
            'backupCount': 30, 
            'encoding':'utf-8',
        },
    },

    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# ----- Init User -----
INIT_ACCOUNT_ID = env("INIT_ACCOUNT_ID")
INIT_PASSWORD = env("INIT_PASSWORD")

# ----- LLM API URL -----
LLM_API_URL = env("LLM_API_URL")
LLM_MODEL = env("LLM_MODEL")
