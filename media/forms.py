from django import forms
from media.models import MediaFile

EMPTY_FIELD_ERROR = "You cannot submit a blog post with no %s"



class MediaForm(forms.models.ModelForm):


    class Meta:
        model = MediaFile
        fields = ("mediatitle", "mediafile")

        widgets = {
         "mediatitle": forms.fields.TextInput(attrs={
          "class": "pure-u-1-1 pure-u-md-15-24"
         }),
         "mediafile": forms.widgets.FileInput(attrs={
          "class": "pure-u-1-1 pure-u-md-15-24"
         })
        }

        error_messages = {
         "mediatitle": {
          "required": "You cannot submit media with no title",
          "unique": "There is already media with this title"}
        }
