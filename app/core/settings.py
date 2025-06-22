from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from decouple import config

# Django related
APP_TITLE = "iSi Test assigment"

SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", cast=bool, default=True)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="").split(",")
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="").split(",")

HOST = config("DJANGO_HOST", "http://127.0.0.1:8000")

BASE_DIR = Path(__file__).resolve().parent.parent

# Static and media files
STATIC_URL = "static/"
STATIC_ROOT = config("DJANGO_STATIC_ROOT", "/var/static/")

MEDIA_URL = "media/"
MEDIA_ROOT = config("DJANGO_MEDIA_ROOT", "/var/media/")

INSTALLED_APPS = [
    # Built in
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third parties
    "corsheaders",
    "rest_framework",
    "drf_yasg",
    # Project
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

PASSWORD_HASHING_ITERATIONS = config(
    "PASSWORD_HASHING_ITERATIONS", cast=int, default=870000
)
PASSWORD_HASHERS = [
    "common.password_hashers.variable_pbkdf2.VariablePBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Database related
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST", default="127.0.0.1"),
        "PORT": config("POSTGRES_PORT", cast=int, default=5432),
        "OPTIONS": {
            "pool": {
                "min_size": config(
                    "POSTGRES_POOL_MIN_SIZE", cast=int, default=4
                ),
                "max_size": config(
                    "POSTGRES_POOL_MAX_SIZE", cast=int, default=10
                ),
                "timeout": config(
                    "POSTGRES_POOL_TIMEOUT", cast=int, default=10
                ),
            }
        },
        "TEST": {
            "NAME": config("POSTGRES_TEST_DB"),
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS related
CORS_ALLOW_HEADERS = list(default_headers)
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="").split(",")

# REST framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "EXCEPTION_HANDLER": "common.handlers.detail_exception_handler",
}

# Swagger
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "USE_SESSION_AUTH": False,
    "DEFAULT_MODEL_RENDERING": "example",
    "DEEP_LINKING": True,
    "DEFAULT_MODEL_DEPTH": 0,
}

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        seconds=config("JWT_ACCESS_LIFETIME_SECONDS", cast=int, default=300)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        seconds=config(
            "JWT_REFRESH_LIFETIME_SECONDS", cast=int, default=2592000
        )
    ),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
