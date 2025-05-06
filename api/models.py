from django.db import models
from django.utils.timezone import now


# Create your models here.


class Anemometer(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),  # Composite index for spatial queries
        ]

class WindSpeedReading(models.Model):
    anemometer = models.ForeignKey(Anemometer, on_delete=models.CASCADE, related_name='readings', db_index=True)  # Explicit index
    speed_knots = models.FloatField()
    recorded_at = models.DateTimeField(default=now, db_index=True)

    class Meta:
        ordering = ['-recorded_at']

