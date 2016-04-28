from django import forms
from django.forms.extras.widgets import SelectDateWidget

class DateInput(forms.DateInput):
    input_type = 'date'



class PlainTextarea(forms.Textarea):

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(PlainTextarea, self).build_attrs(extra_attrs, **kwargs)
        if "cols" in attrs: del attrs["cols"]
        if "rows" in attrs: del attrs["rows"]
        return attrs



class BlogPostForm(forms.Form):

    title = forms.CharField()
    date = forms.DateField(widget=DateInput)
    body = forms.CharField(widget=PlainTextarea)
    visible = forms.BooleanField()
