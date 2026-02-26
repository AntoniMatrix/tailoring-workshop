"""
Global Django settings.

Goals:
- Clean project structure (GitHub-ready)
- Security hardening for production
- SEO defaults injected via context processor
- MySQL database
"""

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ----------------------------
# Core
# ----------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = True

ALLOWED_HOSTS = [
    "seridoozi-workshop.ir", "www.seridoozi-workshop.ir", "127.0.0.1", "localhost"
]

# ----------------------------
# Apps
# ----------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    # Third-party
    "csp",

    # Local
    "core",
    "accounts",
    "orders",
    "adminpanel",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Whitenoise serves static files in production without extra setup
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    # CSRF protection
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Content Security Policy (CSP) - mitigates XSS
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "workshop_tailoring.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # SEO defaults available in all templates
                "core.context_processors.seo_defaults",
            ],
        },
    }
]

WSGI_APPLICATION = "workshop_tailoring.wsgi.application"
ASGI_APPLICATION = "workshop_tailoring.asgi.application"

# ----------------------------
# Database (MySQL)
# ----------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "workshop_db"),
        "USER": os.getenv("DB_USER", "workshop_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "workshop_pass"),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

# ----------------------------
# Auth
# ----------------------------
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----------------------------
# I18N
# ----------------------------
LANGUAGE_CODE = "fa"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# ----------------------------
# Static/Media
# ----------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Use compressed manifest storage for better caching in production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ----------------------------
# Security (Production-ready defaults)
# ----------------------------
# NOTE: Some settings depend on HTTPS. Enable them when deploying with TLS.
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "0") == "1"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # must be readable by JS if you use Fetch with CSRF cookie
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
# SSL

#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

# Only set secure cookies when HTTPS is enabled
SESSION_COOKIE_SECURE = not DEBUG and SECURE_SSL_REDIRECT
CSRF_COOKIE_SECURE = not DEBUG and SECURE_SSL_REDIRECT

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# HSTS should be enabled only when you are 100% on HTTPS
SECURE_HSTS_SECONDS = 31536000 if (not DEBUG and SECURE_SSL_REDIRECT) else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG and SECURE_SSL_REDIRECT
SECURE_HSTS_PRELOAD = not DEBUG and SECURE_SSL_REDIRECT

# If behind a reverse proxy that sets X-Forwarded-Proto:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ----------------------------
# CSP (Content Security Policy)
# ----------------------------
# Keep CSP strict; allow only self. If you add external scripts/fonts, whitelist them explicitly.
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": ("'self'",),
        "style-src": ("'self'", "'unsafe-inline'"),
        "img-src": ("'self'", "data:"),
        "font-src": ("'self'",),
        "connect-src": ("'self'",),
        "frame-ancestors": ("'none'",),
    }
}

# ----------------------------
# SEO / Site config (editable)
# ----------------------------
SITE_NAME = os.getenv("SITE_NAME", "کارگاه سری‌دوزی")
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000").rstrip("/")
SITE_DEFAULT_DESCRIPTION = os.getenv(
    "SITE_DEFAULT_DESCRIPTION",
    "ثبت سفارش سری‌دوزی، دریافت پیش‌فاکتور، پیگیری تولید و مدیریت سفارش‌های کارگاه."
)
SITE_DEFAULT_OG_IMAGE = os.getenv("SITE_DEFAULT_OG_IMAGE", "/static/img/og-default.jpg")

BUSINESS = {
    "name": SITE_NAME,
    "type": "LocalBusiness",
    "telephone": os.getenv("BUSINESS_PHONE", ""),
    "email": os.getenv("BUSINESS_EMAIL", ""),
    "address": {
        "streetAddress": os.getenv("BUSINESS_STREET", ""),
        "addressLocality": os.getenv("BUSINESS_CITY", ""),
        "addressRegion": os.getenv("BUSINESS_REGION", ""),
        "postalCode": os.getenv("BUSINESS_POSTAL", ""),
        "addressCountry": os.getenv("BUSINESS_COUNTRY", "IR"),
    },
    "sameAs": [],
}

# ----------------------------
# Logging (basic but useful)
# ----------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}