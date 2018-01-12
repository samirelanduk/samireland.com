from django import forms
from .models import Publication

class DateInput(forms.DateInput):
    input_type = "date"



class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        exclude = []

        widgets = {
         "id": forms.TextInput(attrs={
          "placeholder": "ID", "autocomplete": "off"
         }),
         "title": forms.TextInput(attrs={
          "placeholder": "Title", "autocomplete": "off"
         }),
         "date": DateInput(),
         "url": forms.TextInput(attrs={
          "placeholder": "URL", "autocomplete": "off"
         }),
         "doi": forms.TextInput(attrs={
          "placeholder": "DOI", "autocomplete": "off"
         }),
         "authors": forms.TextInput(attrs={
          "placeholder": "Authors", "autocomplete": "off"
         }),
         "body": forms.Textarea(attrs={"placeholder": "Body"}),
        }
