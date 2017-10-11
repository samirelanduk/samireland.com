import docupy
from django.db import models
from media.models import media_url_lookup

# Create your models here.
class BlogPost(models.Model):

    date = models.DateField(unique=True)
    title = models.TextField()
    body = models.TextField()
    visible = models.BooleanField()

    @property
    def markdown(self):
        return docupy.markdown_to_html(self.body, media_url_lookup())
