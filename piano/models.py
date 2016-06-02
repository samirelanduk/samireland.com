from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class PracticeSession(models.Model):
    minutes = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateField(unique=True)

    @property
    def formatted_date(self):
        return self.date.strftime("%Y-%m-%d")
