from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-jc$23*h%wtjs&4=+2x$ovklg#wlemz07_7p=5bar89u+e*dr+d"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Général
SITE_ID = 1
INTERNAL_IPS = "127.0.0.1:8000"
WAGTAIL_SITE_NAME = "intranet 3cgs"

try:
    from .local import *
except ImportError:
    pass
