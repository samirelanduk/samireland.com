from django.db import models

# Create your models here.
class PracticeSession(models.Model):
    minutes = models.IntegerField()
    date = models.DateField(unique=True)
