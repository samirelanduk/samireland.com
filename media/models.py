from datetime import datetime
from django.db import models


# Create your models here.
def create_filename(instance, filename):
    extension = "." + filename.split(".")[-1] if "." in filename else ""
    return datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + extension


def media_url_lookup():
    return {
     media.mediatitle: "/" + media.mediafile.url
      for media in MediaFile.objects.all()
    }


class MediaFile(models.Model):

    mediatitle = models.TextField(unique=True)
    mediafile = models.FileField(upload_to=create_filename)
