import datetime
from django.db import models

def create_filename(instance, filename):
    extension = "." + filename.split(".")[-1] if "." in filename else ""
    return "images/" + datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d") + extension


# Create your models here.
class Image(models.Model):

    imagetitle = models.TextField(default="", unique=True)
    imagefile = models.FileField(upload_to=create_filename)
