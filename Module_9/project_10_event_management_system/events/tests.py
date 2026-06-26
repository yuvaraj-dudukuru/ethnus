# ============================================================================
#  tests.py — Event API checks.  Run with:  python manage.py test
# ============================================================================
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from .models import Event


class EventAPITests(APITestCase):
    def setUp(self):
        self.organizer = User.objects.create_user("org", password="x")
        self.u1 = User.objects.create_user("user1", password="x")
        self.u2 = User.objects.create_user("user2", password="x")
        soon = timezone.now() + timedelta(days=7)
        self.event = Event.objects.create(
            organizer=self.organizer, title="Tech Meetup",
            datetime=soon, capacity=10)
        self.tiny = Event.objects.create(
            organizer=self.organizer, title="VIP Dinner",
            datetime=soon, capacity=1)

    def test_public_can_list_events(self):
        self.assertEqual(self.client.get("/api/events/").status_code, 200)

    def test_register_requires_login(self):
        self.assertEqual(
            self.client.post(f"/api/events/{self.event.id}/register/").status_code, 401)

    def test_register_then_duplicate_rejected(self):
        self.client.force_authenticate(self.u1)
        self.assertEqual(
            self.client.post(f"/api/events/{self.event.id}/register/").status_code, 201)
        self.assertEqual(
            self.client.post(f"/api/events/{self.event.id}/register/").status_code, 400)

    def test_capacity_is_enforced(self):
        self.client.force_authenticate(self.u1)
        self.assertEqual(
            self.client.post(f"/api/events/{self.tiny.id}/register/").status_code, 201)
        self.client.force_authenticate(self.u2)           # last seat already gone
        r = self.client.post(f"/api/events/{self.tiny.id}/register/")
        self.assertEqual(r.status_code, 400)

    def test_cancel_frees_a_seat(self):
        self.client.force_authenticate(self.u1)
        self.client.post(f"/api/events/{self.tiny.id}/register/")
        self.client.post(f"/api/events/{self.tiny.id}/cancel/")
        self.client.force_authenticate(self.u2)
        self.assertEqual(
            self.client.post(f"/api/events/{self.tiny.id}/register/").status_code, 201)

    def test_attendees_visible_to_organizer_only(self):
        self.client.force_authenticate(self.u1)
        self.client.post(f"/api/events/{self.event.id}/register/")
        # A random attendee may not see the attendee list.
        self.assertEqual(
            self.client.get(f"/api/events/{self.event.id}/attendees/").status_code, 403)
        # The organizer can.
        self.client.force_authenticate(self.organizer)
        ok = self.client.get(f"/api/events/{self.event.id}/attendees/")
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(len(ok.data), 1)
