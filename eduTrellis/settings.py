"""
Django settings for eduTrellis project (Django 5.2+ ready).
"""

from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
# --------------------
# BASE SETTINGS
# --------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = "django-insecure-h^l!e0kvn8ore3fikloht@x^6nlif_jbgg$=x=!0b(v-lu#ev_"

DEBUG = True

ALLOWED_HOSTS = ['*']

# --------------------
# APPLICATIONS
# --------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "base",
    "live_class",
    "elibrary",
    "testseries",
    "video_courses",
    "adminpanel",
]

# --------------------
# MIDDLEWARE
# --------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "eduTrellis.urls"

# --------------------
# TEMPLATES
# --------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Custom global templates folder
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # Custom context processors
                "adminpanel.context_processors.navbar_settings",
                "adminpanel.context_processors.footer_settings",
                "video_courses.context_processors.categories_context",
            ],
        },
    },
]

WSGI_APPLICATION = "eduTrellis.wsgi.application"

# --------------------
# DATABASE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --------------------
# PASSWORD VALIDATION
# --------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------
# INTERNATIONALIZATION
# --------------------
LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# --------------------
# STATIC & MEDIA FILES (Updated for Django 5.2+)
# --------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # Where collectstatic stores files

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------
# CUSTOM USER MODEL
# --------------------
AUTH_USER_MODEL = "base.User"


CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_SSL_REDIRECT = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "SAMEORIGIN"

# --------------------
# LOGIN / LOGOUT
# --------------------
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

# --------------------
# THIRD-PARTY INTEGRATIONS
# --------------------
RAZORPAY_KEY_ID = 'rzp_test_RaygzMDa8nwFFP'
RAZORPAY_KEY_SECRET = 'F1mtVXEvOvbyc6atPUAEwdZd'

JITSI_DOMAIN = "meet.ffmuc.net"

# --------------------
# DEFAULTS
# --------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Add this to ensure CSRF cookie is always set
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read the cookie
CSRF_USE_SESSIONS = False


# PWA Settings
PWA_APP_NAME = 'advance'
PWA_APP_DESCRIPTION = 'Premium online education platform'
PWA_APP_THEME_COLOR = '#c7212f'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait-primary'
PWA_APP_START_URL = '/'

# Static files for PWA icons (create these images)
PWA_APP_ICONS = [
    {
        'src': '/static/img/icon-192.png',
        'sizes': '192x192'
    },
    {
        'src': '/static/img/icon-512.png',
        'sizes': '512x512'
    }
]

# Security headers for PWA
SECURE_REFERRER_POLICY = 'same-origin'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CSRF_TRUSTED_ORIGINS = [
    "https://ganeshsirclasses.online",
    "https://www.ganeshsirclasses.online",
    "https://web-production-ab46.up.railway.app",
]

DROPBOX_ACCESS_TOKEN = "sl.u.AGUtqtaIJ_vVzeCIskNC1Ta7vmlCzEqKCmLcpPDiqrubkGVMcOawC21EkL7lz3b7FM4I4mwfgS7AyO3Lo7_jElYt-WFGSqiJK6aR7rmb6ztzZBA_I1Pr2niBEXkAGnvzhuzGZS8ENkrXs26G5zZELQlSQmRcDQnWAVb0NMGOo087xVpvupD7S15RNKx32La6XzfMXWYxsIfBBiNwTFUPcELa_oGgZpN5XwhDLYZseJWy3t7JqQlB9cB2gfw12xwiKbUEvGP1rKPdIoM0JmD_J_2qrAaWwevs_hSQIPwh2LjVSAMmOIA5Nu50g0G49LS7kyZGZ2ZP2McU7-b18NUi--XJ_jQGtoVzrijTS0vqy9rpR3UzhRQBNB9iADYmDBu-AuJqfVz-3Cp6Er5_MY17CXcIV9H2jThHd_ZZ6sWI2Acao75dyXZMnipsLGYYHr5mDhVh9vQIA2X-CwBYvAI8lLf9_J6z_qEyIBhC0Zl5O4cKSuxMwaSjxFQpQMzVf9FNnAQ6BqwB0W7ImKtXDmWuyUkdiKXoGtidWdaZcIerBh3BWU-CLJLcSJq97saWRHCkjq-tnOMMGUuk4JFZl08ZYja9BC-OFt5skzu8j-8UTuJsXRZsD4BtbVT7Pt_YEZ_gAPz1xteq7-_6PdJnaKhZQvXBLtn-cq1jH_OmCPSh_xeMd6Jlkc7t5yA34xpp-fCEZbRU9MmHYU9JottvDtKRuzTb6ibp9Cyni8-3oj82li4jZJyfUe3bVr3huKs5w0YBOJb64OdQZXvqrbyivoc6qsg2Ugf7tfo4CZoJOV_KSixNKDfYM1_5yaKAVJ0VxTtGtSU_MQTooyaAVihY8CJaNCG5RNxrWun_1ZypH1A7G65ypgtcjMq5KizNDtWVZkIimFmXqrpIMRePvNgUFi6yWPbcuUVGNXSX-DNfEGMdl-fkQamE9i0yrfpuDLv9qktwVn7Z9xomyMAr1uneRR-lgTVpQaSXaFIxzE_KS2gqc0bwsLlIrRXrTJeI_cCjWwQcXxpHGZ1UszIdvv_Hur_Zuborj3SWXc9PxMVBr-Hhp0KY-p3h8HCAIx9GEmV7Ts1UIzs7QWDPm4IRE6ff-Q9FDX-jXhJXLIxzQuSmJBTRTL93afsHZlYAA5jNUmNyb5panVYFAXx00N75oWZRSedS8NZeNDtp6AZkrreyeJcZnZtgSfuFTkVUFoV7F20dnZ8I5ZSUblulTO5qQO5AVDqf0brA_O4LOujoA4wbvUrEsl8fG9iL7P6eBI9gWSI4mcMLt4LKULZRWdxNkr9nWocpCtEy4ixKcGryZniFPuNfK2iwGnoZaLPk50pz_kjIrcHC5_23VBqccPjxEp30LriqkZFggRc-IhB3bi9lrvIg0-lgD2Eb0ReS_JpURWxpabN36BG3jqDT_vfGhCYgW_sPGZg817Ni-H-Ti3tTDkRaDZl7Pg"