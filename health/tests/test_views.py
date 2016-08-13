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


    def test_redirects_to_self_with_get_after_post(self):
        response = self.client.post("/health/edit/")
        self.assertRedirects(response, "/health/edit/")


    def test_edit_page_view_can_save_muscle_group(self):
        self.assertEqual(MuscleGroup.objects.count(), 0)
        self.client.post("/health/edit/", data={"name": "arm"})
        self.assertEqual(MuscleGroup.objects.count(), 1)
        self.assertEqual(MuscleGroup.objects.first().name, "arm")


    def test_edit_page_view_wont_save_incorrect_posts(self):
        self.assertEqual(MuscleGroup.objects.count(), 0)
        self.client.post("/health/edit/", data={"name": ""})
        self.assertEqual(MuscleGroup.objects.count(), 0)


    def test_edit_page_lists_muscle_groups(self):
        MuscleGroup.objects.create(name="thorax")
        MuscleGroup.objects.create(name="abdomen")
        MuscleGroup.objects.create(name="spine")
        response = self.client.get("/health/edit/")
        self.assertContains(response, "thorax")
        self.assertContains(response, "abdomen")
        self.assertContains(response, "spine")
        pos_abdomen = response.content.decode().find("abdomen")
        pos_spine = response.content.decode().find("spine")
        pos_thorax = response.content.decode().find("thorax")
        self.assertTrue(pos_abdomen < pos_spine < pos_thorax)



class MuscleGroupViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        MuscleGroup.objects.create(name="arms")
        MuscleGroup.objects.create(name="legs")
        MuscleGroup.objects.create(name="fingers")


    def test_musclegroup_view_uses_musclegroup_template(self):
        response = self.client.get("/health/edit/musclegroup/arms/")
        self.assertTemplateUsed(response, "musclegroup.html")


    def test_musclegroup_view_uses_correct_group(self):
        group = MuscleGroup.objects.get(name="legs")
        response = self.client.get("/health/edit/musclegroup/legs/")
        self.assertEqual(response.context["group"], group)


    def test_invalid_group_returns_404(self):
        response = self.client.get("/health/edit/musclegroup/toes/")
        self.assertEqual(response.status_code, 404)



class MuscleGroupDeletionViewTests(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        MuscleGroup.objects.create(name="arms")
        MuscleGroup.objects.create(name="legs")
        MuscleGroup.objects.create(name="fingers")


    def test_musclegroup_deleteion_view_uses_musclegroup_deletion_template(self):
        response = self.client.get("/health/edit/musclegroup/arms/delete/")
        self.assertTemplateUsed(response, "musclegroup_delete.html")


    def test_musclegroup_deleteion_view_uses_correct_group(self):
        group = MuscleGroup.objects.get(name="legs")
        response = self.client.get("/health/edit/musclegroup/legs/delete/")
        self.assertEqual(response.context["group"], group)


    def test_invalid_group_returns_404(self):
        response = self.client.get("/health/edit/musclegroup/toes/delete/")
        self.assertEqual(response.status_code, 404)
