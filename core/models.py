from django.db import models

def create_filename(instance, filename):
    extension = "." + filename.split(".")[-1] if "." in filename else ""
    return f"project-{instance.name.lower()}{extension}"


class Project(models.Model):

    class Meta:
        ordering = ["number"]
    
    def __str__(self):
        return self.name

    number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=64)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    image = models.FileField(null=True, blank=True, upload_to=create_filename)