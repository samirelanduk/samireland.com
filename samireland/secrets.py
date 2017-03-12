import os

db = "samireland"
user = "samireland"
password = "d9cTvKrJqM"
host = "localhost"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "33gd4v4n_$rz+8v6zwvtouq^*e%q0to!%k=-bb)q%uh^zc)_-f"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

local_db = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

live_db = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': db, 'USER': user, 'PASSWORD': password, 'HOST': host
}

DATABASES = {"default": local_db}
