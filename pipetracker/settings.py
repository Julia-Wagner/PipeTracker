import os
from pathlib import Path

import dj_database_url
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES_DIR_ALLAUTH = os.path.join(BASE_DIR, 'templates', 'allauth')

# custom allauth forms
ACCOUNT_FORMS = {
    'login': 'home.forms.CustomLoginForm',
    'signup': 'home.forms.CustomSignupForm',
}

if os.path.isfile("env.py"):
    import env

# store secret key in environment file
SECRET_KEY = os.environ.get("SECRET_KEY")

# store debug decision in environment file
DEBUG = "DEVELOPMENT" in os.environ

ALLOWED_HOSTS = ['pipetracker.herokuapp.com',
                 'pipetracker-96d1f7c7a4dc.herokuapp.com',
                 'localhost',
                 '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_tables2',
    'django_extensions',

    # Apps
    'pipetracker',
    'home',
    'stock',
    'delivery',
    'basket',
]

# allauth
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USERNAME_MIN_LENGTH = 5
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# add custom classes to messages
MESSAGE_TAGS = {
    messages.DEBUG: "border-darkblue text-darkblue",
    messages.INFO: "border-darkblue text-darkblue",
    messages.SUCCESS: "border-success text-success",
    messages.WARNING: "border-warning text-warning",
    messages.ERROR: "border-danger text-danger",
}

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# add custom classes to crispy form inputs
CRISPY_CLASS_CONVERTERS = {
    'textinput': 'bg-gray-50 border border-darkblue text-gray-900 '
                 'text-sm rounded-lg focus:ring-blue-500 '
                 'focus:border-blue-500 block w-full p-2.5',
    'passwordinput': 'bg-gray-50 border border-darkblue text-gray-900 '
                 'text-sm rounded-lg focus:ring-blue-500 '
                 'focus:border-blue-500 block w-full p-2.5',
    'numberinput': 'bg-gray-50 border border-darkblue text-gray-900 '
                 'text-sm rounded-lg focus:ring-blue-500 '
                 'focus:border-blue-500 block w-full p-2.5',
    'select': 'bg-gray-50 border border-darkblue text-gray-900 '
                 'text-sm rounded-lg focus:ring-blue-500 '
                 'focus:border-blue-500 block w-full p-2.5',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'pipetracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
            TEMPLATES_DIR_ALLAUTH
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'pipetracker.wsgi.application'


DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL"))
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = \
    'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://www.wplogout.com/export-database-diagrams-erd-from-django/
GRAPH_MODELS = {
    'all_applications': True,
    'graph_models': True,
}
