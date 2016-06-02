from django import forms
from django.forms.extras.widgets import SelectDateWidget
from piano.models import PracticeSession

EMPTY_FIELD_ERROR = "You cannot submit a session with no %s"


class DateInput(forms.DateInput):
    input_type = 'date'



class PracticeSessionForm(forms.models.ModelForm):


    class Meta:
        model = PracticeSession
        fields = ("date", "minutes")
        widgets = {
         "date": DateInput(),
         "minutes": forms.fields.TextInput(attrs={
          "placeholder": "Minutes",
          "autocomplete": "off"
         })
        }
        error_messages = {
         "minutes": {
          "required": EMPTY_FIELD_ERROR % "minutes",
          "min_value": EMPTY_FIELD_ERROR % "minutes"
         },
         "date": {
          "required": EMPTY_FIELD_ERROR % "date",
          "unique": "There is already a session for this date"
         }
        }
