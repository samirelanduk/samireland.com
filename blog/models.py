from django.db import models

# Create your models here.
class BlogPost(models.Model):

    date = models.DateField()
    title = models.TextField()
    body = models.TextField()
    visible = models.BooleanField()
