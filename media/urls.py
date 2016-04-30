from django.conf.urls import url
from media import views

urlpatterns = [
    url(r"^upload/$", views.upload_media_page, name="upload_media_page"),
    url(r"^delete/(.+)/$", views.delete_media_page, name="delete_media_page"),
    url(r"^$", views.media_page, name="media_page")
]
