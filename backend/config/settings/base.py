from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'