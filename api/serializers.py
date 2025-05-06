from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.utils.timezone import now, timedelta
from django.db.models import Avg
from .models import Anemometer, WindSpeedReading

class WindSpeedReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindSpeedReading
        fields = '__all__'


class AnemometerSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False, help_text="List of tags for the anemometer.")

    latest_readings = serializers.SerializerMethodField()
    daily_mean_speed = serializers.SerializerMethodField()
    weekly_mean_speed = serializers.SerializerMethodField()

    class Meta:
        model = Anemometer
        fields = '__all__'

    @extend_schema_field(serializers.ListSerializer(child=WindSpeedReadingSerializer()))
    def get_latest_readings(self, obj):
        """Get the latest 5 wind speed readings for the anemometer."""
        latest_readings = obj.readings.all()[:5]  # Query is pre-fetched in the view
        return WindSpeedReadingSerializer(latest_readings, many=True).data

    def get_daily_mean_speed(self, obj):
        """Get the mean wind speed for the current day."""
        current_time = now()
        start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = current_time.replace(hour=23, minute=59, second=59, microsecond=999999)
        daily_readings = obj.readings.filter(recorded_at__range=(start_of_day, end_of_day))
        return daily_readings.aggregate(Avg('speed_knots'))['speed_knots__avg'] or 0

    def get_weekly_mean_speed(self, obj):
        """Get the mean wind speed for the last 7 days."""
        week_ago = now() - timedelta(days=7)
        weekly_readings = obj.readings.filter(recorded_at__gte=week_ago)
        return weekly_readings.aggregate(Avg('speed_knots'))['speed_knots__avg'] or 0


class WindSpeedStatsSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    radius = serializers.FloatField(required=True, min_value=0)
