"""Views for samireland.com"""

import docupy
from django.db import models

class EditableText(models.Model):

    name = models.CharField(primary_key=True, max_length=64)
    body = models.TextField()

    @property
    def html(self):
        return docupy.markdown_to_html(self.body)
