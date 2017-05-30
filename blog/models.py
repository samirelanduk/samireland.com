import samdown
from django.db import models

# Create your models here.
class BlogPost(models.Model):

    date = models.DateField()
    title = models.TextField()
    body = models.TextField()
    visible = models.BooleanField()

    @property
    def samdown_body(self):
        return samdown.html_from_markdown(self.body)
