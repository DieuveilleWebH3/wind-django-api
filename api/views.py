import logging
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from geopy.distance import geodesic

from .models import Anemometer, WindSpeedReading
from .serializers import (
    AnemometerSerializer,
    WindSpeedReadingSerializer,
    WindSpeedStatsSerializer,
)
from .filters import AnemometerFilter

logger = logging.getLogger("api")


# Create your views here.


@extend_schema(tags=["Anemometers"])
class AnemometerViewSet(viewsets.ModelViewSet):
    queryset = Anemometer.objects.prefetch_related("readings")
    serializer_class = AnemometerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = AnemometerFilter
    search_fields = ["name"]

    def create(self, request, *args, **kwargs):
        logger.info("Creating a new anemometer.")

        response = super().create(request, *args, **kwargs)

        return response

    def update(self, request, *args, **kwargs):
        logger.info("Updating an anemometer.")

        response = super().update(request, *args, **kwargs)

        return response

    def destroy(self, request, *args, **kwargs):
        logger.warning("Deleting an anemometer.")

        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["Wind Speed Readings"])
class WindSpeedReadingViewSet(viewsets.ModelViewSet):
    queryset = WindSpeedReading.objects.all()
    serializer_class = WindSpeedReadingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["anemometer"]

    def create(self, request, *args, **kwargs):
        logger.info("Creating a new wind speed reading.")

        response = super().create(request, *args, **kwargs)

        return response


@extend_schema(tags=["Wind Speed Stats"], responses={200: WindSpeedReadingSerializer})
class WindSpeedStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=WindSpeedStatsSerializer,
        parameters=[
            OpenApiParameter(
                name="latitude",
                description="Latitude of the central point",
                required=True,
                type=float,
            ),
            OpenApiParameter(
                name="longitude",
                description="Longitude of the central point",
                required=True,
                type=float,
            ),
            OpenApiParameter(
                name="radius",
                description="Search radius in nautical miles",
                required=True,
                type=float,
            ),
        ],
        responses={200: dict},
    )
    def get(self, request):
        logger.info("Processing wind speed stats request.")
        serializer = WindSpeedStatsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        latitude = serializer.validated_data["latitude"]
        longitude = serializer.validated_data["longitude"]
        radius = serializer.validated_data["radius"]

        readings = WindSpeedReading.objects.all()
        filtered_readings = [
            r
            for r in readings
            if geodesic(
                (latitude, longitude), (r.anemometer.latitude, r.anemometer.longitude)
            ).nautical
            <= radius
        ]
        speeds = [r.speed_knots for r in filtered_readings]

        response_data = {
            "min": min(speeds, default=0),
            "max": max(speeds, default=0),
            "mean": sum(speeds) / len(speeds) if speeds else 0,
        }
        logger.debug(f"Wind speed stats calculated: {response_data}")
        return Response(response_data)
