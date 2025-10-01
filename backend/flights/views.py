from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from .models import City, FlightRequest
from .serializers import CitySerializer, FlightRequestSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOperator
from .services import reserve_flight_request

CITIES_CACHE_KEY = "cities:list:v1"
CITIES_CACHE_TTL = 60 * 60  # 1h

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        data = cache.get(CITIES_CACHE_KEY)
        if not data:
            qs = self.filter_queryset(self.get_queryset().filter(active=True))
            data = CitySerializer(qs, many=True).data
            cache.set(CITIES_CACHE_KEY, data, timeout=CITIES_CACHE_TTL)
        return Response(data)

    def perform_create(self, serializer):
        inst = serializer.save()
        cache.delete(CITIES_CACHE_KEY)
        return inst

    def perform_update(self, serializer):
        inst = serializer.save()
        cache.delete(CITIES_CACHE_KEY)
        return inst

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(CITIES_CACHE_KEY)

class FlightRequestViewSet(viewsets.ModelViewSet):
    queryset = FlightRequest.objects.select_related("owner", "city").all()
    serializer_class = FlightRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset.filter(status=FlightRequest.STATUS_PENDING)
        return self.queryset.filter(owner=user)

    @action(detail=True, methods=["post"], permission_classes=[IsOperator])
    def reserve(self, request, pk=None):
        fr = self.get_object() 
        try:
            fr = reserve_flight_request(fr, request.user)
            return Response({"detail": "Solicitud marcada como RESERVED."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
