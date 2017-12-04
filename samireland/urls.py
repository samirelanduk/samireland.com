"""URL redirects for samireland.com"""

from django.conf.urls import url
import samireland.views as views

urlpatterns = [
 url(r"^authenticate/$", views.login),
 url(r"^logout/$", views.logout),
 url(r"^$", views.home)
]
