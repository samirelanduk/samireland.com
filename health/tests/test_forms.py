from django.test import TestCase
from health.forms import MuscleGroupForm
from health.models import MuscleGroup

class FormsRenderingTest(TestCase):

    def test_muscle_group_form_has_correct_inputs(self):
        form = MuscleGroupForm()
        self.assertIn(
         'name="name" type="text"',
         str(form)
        )



class FormsValidationTest(TestCase):

    def test_muscle_group_form_wont_accept_blank_name(self):
        form = MuscleGroupForm(data={"name":""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["name"],
         ["You cannot submit a muscle group with no name"]
        )


    def test_muscle_group_form_wont_accept_blank_name(self):
        MuscleGroup.objects.create(name="arm")
        form = MuscleGroupForm(data={"name":"arm"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
         form.errors["name"],
         ["There is already a muscle group with this name"]
        )
