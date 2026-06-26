# ============================================================================
#  seed.py — admin/admin + an organizer + an attendee + sample events.
#      python manage.py seed
# ============================================================================
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from events.models import Venue, Event


class Command(BaseCommand):
    help = "Create admin/admin, organizer1/organizer, attendee1/attendee + events."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@event.test", "admin")
        organizer, _ = User.objects.get_or_create(username="organizer1")
        organizer.set_password("organizer")
        organizer.save()
        attendee, _ = User.objects.get_or_create(username="attendee1")
        attendee.set_password("attendee")
        attendee.save()
        self.stdout.write(self.style.SUCCESS(
            "Users: admin/admin, organizer1/organizer, attendee1/attendee."))

        hall, _ = Venue.objects.get_or_create(
            name="Grand Hall", defaults={"address": "1 Main St", "capacity": 300})
        room, _ = Venue.objects.get_or_create(
            name="Meeting Room B", defaults={"address": "2 Side Rd", "capacity": 30})

        now = timezone.now()
        events = [
            ("Django Conference 2026", now + timedelta(days=30), hall, 200, "0"),
            ("Startup Pitch Night", now + timedelta(days=10), room, 25, "15.00"),
            ("Free Yoga in the Park", now + timedelta(days=3), None, 50, "0"),
        ]
        for title, when, venue, cap, price in events:
            Event.objects.get_or_create(
                title=title,
                defaults={"organizer": organizer, "datetime": when, "venue": venue,
                          "capacity": cap, "price": price,
                          "description": f"Join us for {title}!"})

        self.stdout.write(self.style.SUCCESS(
            "Seeded venues and events. Run: python manage.py runserver"))
