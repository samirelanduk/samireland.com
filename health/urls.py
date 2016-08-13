from django.conf.urls import url
from health import views

urlpatterns = [
    url(r"^edit/$", views.edit_page, name="edit_page"),
    url(r"^edit/musclegroup/(?P<name>[a-zA-Z]+)/$", views.musclegroup_page, name="musclegroup_page"),
]
