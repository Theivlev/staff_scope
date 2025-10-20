from .base import BASE_DIR


SECRET_KEY = 'django-insecure-%@i)-+9g03bpe78!5_tykl2d$jj4z^y#a8-%7&y9c*piiu)8c='

DEBUG = True

ALLOWED_HOSTS = []


SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
