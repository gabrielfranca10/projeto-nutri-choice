from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

TARGET_ENV = os.getenv('TARGET_ENV', 'dev')
NOT_PROD = not TARGET_ENV.lower().startswith('prod')

# CSRF confiáveis — funcionam em dev e prod com HTTPS
CSRF_TRUSTED_ORIGINS = [
    'https://projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net',
    'https://www.projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net',
]

# Cookies CSRF
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

if NOT_PROD:
    DEBUG = True
    SECRET_KEY = '<django-insecure-fi9t30&0w42w#l*+7#_fy+b6z5y9sl**1&1$2t7flifi8(pwaq>'
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        'projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net',
        'www.projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net',
    ]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']
    SECRET_KEY = os.getenv('SECRET_KEY')

    ALLOWED_HOSTS = os.getenv(
        'ALLOWED_HOSTS',
        'projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net www.projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net'
    ).split(' ')

    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']
    if SECURE_SSL_REDIRECT:
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DBNAME'),
            'HOST': os.getenv('DBHOST'),
            'USER': os.getenv('DBUSER'),
            'PASSWORD': os.getenv('DBPASS'),
            'OPTIONS': {'sslmode': 'require'},
        }
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'meu_app',
    'whitenoise.runserver_nostatic',
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
]

ROOT_URLCONF = 'meu_projeto.urls'

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

WSGI_APPLICATION = 'meu_projeto.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'