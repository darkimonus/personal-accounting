import os
from pathlib import Path

from django.urls import reverse_lazy
from oauth2_provider.settings import oauth2_settings

from custom_logging import config

BASE_DIR = Path(__file__).resolve().parent.parent
DJANGO_PROJECT_NAME = os.getenv("DJANGO_PROJECT_NAME")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = os.getenv("DEBUG", True)

ALLOWED_HOSTS = os.getenv("K8S_HOSTNAME", '*').split(",")

TOKEN_DURATION_SEC = os.getenv("TOKEN_DURATION_SEC")
TOKEN_DURATION_SEC = (
    int(TOKEN_DURATION_SEC) if TOKEN_DURATION_SEC is not None else 86_400
)
oauth2_settings.defaults["OIDC_RSA_PRIVATE_KEY"] = os.getenv('OIDC_RSA_PRIVATE_KEY')
OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "ACCESS_TOKEN_EXPIRE_SECONDS": TOKEN_DURATION_SEC,
    "OIDC_RSA_PRIVATE_KEY": os.getenv('OIDC_RSA_PRIVATE_KEY'),
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "users",
    "incomes",
    "expenses.AppConfig",
    "oauth2_provider",
    "rest_framework",
    'rest_framework.authtoken',
    "drf_yasg",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'personal_accounting.urls'

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

WSGI_APPLICATION = 'personal_accounting.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        "TEST": {
            "MIRROR": "default",
        },
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST_FRAMEWORK settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_THROTTLE_RATES": {"email_send": "3/minute"},
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        'rest_framework.authentication.TokenAuthentication',
    ],
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
FROM_EMAIL = os.getenv("FROM_EMAIL")

EMAIL_CODE_LENGTH = int(os.getenv("EMAIL_CODE_LENGTH", "6"))
EMAIL_SUBJECT = "Hello, {0}!"
EMAIL_BODY = "{0} {1}"

# Run Celery in sync mode (for local development)
CELERY_WORK_SYNC = os.getenv("CELERY_WORK_SYNC")
CELERY_ALWAYS_EAGER = CELERY_WORK_SYNC is not None
CELERY_TASK_ALWAYS_EAGER = CELERY_WORK_SYNC is not None

# login settings
LOGIN_URL = os.getenv('LOGIN_URL')
LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL")

ENABLE_OAUTH = os.getenv("ENABLE_OAUTH") == "True"
if ENABLE_OAUTH:
    INSTALLED_APPS += [
        "social_django",
        "drf_social_oauth2",
    ]
    SOCIAL_AUTH_REDIRECT_IS_HTTPS = os.getenv('SOCIAL_AUTH_REDIRECT_IS_HTTPS', False)
    MIDDLEWARE += [
        "oauth2_provider.middleware.OAuth2TokenMiddleware",
    ]
    context_processors_list = TEMPLATES[0].get("OPTIONS").get("context_processors")
    context_processors_list += [
        # OAuth
        "social_django.context_processors.backends",
        "social_django.context_processors.login_redirect",
    ]
    default_authentication_classes = REST_FRAMEWORK.get(
        "DEFAULT_AUTHENTICATION_CLASSES"
    )
    default_authentication_classes += [
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "drf_social_oauth2.authentication.SocialAuthentication",
    ]

    AUTHENTICATION_BACKENDS = [
        # Facebook OAuth2
        "social_core.backends.facebook.FacebookAppOAuth2",
        "social_core.backends.facebook.FacebookOAuth2",
        # Google OAuth2
        "social_core.backends.google.GoogleOAuth2",
        # for token auth in django admin
        "oauth2_provider.backends.OAuth2Backend",
        # drf-social-oauth2
        "drf_social_oauth2.backends.DjangoOAuth2",
        # Django
        "django.contrib.auth.backends.ModelBackend",
    ]
    # Token settings
    # convert our base token into jwt format [NOT NEEDED]
    ACTIVATE_JWT = os.getenv("ACTIVATE_JWT") == "True"  # 1 day
    oauth2_settings.defaults["ACCESS_TOKEN_EXPIRE_SECONDS"] = TOKEN_DURATION_SEC

ENABLE_GOOGLE_OAUTH = os.getenv("ENABLE_GOOGLE_OAUTH") == "True"
if ENABLE_GOOGLE_OAUTH:
    # Google configuration
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

    # Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE
    # to get extra permissions from Google.
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
    SOCIAL_AUTH_JSONFIELD_ENABLED = True
    SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/callback/'

ENABLE_CUSTOM_LOGGING = os.getenv("ENABLE_CUSTOM_LOGGING", "False")
if ENABLE_CUSTOM_LOGGING == "True":
    LOGGING = config.LOGGING
    LOGGING_DEBUG = os.getenv("LOGGING_DEBUG", "False")
    LOGGING_INFO = os.getenv("LOGGING_INFO", "True")
    LOGGING_ERROR = os.getenv("LOGGING_ERROR", "True")
    MIDDLEWARE += [
        "custom_logging.middleware.LoggingMiddleware",
    ]

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": True,
    "LOGIN_URL": reverse_lazy("admin:login"),
    "LOGOUT_URL": reverse_lazy("admin:logout"),
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_root/")  # noqa F405
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

REDIS_HOST = os.getenv("REDIS_HOST", 'accounting-cache')
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

if REDIS_PASSWORD is not None:
    REDIS_PATH = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2"
else:
    REDIS_PATH = f"redis://{REDIS_HOST}:{REDIS_PORT}/2"

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_DEFAULT_QUEUE = f'{DJANGO_PROJECT_NAME}_queue'
CELERY_BROKER_TRANSPORT_OPTIONS = {'queue_prefix': f'{DJANGO_PROJECT_NAME}_'}

CELERY_BROKER_URL = REDIS_PATH
CELERY_RESULT_BACKEND = REDIS_PATH
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_PATH,
    }
}

# Users app settings
AUTH_USER_MODEL = "users.User"
ENABLE_USER_VERIFICATION = os.getenv("ENABLE_USER_VERIFICATION") == "True"
