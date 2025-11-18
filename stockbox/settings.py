"""
Django settings for stockbox project.

Generado por 'django-admin startproject'.

Para más info:
https://docs.djangoproject.com/en/stable/topics/settings/
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
# En producción, la leerá de la variable de entorno SECRET_KEY
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key-no-usar-en-produccion"
)

# SECURITY WARNING: don't run with debug turned on in production!
# En Render pon DEBUG=False
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",  # cualquier subdominio de Render
]

# Si quieres ser más estricto en producción puedes hacer algo como:
# RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
# if RENDER_HOSTNAME:
#     ALLOWED_HOSTS.append(RENDER_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventario',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # para servir estáticos en Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stockbox.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # aquí puedes poner rutas extra de templates si las usas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stockbox.wsgi.application'


# Database
# En local usará sqlite, en Render usará DATABASE_URL (PostgreSQL)

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = 'en-us'  # si quieres español: 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # donde collectstatic juntará todo

# Si tienes una carpeta "static" en el proyecto:
# STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise: compresión y versionado de archivos estáticos
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
