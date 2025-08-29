import os
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = BASE_DIR.parent / 'config' / 'config.yml'
_config = {}
if CONFIG_PATH.exists():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        _config = yaml.safe_load(f) or {}

# Helper: prefer ENV, then YAML, then default
def _env_or_config(name, default=None):
    v = os.getenv(name)
    if v is not None:
        return v
    return _config.get(name, default)

SECRET_KEY = _env_or_config('SECRET_KEY', 'changeme')
_debug_raw = _env_or_config('DEBUG', True)
if isinstance(_debug_raw, bool):
    DEBUG = _debug_raw
else:
    DEBUG = str(_debug_raw) in ('True', 'true', '1')

_allowed = _env_or_config('ALLOWED_HOSTS', ['*'])
if isinstance(_allowed, (list, tuple)):
    ALLOWED_HOSTS = list(_allowed)
else:
    ALLOWED_HOSTS = str(_allowed).split(',') if _allowed else []

# Max quotes per source
MAX_QUOTES_PER_SOURCE = int(_env_or_config('MAX_QUOTES_PER_SOURCE', _config.get('MAX_QUOTES_PER_SOURCE', 3)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.quotes',
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

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'data' / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'
