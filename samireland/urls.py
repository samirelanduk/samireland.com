"""samireland URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from blog import urls as blog_urls
from piano import urls as piano_urls
from health import urls as health_urls
from media import urls as media_urls
from account import urls as account_urls
from blog.views import about_page, home_page

urlpatterns = [
    url(r'^blog/', include(blog_urls)),
    url(r'^piano/', include(piano_urls)),
    url(r'^health/', include(health_urls)),
    url(r'^media/', include(media_urls)),
    url(r'^account/', include(account_urls)),
    url(r'^about/$', about_page, name="about_page"),
    url(r'^$', home_page, name="home_page")
] + static(
 settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT
)
