"""URL redirects for samireland.com"""

from django.urls import path, include
import samireland.views as views

urlpatterns = [
 path(r"authenticate/", views.login),
 path(r"logout/", views.logout),
 path(r"edit/<slug:name>/", views.edit),
 path(r"research/", views.research),
 path(r"research/new/", views.new_pub),
 path(r"research/<slug:id>/", views.publication),
 path(r"research/<slug:id>/edit/", views.edit_pub),
 path(r"about/", views.about),
 path(r"media/", views.media),
 path(r"", views.home)
]
