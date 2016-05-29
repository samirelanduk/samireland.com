from django.conf.urls import url
from piano import views

urlpatterns = [
    url(r"^practice/$", views.practice_page, name="practice_page"),
    url(r"^update/$", views.update_page, name="update_page"),
    url(r"^$", views.piano_page, name="piano_page")
]
