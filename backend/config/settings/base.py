"""
This is the base settings module of the Django application.

It contains configurations and settings used by the Django project. These include:

- BASE_DIR: The project root directory.
- SECRET_KEY: The secret key used for Django's cryptographic operations.
- DEBUG: Flag to indicate if the project is in debug mode.
- ALLOWED_HOSTS: List of hosts/domains the application can serve.
- INSTALLED_APPS: List of all installed applications which need to be included in the project.
- MIDDLEWARE: List of all middleware used in the project.
- ROOT_URLCONF: The location of the root URL configuration.
- TEMPLATES: Configuration for the templates in the project.
- WSGI_APPLICATION: The location of the WSGI application for deployment.
- DATABASES: Configuration for the project databases.
- AUTHENTICATION_BACKENDS: Authentication backends used in this project.
- AUTH_PASSWORD_VALIDATORS: List of enabled password validators.
- LANGUAGE_CODE: The language code for localization.
- TIME_ZONE: Time zone for date and time formatting.
- USE_I18N: Flag to indicate if internationalization is enabled.
- USE_TZ: Flag to indicate if localization in templates and forms, timezone-aware datetimes and model datetimes are enabled.
- STATIC_URL: The URL to use when referring to static files.
- MEDIA_URL: The URL to use when referring to media files.
- MEDIA_ROOT: Absolute path where media files are stored.
- STATIC_ROOT: Absolute path where static files are collected.
- DEFAULT_AUTO_FIELD: Default primary key to use for models.
- AUTH_USER_MODEL: Custom user model for the project.
- REST_FRAMEWORK: Settings for the Django Rest Framework.
- SIMPLE_JWT: Settings for JSON Web Tokens.
- SPECTACULAR_SETTINGS: Settings for Spectacular, a Django Rest Framework schema generation tool.
- SHOW_DOCS: Flag to control the visibility of the API documentation.
- ADMIN_SITE_HEADER: Text to put at the top of all admin pages.
- ADMIN_SITE_TITLE: Title for the admin pages.
- ADMIN_INDEX_TITLE: Title for the admin index page.
- ADMIN_SITE_URL: The URL for the administrative site.
- SMTP_EMAIL_HOST: The host of the SMTP server. The default value set here is 'smtp.gmail.com'.
- SMTP_EMAIL_HOST_USER: The user of the SMTP server. You can replace 'your-email@gmail.com' with your actual email account within the gmail hosting.
- SMTP_EMAIL_HOST_PASSWORD: The password value associated with the above user of the SMTP server. Replace 'your-password' with your actual account password.
- ANYMAIL: This dictionary includes the settings for different mail providers.

Remember to never expose sensitive information such as your secret key or any database credentials.
"""

import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')
SALT = os.environ.get('SALT', 'changeme')  # currently using only for itsdangerous

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(','),
    )
)

CSRF_TRUSTED_ORIGINS = [
    f"http://{origin}" for origin in ALLOWED_HOSTS
] + [
    f"https://{origin}" for origin in ALLOWED_HOSTS
]

CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS.copy()

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# Application definition

INSTALLED_APPS = [
    # Base modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # External modules
    # social auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # drf
    'rest_framework',

    # sign-up/in
    'rest_framework_simplejwt',

    # openai docs/schema generator + swagger
    'drf_spectacular',

    # email sender
    'anymail',

    # additional useful commands for django
    'django_extensions',

    # cors settings
    'corsheaders',

    # Internal modules
    'apps.core.apps.UserConfig',
    'apps.user.apps.UserConfig',
    'apps.clients.apps.ClientsConfig',
    'apps.maillisting.apps.MaillistingConfig',
    'apps.mailsender.apps.MailsenderConfig',
]

MIDDLEWARE = [
    # Base
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # External
    # for static files
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # Add the account middleware:
    'allauth.account.middleware.AccountMiddleware',

    # Internal
    # healthcheck
    'apps.core.middleware.healthcheck.HealthCheckMiddleware',

    # sql_profiler
    'apps.core.middleware.sql_profiler.SQLProfilerMiddleware',

    # cors middleware
    'corsheaders.middleware.CorsMiddleware',
]
# additional healthcheck settings
HEALTH_CHECK_URL = os.environ.get('HEALTH_CHECK_URL', '/health/')


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'PORT': os.environ.get('DB_PORT', '5432'),  # Default PostgreSQL port
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
)

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

# django-allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
SITE_ID = 1  # new

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'

MEDIA_ROOT = '/vol/web/media'
STATIC_ROOT = '/vol/web/static'

CKEDITOR_UPLOAD_PATH = "uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

# Configure Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Simple JWT/Token settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=24),

    'TOKEN_OBTAIN_SERIALIZER': 'apps.user.serializers.CustomTokenObtainPairSerializer',
}

# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Complexity Solution Group API',
    'DESCRIPTION': 'API Schema for Complexity Solution Group project.',
    'VERSION': '0.1.0',
    'COMPONENT_SPLIT_REQUEST': True,
    'SERVE_INCLUDE_SCHEMA': False,
}
SHOW_DOCS = bool(int(os.environ.get('SHOW_DOCS', 1)))

# Django Admin settings
ADMIN_SITE_HEADER = os.environ.get('ADMIN_SITE_HEADER', 'Complexity Solution Group')
ADMIN_SITE_TITLE = os.environ.get('ADMIN_SITE_TITLE', 'Complexity Solution Group')
ADMIN_INDEX_TITLE = os.environ.get('ADMIN_INDEX_TITLE', 'Welcome to Complexity Solution Group Admin Panel')
ADMIN_SITE_URL = os.environ.get('ADMIN_SITE_URL', 'http://localhost:8000/admin/')

# Anymail settings, you can use all of them or just delete/forget which you won't use
# To choose which env going to use which service, go to {your-env}.py, and select EMAIL_BACKEND from the list there.

# SMTP settings
# EMAIL_HOST = os.environ.get('SMTP_EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.environ.get('SMTP_EMAIL_HOST_USER', 'your-email@gmail.com')
# EMAIL_HOST_PASSWORD = os.environ.get('SMTP_EMAIL_HOST_PASSWORD', 'your-password')

EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', "complexity.solution@gmail.com")

ANYMAIL = {
    # SendGrid settings
    'SENDGRID_API_KEY': os.environ.get('SENDGRID_API_KEY', 'your-sendgrid-api-key'),
    'SENDGRID_GENERATE_MESSAGE_ID': os.environ.get('SENDGRID_GENERATE_MESSAGE_ID', True),

    # Amazon SES settings
    'SES_ACCESS_KEY_ID': os.environ.get('SES_ACCESS_KEY_ID', 'your-aws-access-key-id'),
    'SES_SECRET_ACCESS_KEY': os.environ.get('SES_SECRET_ACCESS_KEY', 'your-aws-secret-access-key'),
    'SES_REGION_NAME': os.environ.get('SES_REGION_NAME', 'your-aws-region'),

    # Mailgun settings
    'MAILGUN_API_KEY': os.environ.get('MAILGUN_API_KEY', 'your-mailgun-api-key'),
    'MAILGUN_SENDER_DOMAIN': os.environ.get('MAILGUN_SENDER_DOMAIN', 'your-mailgun-domain.com'),
}

# Email Data
EMAIL_CONFIRMATION_SUBJECT = "PantherPay Email Confirmation"
PASSWORD_RESET_SUBJECT = "Reset Your Password"
CHANGE_PASSWORD_SUBJECT = "Change Your Password"
DEACTIVATING_CONFIRMATION_SUBJECT = "Deactivating Confirmation"


# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{os.environ.get('REDIS_HOST', 'redis')}:6379/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',

        }
    }
}

# Celery settings
CELERY_BROKER_URL = f"redis://{os.environ.get('REDIS_HOST', 'redis')}:6379/2"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'

# Example of using the cache
CACHE_TTL = 60 * 1  # Cache time-to-live in second

DOMAIN: str = os.environ.get('DOMAIN', '0.0.0.0:8000')
FRONTEND_URL: str = os.environ.get('FRONTEND_URL', '0.0.0.0:8000')
