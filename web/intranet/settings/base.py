"""
Django settings for intranet project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os 
from termcolor import colored
from django.utils.translation import gettext_lazy as _

# Ignorer les warnings spécifiques à `RemovedInWagtail70Warning`
import warnings
from wagtail.utils.deprecation import RemovedInWagtail70Warning
warnings.filterwarnings("ignore", category=RemovedInWagtail70Warning)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = os.environ.get('WAGTAILADMIN_BASE_URL', 'http://localhost:8000')
WAGTAILAPI_BASE_URL = os.environ.get('WAGTAILAPI_BASE_URL', 'http://localhost:8000')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Application definition
INSTALLED_APPS = [
    "dashboard",  # Modifs sur le panneau d'admin  
        
    # Modeles Custom
    "users",  # https://docs.wagtail.org/en/stable/advanced_topics/customisation/custom_user_models.html#custom-user-models
    "images", # https://docs.wagtail.org/en/stable/advanced_topics/images/custom_image_model.html#custom-image-models  
    # Custom
    
    # Docx import
    # "wagtail_content_import", # https://torchbox.github.io/wagtail-content-import/
    # "wagtail_content_import.pickers.google", # https://torchbox.github.io/wagtail-content-import/google_docs_setup/
    # "wagtail_content_import.pickers.microsoft", # https://torchbox.github.io/wagtail-content-import/microsoft_setup/
    # "wagtail_content_import.pickers.local", # https://torchbox.github.io/wagtail-content-import/basic_usage/
    # Docx import
    
    "home",
    "accompte", # Fausse page d'accompte (pour les restrictions, les icones, etc.) Pour le backend du login/logout voir le package django-allauth
    "intranet.templatetags",  # https://docs.djangoproject.com/en/dev/howto/custom-template-tags/
    "amicale",  # Le blog de l'amicale
    "administration",  # La partie de l'intranet réservée aux élus (CR, convocations, etc.)
    "agents",  # La partie de l'intranet réservée aux agents (FAQ, etc.)
    "mailing",
    "intranet",  
    "corsheaders",
    "wagtail.contrib.forms", # https://docs.wagtail.org/en/latest/reference/contrib/forms/
    "wagtail.contrib.table_block",  # https://docs.wagtail.org/en/stable/reference/contrib/table_block.html
    "wagtail.contrib.typed_table_block", # https://docs.wagtail.org/en/stable/reference/contrib/typed_table_block.html
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",  # Allauth need this
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",  # Allauth need this
    "django.contrib.messages",  # Allauth need this
    "django.contrib.staticfiles",
    
    # "wagtail_content_import", # https://torchbox.github.io/wagtail-content-import/
    # "wagtail_content_import.pickers.google", # Requis par wagtail content import (API Google)
    # "wagtail_content_import.pickers.microsoft", # Requis par wagtail content import (API Microsoft)
    # "wagtail_content_import.pickers.local", # Requis par wagtail content import (API locale)

    # Charts 
    # "wagtailcharts", # https://github.com/overcastsoftware/wagtailcharts?tab=readme-ov-file#wagtail-charts
    # Charts
    
    # Formulaires
    "wagtailstreamforms", # https://wagtailstreamforms.readthedocs.io/en/latest/
    "generic_chooser", # Requis par wagtailstreamforms   
    # Formulaires

    # Calendrier
    "ls.joyous",
    "events",
    # jours-feries-france : https://github.com/etalab/jours-feries-france
    # Calendrier    
    
    # Menus
    "wagtail_modeladmin",  # Requis par wagtail menus
    "wagtailmenus", # https://docs.wagtail.org/en/stable/reference/contrib/modeladmin/index.html
    # Menus
    
    # PDF
    "wagtail_pdf_view", # https://github.com/donhauser/wagtail-pdf
    "wagtail.contrib.routable_page", # Requis par wagtail pdf view
    # "weasyprint", # https://github.com/fdemmer/django-weasyprint#django-weasyprint
    # PDF
    
    # Media
    "wagtailmedia",  # https://github.com/torchbox/wagtailmedia#wagtailmedia
    # Media
    
    # Interace Admin : Guide, Quickcreate
    "wagtailquickcreate",  # https://github.com/torchbox/wagtailquickcreate#wagtail-quick-create
    "wagtail_guide",  # https://github.com/torchbox/wagtailguide#installation
    "wagtail.contrib.settings",
    # Interface Admin
    
    # GeoWidget
    "wagtailgeowidget", 
    # Fonctionne avec Leaflet pour le mapping et Nominatim pour la recherche d'adresse
    # https://github.com/Frojd/wagtail-geo-widget/blob/main/docs/getting-started-with-leaflet.md
    # https://github.com/Frojd/wagtail-geo-widget/blob/main/docs/supported-geocoders.md#nominatim
    # GeoWidget
    
    # Allauth
    "django_countries",
    "allauth",  # https://django-allauth.readthedocs.io/en/latest/account/index.html
    "allauth.account",
    "allauth.socialaccount",
    # Allauth
    
    # socials
    # socials
    
    # Api
    "wagtail.api.v2",  # https://docs.wagtail.org/en/stable/advanced_topics/api/index.html#wagtail-api
    "rest_framework",  # https://www.django-rest-framework.org/
    "rest_framework.authtoken",
    "dj_rest_auth",  # https://dj-rest-auth.readthedocs.io/en/latest/
    "dj_rest_auth.registration",
    # Api
]

MIDDLEWARE = [
    # https://docs.coderedcorp.com/wagtail-cache/getting_started/install.html#install
    # UpdateCacheMiddleware must come FIRST and
    # FetchFromCacheMiddleware must come LAST in the list of middleware to correctly cache everything
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "accompte.middleware.CGSProfileMiddleware",
]

ROOT_URLCONF = "intranet.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # Allauth need this
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailmenus.context_processors.wagtailmenus",
            ],
        },
    },
]

# Database PostgreSQL
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("SQL_DATABASE", "intranet-dev"),
        "USER": os.environ.get("SQL_USER", "multi"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "root"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        'OPTIONS': {
            'min_length': 10,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

WSGI_APPLICATION = "intranet.wsgi.application"

# Authentification
# https://django-allauth.readthedocs.io/en/latest/installation/quickstart.html
# https://medium.com/@ksarthak4ever/django-custom-user-model-allauth-for-oauth-20c84888c318

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

# AUTH
# CORS_ALLOW_ALL_ORIGINS = True  # Debug
CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)


# ALLAUTH SETTINGS
WAGTAIL_FRONTEND_LOGIN_TEMPLATE = 'account/login.html' # Pas Allauth directement

LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = None
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 0
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = False 
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "3CGS - "

# Rest Framework & APIv2

WAGTAILAPI_SEARCH_ENABLED = True # Debug ??
WAGTAILAPI_LIMIT_MAX = None

# CI-DESSOUS INUTILE ATM
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
    ],
}

DJ_REST_AUTH = {
    "USER_DETAILS_SERIALIZER": "users.serializers.CustomUserDetailsSerializer",
}

REST_USE_JWT = True
# USE_JWT = True

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ("fr", _("French")),
    ("en", _("English")),
    ("es", _("Spanish")),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Django settings
DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"  # Certains package utilise encore ce paramètre (ex: guide, wagtailstreamforms)
)

# Mailing
EMAIL_BACKEND = os.getenv("WAGTAIL_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.getenv("WAGTAIL_EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = os.getenv("WAGTAIL_EMAIL_PORT", 587)
EMAIL_USE_SSL = os.getenv("WAGTAIL_EMAIL_USE_SSL", False)
EMAIL_HOST_PASSWORD = os.getenv("WAGTAIL_EMAIL_HOST_PASSWORD", "password")
EMAIL_HOST_USER = os.getenv("WAGTAIL_EMAIL_HOST_USER", "intranet.com")

CGS_REPLY_TO = {
    'conseil': "secretariat",
    'commissions': "secretariat",
    'bureau': "claire.legal",
    'conference': "secretariat",
    'amicale': "amicale",
    'faq': "rh",
    'home': "secretariat",
}

# PDF2Images
POPPLER_PATH = os.getenv("POPPLER_PATH", r"C:\\Program Files\\poppler-24.02.0\\Library\\bin")

# Guide
WAGTAIL_GUIDE_SETTINGS = {
    "ADD_WAGTAIL_GUIDE_TO_HELP_MENU": True,
    "WAGTAIL_GUIDE_MENU_LABEL": "Comment utiliser l'Intranet",
    "HIDE_WAGTAIL_CORE_EDITOR_GUIDE": False,
}

# Divers
WAGTAILADMIN_GLOBAL_EDIT_LOCK = (True,)

TAGGIT_CASE_INSENSITIVE = True
TAG_SPACES_ALLOWED = False

WAGTAIL_WORKFLOW_ENABLED = False
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAILADMIN_COMMENTS_ENABLED = False
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# User model
AUTH_USER_MODEL = "users.User"
WAGTAIL_USER_EDIT_FORM = "users.forms.CustomUserEditForm"
WAGTAIL_USER_CREATION_FORM = "users.forms.CustomUserCreationForm"
WAGTAIL_USER_CUSTOM_FIELDS = [
    "civility",
    "date_of_birth",
    "address1",
    "address2",
    "zip_code",
    "city",
    "mobile_phone",
    "municipality",
    "function_municipality",
    "function_council",
    "commissions",
    "functions_commissions",
    "function_bureau",
    "function_conference"
]

# PAGES DE MENU GENERAL
WAGTAIL_MENU_PAGES = ['HomePage', 'AdministrationIndexPage', 'CommissionsIndexPage', 'RessourcesPage']

# Nombre de jours avant qu'une nouvelle page ne soit considérée comme ancienne
DELTA_NEWS = 14

# Geowidget
GEO_WIDGET_DEFAULT_LOCATION = {"lat": 43.08366, "lng": 0.947}
GEO_WIDGET_ZOOM = 12

# QuickCreate
WAGTAIL_QUICK_CREATE_PAGE_TYPES = [
    ("administration.ConvocationPage", "une convocation"),
    ("administration.CompteRenduPage", "un compte-rendu"),
    ("amicale.AmicalePage", "une page de l'amicale"),
    ("agents.FaqPage", "une page de la FAQ"),
    ("joyous.SimpleEventPage", "un événement"),
    ("joyous.MultiDayEventPage", "un long événement"),
]

WAGTAIL_QUICK_CREATE_DOCUMENTS = True
WAGTAIL_QUICK_CREATE_IMAGES = True
WAGTAIL_QUICK_CREATE_AUDIO = False
WAGTAIL_QUICK_CREATE_VIDEO = False

# Formulaires pour l'amicale
WAGTAILSTREAMFORMS_ENABLE_FORM_PROCESSING = True
WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL = 'home.AdvancedFormSetting'
WAGTAILSTREAMFORMS_DEFAULT_TO_ADDRESS = 'secretariat@cagiregaronnesalat.fr'
WAGTAILSTREAMFORMS_FORM_TEMPLATES = (
    ('widgets/forms/contact.html', 'Formulaire de contact'),    
    ('widgets/forms/amicale.html', 'Inscription à l\'amicale'),
    ('widgets/forms/sortie.html', 'Sorties de l\'amicale'),
    ('widgets/forms/agents.html', 'Formulaire pour les agents'),
    ('widgets/forms/administration.html', 'Formulaire pour les élus'),
    ('widgets/forms/home.html', 'Formulaire pour les pages génériques'),
    ('streamforms/form_block.html', 'Formulaire par défaut'),
)

# Calendrier 
JOYOUS_GROUP_SELECTABLE = False
JOYOUS_UPCOMING_INCLUDES_STARTED = True
JOYOUS_HOLIDAYS = "France"
JOYOUS_DATE_FORMAT = "d F Y"
JOYOUS_DATE_SHORT_FORMAT = "d/m"
JOYOUS_TIME_FORMAT = "H:i"
JOYOUS_TIME_INPUT = "24"

# SVG
WAGTAILIMAGES_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp", "svg"]
WAGTAILIMAGES_IMAGE_MODEL = 'images.CustomImage'

# Custom rich text features
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': ['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr']
        }
    },
    'full': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': [
                'bold', 'italic', 'code', 'strikethrough' , 
                'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul',
                'blockquote', 'hr', 'link'
            ]
        }
    }
}
