import docupy
from django.db import models

def create_filename(instance, filename):
    extension = "." + filename.split(".")[-1] if "." in filename else ""
    try:
        name = instance.name
    except:
        name = instance.id
    kind = instance._meta.model.__name__.lower()
    return f"{kind}-{name.lower()}{extension}"


def get_image_lookup():
    return {
     **{article.image.name.split("/")[-1].split(".")[0]: article.image.url for article in Article.objects.all()}
    }




class Project(models.Model):

    class Meta:
        db_table = "projects"
        ordering = ["number"]
    
    def __str__(self):
        return self.name

    number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=64)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    image = models.FileField(null=True, blank=True, upload_to=create_filename)



class Publication(models.Model):

    class Meta:
        db_table = "publications"
        ordering = ["-date"]
        
    def __str__(self):
        return self.title 

    id = models.SlugField(primary_key=True)
    title = models.CharField(max_length=512)
    date = models.DateField()
    url = models.URLField()
    authors =  models.CharField(max_length=512)
    doi = models.CharField(max_length=128)
    abstract = models.TextField()
    body = models.TextField()
    image = models.FileField(upload_to=create_filename)
    pdf = models.FileField(upload_to=create_filename)



class Article(models.Model):

    class Meta:
        db_table = "articles"
        ordering = ["-date"]
        
    def __str__(self):
        return self.title 

    id = models.SlugField(primary_key=True)
    title = models.CharField(max_length=512)
    date = models.DateField()
    summary = models.TextField()
    body = models.TextField()
    image = models.FileField(upload_to=create_filename)

    def body_html(self):
        print(get_image_lookup())
        return docupy.markdown_to_html(self.body.replace("\r", ""), get_image_lookup())


