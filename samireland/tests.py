from django.core.urlresolvers import resolve
from django.contrib.auth.models import User
from django.test import TestCase

class SamTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
         username="testsam",
         password="testpassword"
        )



class UrlTest(SamTest):

    def check_url_returns_view(self, url, view):
        resolver = resolve(url)
        self.assertEqual(resolver.func, view)



class ViewTest(SamTest):
    pass
