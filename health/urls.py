from django.conf.urls import url
from health import views

urlpatterns = [
    url(r"^edit/$", views.edit_page, name="edit_page"),
    url(r"^edit/musclegroup/(?P<name>(.+)+)/delete/$", views.musclegroup_delete_page, name="musclegroup_delete_page"),
    url(r"^edit/musclegroup/(?P<name>(.+)+)/$", views.musclegroup_page, name="musclegroup_page"),
]
