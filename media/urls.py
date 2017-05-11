from django.conf.urls import url
from media import views

urlpatterns = [
 url(r"^$", views.media_page, name="media_page")
]
