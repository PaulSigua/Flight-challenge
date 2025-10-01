from django.contrib import admin
from .models import City, FlightRequest

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "province", "code_iata", "active")
    search_fields = ("name", "province", "code_iata")
    list_filter = ("active",)

@admin.register(FlightRequest)
class FlightRequestAdmin(admin.ModelAdmin):
    list_display = ("owner", "city", "travel_date", "status", "notified_2days", "created_at")
    list_filter = ("status", "notified_2days")
    search_fields = ("owner__username", "city__name")
