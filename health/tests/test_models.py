import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from health.models import MuscleGroup

class ModelCreationTest(TestCase):

    def test_save_and_retrieve_muscle_groups(self):
        self.assertEqual(MuscleGroup.objects.all().count(), 0)
        group = MuscleGroup()
        group.name = "Arm"
        group.save()
        self.assertEqual(MuscleGroup.objects.all().count(), 1)

        retrieved_group = MuscleGroup.objects.first()
        self.assertEqual(retrieved_group, group)



class ModelValidationTest(TestCase):

    def test_cannot_create_group_without_name(self):
        group = MuscleGroup()
        group.save()
        with self.assertRaises(ValidationError):
            group.full_clean()


    def test_cannot_create_two_groups_with_same_name(self):
        MuscleGroup.objects.create(name="arm")
        with self.assertRaises(ValidationError):
            group = MuscleGroup(name="arm")
            group.full_clean()
