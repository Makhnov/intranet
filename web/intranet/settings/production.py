from .base import *

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

# Wagtail settings
INTERNAL_IPS = '127.0.0.1:8000'
WAGTAIL_SITE_NAME="intranet 3cgs"
SITE_ID = 1
ALLOWED_HOSTS = ['.localhost', '127.0.0.1', 'intranet.cagiregaronnesalat.fr', '[::1]']

CSRF_TRUSTED_ORIGINS = ['https://intranet.cagiregaronnesalat.fr', 'https://www.intranet.cagiregaronnesalat.fr', 'https://cagiregaronnesalat.fr', 'https://www.cagiregaronnesalat.fr']
SECURE_HSTS_SECONDS = 60
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

try:
    from .local import *
except ImportError:
    pass
