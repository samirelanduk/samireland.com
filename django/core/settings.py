import os
import environ

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(PROJECT_DIR)

env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, "12345"),
    STATIC_ROOT=(str, os.path.join(BASE_DIR, "static")),
    MEDIA_ROOT=(str, os.path.join(BASE_DIR, "media")),
    DB_URL=(str, "sqlite:///db.sqlite3"),
    WAGTAILADMIN_BASE_URL=(str, "admin"),
    FRONTEND_URL=(str, "http://localhost"),
)

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    env("FRONTEND_URL")
]

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

ROOT_URLCONF = "core.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TIME_ZONE = "UTC"

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wagtail.contrib.forms",
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
    "corsheaders",
    "core",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware"
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
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

STATIC_URL = "/admin/static/"

STATIC_ROOT = env("STATIC_ROOT")

MEDIA_ROOT = env("MEDIA_ROOT")

MEDIA_URL = "/media/"

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

WAGTAIL_SITE_NAME = "samireland.com"

DATABASES = {
    "default": env.db("DB_URL")
}

WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL")

FRONTEND_URL = env("FRONTEND_URL")