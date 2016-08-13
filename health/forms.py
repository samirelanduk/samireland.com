from django import forms
from health.models import MuscleGroup

class MuscleGroupForm(forms.models.ModelForm):

    class Meta:
        model = MuscleGroup
        fields = ("name",)

        widgets = {
         "name": forms.fields.TextInput()
        }
