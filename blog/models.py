from django.db import models

# Create your models here.
class BlogPost(models.Model):
    title = models.TextField()
    date = models.DateField(unique=True)
    body = models.TextField()
    visible = models.BooleanField()
