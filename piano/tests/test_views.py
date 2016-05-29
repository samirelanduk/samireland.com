import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from piano import views

class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="person", password="secret")
        self.client.login(username="person", password="secret")



class PianoPageViewTests(ViewTest):

    def test_piano_page_view_uses_piano_page_template(self):
        response = self.client.get("/piano/")
        self.assertTemplateUsed(response, "piano.html")



class PracticePageViewTests(ViewTest):

    def test_piano_practice_page_view_uses_piano_practice_page_template(self):
        response = self.client.get("/piano/practice/")
        self.assertTemplateUsed(response, "pianopractice.html")



class UpdatePageViewTests(ViewTest):

    def test_piano_update_page_view_uses_piano_update_page_template(self):
        response = self.client.get("/piano/update/")
        self.assertTemplateUsed(response, "pianoupdate.html")
