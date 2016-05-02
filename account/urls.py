from django.conf.urls import url
from account import views

urlpatterns = [
    url(r"^login/$", views.login_page, name="login_page"),
    url(r"^logout/$", views.logout_page, name="logout_page")
]
