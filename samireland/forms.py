from django import forms
from .models import Publication

class DateInput(forms.DateInput):
    input_type = "date"



class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        exclude = []

        widgets = {
            "id": forms.TextInput(attrs={"placeholder": "ID"}),
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "date": DateInput(),
            "url": forms.TextInput(attrs={"placeholder": "URL"}),
            "doi": forms.TextInput(attrs={"placeholder": "DOI"}),
            "authors": forms.TextInput(attrs={"placeholder": "Authors"}),
            "body": forms.Textarea(attrs={"placeholder": "Body"}),
        }
