from django.conf.urls import url
from media import views

urlpatterns = [
 url(r"^delete/(.+)/", views.media_delete_page, name="media_delete_page"),
 url(r"^$", views.media_page, name="media_page")
]
