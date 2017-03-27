from django.conf.urls import url
from piano import views

urlpatterns = [
 url(r"^$", views.piano_page, name="piano_page")
]
