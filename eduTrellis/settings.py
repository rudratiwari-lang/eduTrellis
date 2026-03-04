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

DROPBOX_ACCESS_TOKEN = "sl.u.AGXUMj-dHI6DnL58HHueOvv9S5k9l8gjJ9InGhmUXcif3GmxjLdfqxoakfLkAX7-aivD7EgSmCuierLywGzMgqFzjl2sfC_eSr6YCRWaLDSkqAV28wYHwL4w6Q38k5lCVz73Q45GJvrDJYqfPDhA579PeY6DElFDk2ey1JFPNujW0zUgo8lZ-iCMrSCxx_OYHBwkj1pXgquMLFOTwamATfB7z1R_fI3GYq4UkFJMDUy-cGWyECCATMH77d6vpljpPbIhnYfvykymgBs-6FEVrXfkq5c4yFvJMkdZUFr9YcUTrdGcBdwh0uWnK9zQ5DqXb4QGP9mGIVZJwV0Wriixc5PnvEuOtcEJRuWtV4fKpPXrEQEDKfa5bmtZeqSBsuU1d0lqF9ilKufc8Xo52O0ZJqdTX2jVKd_oPOsI31V5XxX3ESiRrgUt0lFai6q0G6rVKs9tN9yA6kMJTE2AH-ggbC6OJKQOKYKRmscsQXg-aSBiEO39ze30HlkUHIQBw4KpaOB5vOqtRksvUlAwR87ucMhRmAxXvEFxXZXrFGzsupqxi-zb9ekoH6c9KMO6fCB06JyPKdBrW9Og7LL3ucgjfjIUJOMyfREQFf8rRsBsIwVl4x7LixrcCQXC8RfbIUg-QmZ65I6jEJITp6UVO5JlHJUegtp1ZVnG_fy_13Dj9xnjAFclUF8rIxMfr4gZQRcHQc_IVfhBhlNrQ_vsEzU3_c85rr0iEIMk_UbxjwTGt4bcwpWRZPWuzTuEwr0KYqJ8FYjVyHo6-Wlyyu2RPJnNo2xq_B-KJ6uunAW1Sgj9TAGZir_rxJshkcJKD5q5Ue_rNmPLAhyLUEfnAdi8Q-divX38MaWVdKwCI9pW8Z7jtOIuhAVB-7RSUU_vsfjKhKEwopjf6SGX4iW6DHp9Y1uoo_BCw49x4HUBDGvNo4izTzYa6pO9CrPa_oYTRF1obazfFRast0sCuWdztqvWOwjp2x8CwrYL4x7Wd6RIjzOrdKrub2Eb4MpjBi_QVtTPbhNpr9iGZxgbqhZ_XWoYECr85A6r16oQUleszJdVcQbBl1fdB66XTaPFeV5vQEgLI7MQfSQ502r724zq35mqS3cFU2RT4WZ2abad57TnrYrmFGxvJbLvTR9fPzjkqK8BEK-C7JkslTCDNnrJD2rovc8E1fB158gFAjSILVNpvdtPP2CqLQ9Mbf4crsTqqNVqB06MMEIWKwEk41-rLYFZZgUUiA90RzZ_-G6I6UCWHRZmgXS-eXihVQUK7aaJYJuPXlLPW59_fSx_m4jgmenMbTYkIC9eazOO6idBGL__zLjKqT8ImipIkG_EHGJqggVrzagP4UEm5phP0fFTV7bi0SUlpWZ-KUTqV87EseSIs2-7rA_hzNyFqSZ8uAI67Mrm0psRlrDwFSbeGlzXhZiPX_rfBDdy9c_v_yBuZKYU2e_ncGSE2A"