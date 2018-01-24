# Settings for samireland.com

import os
from .secrets import SECRET_KEY, BASE_DIR, DATABASES

ALLOWED_HOSTS = []

DEBUG = True

ROOT_URLCONF = "samireland.urls"

INSTALLED_APPS = [
 "django.contrib.contenttypes",
 "django.contrib.staticfiles",
 "django.contrib.auth",
 "django.contrib.sessions",
 "samireland"
]

MIDDLEWARE = [
 "django.contrib.sessions.middleware.SessionMiddleware",
 "django.middleware.common.CommonMiddleware",
 "django.middleware.csrf.CsrfViewMiddleware",
 "django.contrib.auth.middleware.AuthenticationMiddleware",
]

STATIC_URL = "/static/" # URL root for static files
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../static"))
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_URL = "uploads/"

TEMPLATES = [{
 "BACKEND": "django.template.backends.django.DjangoTemplates",
 "APP_DIRS": True,
 "OPTIONS": {
  "context_processors": [
   "django.contrib.auth.context_processors.auth",
  ],
 },
}]
