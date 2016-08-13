import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from health import views
from health.models import MuscleGroup
from health.forms import MuscleGroupForm

class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="person", password="secret")
        self.client.login(username="person", password="secret")



class EditPageViewTests(ViewTest):

    def test_edit_page_view_uses_edit_page_template(self):
        response = self.client.get("/health/edit/")
        self.assertTemplateUsed(response, "edit_health.html")


    def test_edit_page_view_uses_muscle_group_form(self):
        response = self.client.get("/health/edit/")
        self.assertIsInstance(response.context["group_form"], MuscleGroupForm)
