from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from .models import City, FlightRequest
from .tasks import notify_owners_two_days_before

User = get_user_model()

class MinimalBackendTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="u1@example.com", password="pass")
        self.operator = User.objects.create_user(username="op", email="op@example.com", password="pass", is_staff=True)
        self.city = City.objects.create(name="Quito")

    def test_create_flight_request_via_api(self):
        client = APIClient()
        resp = client.post("/api/auth/token/", {"username": "user1", "password": "pass"}, format="json")
        self.assertEqual(resp.status_code, 200)
        token = resp.data["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        travel_date = str(timezone.localdate() + timedelta(days=5))
        r = client.post("/api/flight-requests/", {"city": self.city.id, "travel_date": travel_date}, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(FlightRequest.objects.count(), 1)

    def test_operator_can_reserve(self):
        fr = FlightRequest.objects.create(owner=self.user, city=self.city, travel_date=timezone.localdate() + timedelta(days=4))
        client = APIClient()
        resp = client.post("/api/auth/token/", {"username": "op", "password": "pass"}, format="json")
        token = resp.data["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        r = client.post(f"/api/flight-requests/{fr.id}/reserve/")
        self.assertEqual(r.status_code, 200)
        fr.refresh_from_db()
        self.assertEqual(fr.status, FlightRequest.STATUS_RESERVED)

    def test_task_notify_marks_notified(self):
        fr = FlightRequest.objects.create(owner=self.user, city=self.city, travel_date=timezone.localdate() + timedelta(days=2))
        result = notify_owners_two_days_before()
        fr.refresh_from_db()
        self.assertTrue(fr.notified_2days)
