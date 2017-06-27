from django.conf.urls import url
from blog import views

urlpatterns = [
 url(r"^new/$", views.new_blog_page, name="new_blog_page"),
 url(r"^(\d+)/(\d+)/(\d+)/$", views.one_post_page, name="one_post_page"),
 url(r"^$", views.blog_page, name="blog_page"),
]
