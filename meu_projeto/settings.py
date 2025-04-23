from pathlib import Path
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Definir o ambiente (dev ou prod)
TARGET_ENV = os.getenv('TARGET_ENV', 'dev')
NOT_PROD = not TARGET_ENV.lower().startswith('prod')

# Configurações de CSRF confiáveis para produção
CSRF_TRUSTED_ORIGINS = [
    'https://projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net',
    'https://www.projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net',
]

# Cookies CSRF e sessões seguras para produção
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Configuração de ambiente: desenvolvimento ou produção
if NOT_PROD:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', '<django-insecure-fi9t30&0w42w#l*+7#_fy+b6z5y9sl**1&1$2t7flifi8(pwaq>')  # Em desenvolvimento
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
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', 't', '1']
    SECRET_KEY = os.getenv('SECRET_KEY')

    ALLOWED_HOSTS = os.getenv(
        'ALLOWED_HOSTS',
        'projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net www.projetodjango-e7fvgbbchbapdvgn.brazilsouth-01.azurewebsites.net'
    ).split(' ')

    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() in ['true', 't', '1']
    if SECURE_SSL_REDIRECT:
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DBNAME'),  # Nome do banco de dados
            'USER': os.getenv('DBUSER'),  # Usuário do banco de dados
            'PASSWORD': os.getenv('DBPASS'),  # Senha do banco de dados
            'HOST': os.getenv('DBHOST'),  # Host do banco de dados
            'PORT': '5432',  # A porta padrão para PostgreSQL
            'OPTIONS': {
                'sslmode': 'require',  # Exige SSL para a conexão
            },
        }
    }

# Outros ajustes e configurações (não modificados)
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

# Static files (CSS, JavaScript, images)
STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
