# Settings for samireland.com

from .secrets import SECRET_KEY, BASE_DIR, DATABASES

ALLOWED_HOSTS = True

ROOT_URLCONF = "samireland.urls"

INSTALLED_APPS = [
 "django.contrib.contenttypes",
 "django.contrib.staticfiles",
 "samireland"
]
