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
        return WindSpeedReadingSerializer(obj.readings.all()[:5], many=True).data

    def get_daily_mean_speed(self, obj):
        today = now().date()
        daily_readings = obj.readings.filter(recorded_at__date=today)
        return daily_readings.aggregate(Avg('speed_knots'))['speed_knots__avg'] or 0
    
    def get_weekly_mean_speed(self, obj):
        week_ago = now() - timedelta(days=7)
        weekly_readings = obj.readings.filter(recorded_at__gte=week_ago)
        return weekly_readings.aggregate(Avg('speed_knots'))['speed_knots__avg'] or 0


class WindSpeedStatsSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    radius = serializers.FloatField(required=True, min_value=0)
