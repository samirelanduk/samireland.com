from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(Publication)
admin.site.register(Article)
admin.site.register(Period)
admin.site.register(MediaFile)