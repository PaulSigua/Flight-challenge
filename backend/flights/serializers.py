from rest_framework import serializers
from .models import City, FlightRequest
from django.utils import timezone

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "province", "code_iata", "active"]

class FlightRequestSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.filter(active=True))

    class Meta:
        model = FlightRequest
        fields = ["id", "owner", "city", "travel_date", "status", "created_at", "updated_at"]

    def validate_travel_date(self, value):
        today = timezone.localdate()
        if value < today:
            raise serializers.ValidationError("La fecha de viaje no puede ser en el pasado.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["owner"] = user
        return super().create(validated_data)
