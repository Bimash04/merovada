"""
Django settings for MeroVada project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import pymysql
pymysql.install_as_MySQLdb()

import os
from pathlib import Path

import dj_database_url
from django.conf import settings
from django.conf.urls.static import static

BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY key
SECRET_KEY = "django-insecure-7q$c4*t3stt0723v+*_saydo+y7$a_0up38l78%_hrd5-!0dow"


DEBUG = False

# Add to ALLOWED_HOSTS
ALLOWED_HOSTS = ['localhost', '127.0.0.1','*']


# Khalti Configuration

KHALTI_PUBLIC_KEY = "1dce43999516436dafde8f8141fbf0ad"  
KHALTI_SECRET_KEY = "48291051ceb24fe39659b652ed17f3fc"  
# Application definition

INSTALLED_APPS = [
    "daphne",
    # "django.contrib.admin", we are not using admin panel we make custom admin panel
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Register",
    'channels',
    "owner",
    "renter",
    "Payment",
    "notifications",
    'chat',
    'chatbot',
    'widget_tweaks',
    'Blog',
    "rest_framework",
    "cms",
    'recom',

    
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MeroVada.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR ,"/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom context processor
                'renter.context_processors.cart_item_count',
            ],
        },
    },
]

# ASGI_APPLICATION = 'MeroVada.asgi.application'

WSGI_APPLICATION = "MeroVada.wsgi.application"



ASGI_APPLICATION = "MeroVada.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}



urlpatterns = []
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",  
#     }
# }



# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = 'Register.CustomUser'



# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# https://docs.djangoproject.com/en/4.2/howto/static-files/
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / 'renter/static']


# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'Register.CustomUser'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bimash.dulal.logicseed@gmail.com'
EMAIL_HOST_PASSWORD = 'wjxq jbpm lfbf fcgd'
DEFAULT_FROM_EMAIL = 'MeroVada <your-email@gmail.com>'



DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"), conn_max_age=600
    )
}
# # Database Connection
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'MeroVada',  
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': '127.0.0.1',  
#         'PORT': '3306',  
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#         }
#     }
# }




# Logging for debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}