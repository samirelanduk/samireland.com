"""URL redirects for samireland.com"""

from django.urls import path, include
from django.conf.urls.static import static
import samireland.views as views
from django.conf import settings

urlpatterns = [
 path(r"authenticate/", views.login),
 path(r"logout/", views.logout),
 path(r"edit/<slug:name>/", views.edit),
 path(r"research/", views.research),
 path(r"research/new/", views.new_pub),
 path(r"research/<slug:id>/", views.publication),
 path(r"research/<slug:id>/edit/", views.edit_pub),
 path(r"projects/", views.projects),
 path(r"projects/new/", views.new_project),
 path(r"projects/<int:id>/edit/", views.edit_project),
 path(r"writing/", views.writing),
 path(r"writing/new/", views.new_article),
 path(r"writing/<slug:id>/", views.article),
 path(r"writing/<slug:id>/edit/", views.edit_article),
 path(r"about/", views.about),
 path(r"media/", views.media),
 path(r"", views.home)
] + static(
 settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT
)
