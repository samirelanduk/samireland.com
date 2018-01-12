"""Views for samireland.com"""

import docupy
from django.db import models

class EditableText(models.Model):

    name = models.CharField(primary_key=True, max_length=64)
    body = models.TextField()

    @property
    def html(self):
        return docupy.markdown_to_html(self.body)



class Publication(models.Model):

    id = models.SlugField(primary_key=True)
    title = models.TextField()
    date = models.DateField()
    url = models.TextField()
    doi = models.TextField()
    authors = models.TextField()
    body = models.TextField()

    @property
    def html(self):
        return docupy.markdown_to_html(self.body)


    @property
    def html_authors(self):
        return docupy.markdown_to_html(self.authors)
