from django.conf.urls import url
from home import views

urlpatterns = [
 url(r"^authenticate/$", views.login_page, name="login_page"),
 url(r"^$", views.home_page, name="home_page")
]
