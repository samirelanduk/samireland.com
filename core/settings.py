import os

DEBUG = True

if DEBUG:
    from .secrets import SECRET_KEY, DB_PASSWORD
else:
    SECRET_KEY = os.environ["SECRETKEY"]
    DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "core.urls"

if DEBUG:
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3")
    }}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": DB_PASSWORD,
            "HOST": "db",
            "PORT": 5432,
        }
    }

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
 "django.middleware.common.CommonMiddleware",
 "django.contrib.sessions.middleware.SessionMiddleware",
 "django.contrib.auth.middleware.AuthenticationMiddleware",
 "django.contrib.messages.middleware.MessageMiddleware",
 "django_user_agents.middleware.UserAgentMiddleware",
 "htmlmin.middleware.HtmlMinifyMiddleware",
 "htmlmin.middleware.MarkRequestMiddleware"
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/uploads/"
SASS_PROCESSOR_ROOT = os.path.abspath(os.path.join(BASE_DIR, "core", "static"))

HTML_MINIFY = True