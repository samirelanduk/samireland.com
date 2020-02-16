import os
from .secrets import SECRET_KEY, BASE_DIR, DATABASES


ALLOWED_HOSTS = ["localhost", "192.168.0.12"]
DEBUG = True

ROOT_URLCONF = "core.urls"

INSTALLED_APPS = [
 "django.contrib.contenttypes",
 "django.contrib.staticfiles",
 "django.contrib.sessions",
 "django.contrib.auth",
 "django.contrib.messages",
 "django.contrib.admin",
 "django_user_agents",
 "sass_processor",
 "core",
]

TEMPLATES = [{
 "BACKEND": "django.template.backends.django.DjangoTemplates",
 "APP_DIRS": True,
 "OPTIONS": {
  "context_processors": [
   "django.template.context_processors.request",
   "django.contrib.auth.context_processors.auth",
   "django.contrib.messages.context_processors.messages"
  ],
 },
}]

MIDDLEWARE = [
 "django.middleware.csrf.CsrfViewMiddleware",
 "django.contrib.sessions.middleware.SessionMiddleware",
 "django.contrib.auth.middleware.AuthenticationMiddleware",
 "django.contrib.messages.middleware.MessageMiddleware",
 "django_user_agents.middleware.UserAgentMiddleware",
 "htmlmin.middleware.HtmlMinifyMiddleware",
 "htmlmin.middleware.MarkRequestMiddleware"
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.abspath(f"{BASE_DIR}/../static")
if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
else:
     MEDIA_ROOT = os.path.join(BASE_DIR, "..", "uploads")
MEDIA_URL = "/uploads/"
SASS_PROCESSOR_ROOT = os.path.abspath(os.path.join(BASE_DIR, "core", "static"))

HTML_MINIFY = True