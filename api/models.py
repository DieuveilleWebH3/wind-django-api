from django.db import models
from django.utils.timezone import now


# Create your models here.


class Anemometer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class WindSpeedReading(models.Model):
    anemometer = models.ForeignKey(Anemometer, on_delete=models.CASCADE, related_name='readings')
    speed_knots = models.FloatField()
    recorded_at = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-recorded_at']

