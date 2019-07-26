from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from core.views import *

urlpatterns = [
 path("about/", about),
 path("projects/", projects),
 path("writing/", writing),
 path("writing/<slug:id>/", article),
 path("admin/", admin.site.urls),
 path("", home)
] + static(
 settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT
)
