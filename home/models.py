from django.db import models

# Create your models here.
class EditableText(models.Model):

    name = models.CharField(max_length=30)
    content = models.TextField()
