from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^$", views.home_page, name="home_page"),
    url(r"^about/", views.about_page, name="about_page"),
    url(r"^blog/new/", views.new_post_page, name="new_post_page"),
    url(r"^blog/", views.blog_page, name="blog_page")
]
