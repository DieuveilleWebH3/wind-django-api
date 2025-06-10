from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AnemometerViewSet, WindSpeedReadingViewSet, WindSpeedStatsView


router = DefaultRouter()
router.register(r"anemometers", AnemometerViewSet)
router.register(r"readings", WindSpeedReadingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("stats/", WindSpeedStatsView.as_view(), name="stats"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
