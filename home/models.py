import docupy
from django.db import models
from media.models import media_url_lookup

# Create your models here.
class EditableText(models.Model):

    name = models.CharField(max_length=30)
    content = models.TextField()

    @property
    def markdown(self):
        return docupy.markdown_to_html(self.content, media_url_lookup())



class Publication(models.Model):

    id = models.TextField(primary_key=True)
    title = models.TextField()
    date = models.DateField()
    url = models.TextField()
    doi = models.TextField()
    authors = models.TextField()
    abstract = models.TextField()
    body = models.TextField()
