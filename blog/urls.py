from django.conf.urls import url
from blog import views

urlpatterns = [
 url(r"^new/$", views.new_blog_page, name="new_blog_page"),
]
