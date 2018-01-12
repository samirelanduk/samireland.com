"""URL redirects for samireland.com"""

from django.urls import path
import samireland.views as views

urlpatterns = [
 path(r"authenticate/", views.login),
 path(r"logout/", views.logout),
 path(r"edit/<slug:name>/", views.edit),
 path(r"research/", views.research),
 path(r"research/new/", views.new_pub),
 path(r"about/", views.about),
 path(r"", views.home)
]
