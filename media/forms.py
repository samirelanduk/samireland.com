from django import forms
from media.models import Image

EMPTY_FIELD_ERROR = "You cannot submit a blog post with no %s"



class MediaForm(forms.models.ModelForm):


    class Meta:
        model = Image
        fields = ("imagetitle", "imagefile")

        widgets = {
         "imagetitle": forms.fields.TextInput()
        }

        error_messages = {
         "imagetitle": {
          "required": "You cannot submit media with no title",
          "unique": "There is already media with this title"}
        }
