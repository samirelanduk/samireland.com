from django import forms
from django.forms.extras.widgets import SelectDateWidget
from blog.models import BlogPost

EMPTY_FIELD_ERROR = "You cannot submit a blog post with no %s"


class DateInput(forms.DateInput):
    input_type = 'date'



class PlainTextarea(forms.Textarea):

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(PlainTextarea, self).build_attrs(extra_attrs, **kwargs)
        if "cols" in attrs: del attrs["cols"]
        if "rows" in attrs: del attrs["rows"]
        return attrs



class BlogPostForm(forms.models.ModelForm):


    class Meta:
        model = BlogPost
        fields = ("title", "date", "body", "visible")
        widgets = {
         "title": forms.fields.TextInput(attrs={
          "class": "pure-u-1-1 pure-u-md-19-24"
         }),
         "date": DateInput(),
         "body": PlainTextarea(attrs={
          "class": "pure-u-1-1 pure-u-md-19-24"
         }),
         "visible": forms.CheckboxInput(attrs={
          "class": "pure-u-1-24"
         })
        }
        error_messages = {
         "title": {"required": EMPTY_FIELD_ERROR % "title"},
         "date": {
          "required": EMPTY_FIELD_ERROR % "date",
          "unique": "There is already a blog post for this date"},
         "body": {"required": EMPTY_FIELD_ERROR % "body"}
        }
