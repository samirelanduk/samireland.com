import samdown
from django.db import models

# Create your models here.
class EditableText(models.Model):

    name = models.CharField(max_length=30)
    content = models.TextField()

    @property
    def samdown_content(self):
        return samdown.html_from_markdown(self.content)
