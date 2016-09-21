from django import forms
from health.models import MuscleGroup

class MuscleGroupForm(forms.models.ModelForm):

    class Meta:
        model = MuscleGroup
        fields = ("name",)

        widgets = {
         "name": forms.fields.TextInput()
        }

        error_messages = {
         "name": {
          "required": "You cannot submit a muscle group with no name",
          "unique": "There is already a muscle group with this name"
         }
        }
