import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from blog import views
from blog.models import BlogPost
from blog.forms import BlogPostForm

class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="person", password="secret")
        self.client.login(username="person", password="secret")



class HomePageViewTests(ViewTest):

    def test_edit_page_view_uses_edit_page_template(self):
        response = self.client.get("/health/edit/")
        self.assertTemplateUsed(response, "edit_health.html")
