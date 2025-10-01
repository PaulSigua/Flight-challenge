from rest_framework.routers import DefaultRouter
from .views import CityViewSet, FlightRequestViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"cities", CityViewSet, basename="city")
router.register(r"flight-requests", FlightRequestViewSet, basename="flightrequest")

urlpatterns = [
    path("", include(router.urls)),
]
