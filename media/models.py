from datetime import datetime
from django.db import models


# Create your models here.
def create_filename(instance, filename):
    extension = "." + filename.split(".")[-1] if "." in filename else ""
    return datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + extension


class MediaFile(models.Model):

    mediatitle = models.TextField(default="", unique=True)
    mediafile = models.FileField(upload_to=create_filename)
