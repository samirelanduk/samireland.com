from django.db import models
from samdown import process_samdown

# Create your models here.
class BlogPost(models.Model):
    title = models.TextField()
    date = models.DateField(unique=True)
    body = models.TextField()
    visible = models.BooleanField()

    @property
    def formatted_body(self):
        return process_samdown(self.body)
