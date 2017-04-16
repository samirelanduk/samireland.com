from django.db import models

# Create your models here.
class PracticeSession(models.Model):
    minutes = models.IntegerField()
    date = models.DateField(unique=True)

    @property
    def cumulative_minutes(self):
        all_previous = PracticeSession.objects.all().filter(date__lte=self.date)
        return sum([session.minutes for session in all_previous])
