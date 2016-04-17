from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^$", views.home_page, name="home_page"),
    url(r"^about/", views.about_page, name="about_page")
]
