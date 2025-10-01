from django.db import models
from django.conf import settings

class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=100, blank=True, null=True)
    code_iata = models.CharField(max_length=10, blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class FlightRequest(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_RESERVED = "RESERVED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_RESERVED, "Reserved"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="flight_requests")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="flight_requests")
    travel_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    notified_2days = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner.username} - {self.city.name} ({self.travel_date})"
