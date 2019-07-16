import os
from .secrets import SECRET_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = []
DEBUG = True

ROOT_URLCONF = "core.urls"

INSTALLED_APPS = [
 "django.contrib.staticfiles",
 "sass_processor",
 "core",
]

TEMPLATES = [{
 "BACKEND": "django.template.backends.django.DjangoTemplates",
 "APP_DIRS": True,
}]

MIDDLEWARE = [
 "htmlmin.middleware.HtmlMinifyMiddleware",
 "htmlmin.middleware.MarkRequestMiddleware"
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.abspath(f"{BASE_DIR}/../static")
SASS_PROCESSOR_ROOT = os.path.abspath(os.path.join(BASE_DIR, "core", "static"))

HTML_MINIFY = True