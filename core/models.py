import docupy
from collections import Counter
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
    technologies = models.CharField(max_length=256, default="", blank=True)
    github = models.URLField(blank=True, null=True)
    image = models.FileField(null=True, blank=True, upload_to=create_filename)

    @staticmethod
    def all_tech():
        tech = []
        for project in Project.objects.all():
            for pro_tech in project.tech_list():
                tech.append(pro_tech)
        return [tech[0] for tech in Counter(tech).most_common()]


    def intro(self):
        return docupy.markdown_to_html(self.description.splitlines()[0])
    

    def body(self):
        return docupy.markdown_to_html("\n".join(self.description.splitlines()[1:]))


    def tech_list(self):
        return [tech for tech in self.technologies.split(",") if tech.strip()]



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
        return docupy.markdown_to_html(self.body.replace("\r", ""), get_image_lookup())



class Period(models.Model):

    class Meta:
        db_table = "periods"
        ordering = ["-number"]
        
    def __str__(self):
        return self.name 

    number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=64)
    time = models.CharField(max_length=64)
    description = models.TextField()
    image = models.FileField(null=True, blank=True, upload_to=create_filename)

    def description_html(self):
        return docupy.markdown_to_html(self.description.replace("\r", ""), get_image_lookup())