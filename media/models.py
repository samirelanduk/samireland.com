from django.db import models

# Create your models here.
class Image(models.Model):

    imagetitle = models.TextField(default="", unique=True)
    imagefile = models.FileField(upload_to="images")
