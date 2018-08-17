"""URL redirects for samireland.com"""

from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
import samireland.views as views
from django.conf import settings

urlpatterns = [

 path(r"research/", views.research),
 path(r"research/<slug:id>/", views.publication),
 path(r"projects/", views.projects),
 path(r"writing/", views.writing),
 path(r"writing/<slug:id>/", views.article),
 path(r"blog/", views.blog),
 path(r"blog/<int:year>/<int:month>/<int:day>/", views.blog_post),
 path(r"about/", views.about),
 path(r"media/", views.media),
 path(r"admin/", admin.site.urls),
 path(r"", views.home)
] + static(
 settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT
)
