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
