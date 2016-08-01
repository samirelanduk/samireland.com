from django.conf.urls import url
from health import views

urlpatterns = [
    url(r"^edit/$", views.edit_page, name="edit_page"),
]
