from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class MuscleGroup(models.Model):
    name = models.TextField(unique=True)
