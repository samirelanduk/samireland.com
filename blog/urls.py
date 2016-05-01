from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^new/$", views.new_post_page, name="new_post_page"),
    url(r"^edit/(\d+)/$", views.edit_post_page, name="edit_post_page"),
    url(r"^edit/$", views.edit_posts_page, name="edit_posts_page"),
    url(r"^delete/(\d+)/$", views.delete_post_page, name="delete_post_page"),
    url(r"^$", views.blog_page, name="blog_page")
]
