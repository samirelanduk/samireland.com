from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from core.views import *

urlpatterns = [
 path("writing/<slug:id>/", article),
 path("admin/", admin.site.urls),
 path("", home)
] + static(
 settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT
)
