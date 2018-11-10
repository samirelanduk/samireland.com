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
 "django.contrib.messages",
 "django.contrib.admin",
 "sass_processor",
 "track",
 "samireland"
]

MIDDLEWARE = [
 "django.contrib.sessions.middleware.SessionMiddleware",
 "django.middleware.common.CommonMiddleware",
 "django.middleware.csrf.CsrfViewMiddleware",
 "django.contrib.auth.middleware.AuthenticationMiddleware",
 "django.contrib.messages.middleware.MessageMiddleware",
 "htmlmin.middleware.HtmlMinifyMiddleware",
 "htmlmin.middleware.MarkRequestMiddleware",
 "track.middleware.inspect_response",
]

STATIC_URL = "/static/" # URL root for static files
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../static"))
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_URL = "/uploads/"
SASS_PROCESSOR_ROOT = os.path.abspath(os.path.join(BASE_DIR, "samireland", "static"))

TEMPLATES = [{
 "BACKEND": "django.template.backends.django.DjangoTemplates",
 "APP_DIRS": True,
 "OPTIONS": {
  "context_processors": [
   "django.contrib.auth.context_processors.auth",
  ],
 },
}]

TRACK_TZ = "Europe/London"
TRACK_PATH_EXCLUDE = [r"\.ico$", r"\.txt$", r"^/admin"]
TRACK_HOST_EXCLUDE = ["samireland.uk", "www.samireland.uk"]
GEOIP_PATH = "/usr/local/bin/geolite2"
EXCLUDE_TAGS_FROM_MINIFYING = ["pre", "code"]
