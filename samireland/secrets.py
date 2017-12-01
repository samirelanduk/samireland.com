# Secret settings for samireland.com

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "vw7xy2#m@r+_w!dl1_f74jq+(0ep_i=p!xu1-ucao+=#oky-^$"

DATABASES = {"default": {
 "ENGINE": "django.db.backends.sqlite3",
 "NAME": os.path.join(BASE_DIR, "db.sqlite3")
}}