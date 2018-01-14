"""URL redirects for samireland.com"""

from django.urls import path
import media.views as views

urlpatterns = [
 path(r"", views.media)
]
