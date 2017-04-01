from django.conf.urls import url
from piano import views

urlpatterns = [
 url(r"^update/", views.piano_update_page, name="piano_update_page"),
 url(r"^delete/(\d+)/", views.piano_delete_page, name="piano_delete_page"),
 url(r"^$", views.piano_page, name="piano_page")
]
