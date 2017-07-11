from django.conf.urls import url
from blog import views

urlpatterns = [
 url(r"^new/$", views.new_blog_page, name="new_blog_page"),
 url(r"^(\d+)/(\d+)/(\d+)/$", views.one_post_page, name="one_post_page"),
 url(r"^(\d+)/(\d+)/(\d+)/edit/$", views.edit_post_page, name="edit_post_page"),
 url(r"^(\d+)/(\d+)/(\d+)/delete/$", views.delete_post_page, name="delete_post_page"),
 url(r"^(\d+)/$", views.year_page, name="year_page"),
 url(r"^$", views.blog_page, name="blog_page"),
]
