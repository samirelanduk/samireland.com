"""Views for samireland.com"""

import docupy
from datetime import datetime
from django.db import models

class EditableText(models.Model):

    name = models.CharField(primary_key=True, max_length=64)
    body = models.TextField()

    def __str__(self):
        return "EditableText ({})".format(self.name)


    @property
    def html(self):
        return docupy.markdown_to_html(self.body.replace("\r", ""), MediaFile.media_lookup())



class Publication(models.Model):

    id = models.SlugField(primary_key=True)
    title = models.TextField()
    date = models.DateField()
    url = models.TextField()
    doi = models.TextField()
    authors = models.TextField()
    body = models.TextField()

    @property
    def html(self):
        return docupy.markdown_to_html(self.body.replace("\r", ""), MediaFile.media_lookup())


    @property
    def html_authors(self):
        return docupy.markdown_to_html(self.authors)


    def __str__(self):
        return "Publication ({})".format(self.title)



class Project(models.Model):

    CATEGORIES = [
     ["web", "web"], ["python", "python"], ["other", "other"],
    ]

    name = models.CharField(max_length=128)
    image = models.CharField(max_length=128)
    description = models.TextField()
    category = models.CharField(max_length=64, choices=CATEGORIES, default="web")

    @property
    def image_url(self):
        try:
            image = MediaFile.objects.get(name=self.image)
            return image.mediafile.url
        except MediaFile.DoesNotExist:
            return ""


    @property
    def html(self):
        return docupy.markdown_to_html(self.description.replace("\r", ""), MediaFile.media_lookup())


    def __str__(self):
        return "{} Project ({})".format(self.category.title(), self.name)



class Article(models.Model):

    id = models.SlugField(primary_key=True)
    title = models.TextField()
    date = models.DateField()
    summary = models.TextField()
    body = models.TextField()

    def __str__(self):
        return "Article ({})".format(self.title)


    @property
    def html(self):
        return docupy.markdown_to_html(self.body.replace("\r", ""), MediaFile.media_lookup())



class BlogPost(models.Model):

    date = models.DateField(primary_key=True)
    title = models.TextField()
    body = models.TextField()

    def __str__(self):
        return "BlogPost ({} - {})".format(self.date, self.title)


    @property
    def html(self):
        return docupy.markdown_to_html(self.body.replace("\r", ""), MediaFile.media_lookup())


    @property
    def next(self):
        return BlogPost.objects.filter(date__gt=self.date).order_by("date").first() or None


    @property
    def previous(self):
        return BlogPost.objects.filter(date__lt=self.date).order_by("-date").first() or None


class MediaFile(models.Model):

    def create_filename(instance, filename):
        extension = "." + filename.split(".")[-1] if "." in filename else ""
        return datetime.strftime(datetime.now(), "%Y%m%d-%H%M%S") + extension


    def media_lookup():
        return {
         media.name: media.mediafile.url for media in MediaFile.objects.all()
        }


    name = models.TextField(primary_key=True)
    mediafile = models.FileField(upload_to=create_filename)

    def __str__(self):
        return "MediaFile ({})".format(self.name)
