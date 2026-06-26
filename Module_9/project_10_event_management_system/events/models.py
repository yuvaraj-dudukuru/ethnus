# ============================================================================
#  models.py — venues, events and capacity-limited registrations.
# ----------------------------------------------------------------------------
#  Organizer(User) 1 ─< N Event >─ N 1 Venue
#  Event 1 ─< N Registration >─ N 1 User   (unique per user+event)
# ============================================================================
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=300, blank=True)
    capacity = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="events_organized")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    datetime = models.DateTimeField()
    venue = models.ForeignKey(
        Venue, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="events")
    capacity = models.PositiveIntegerField(default=50)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["datetime"]

    @property
    def registered_count(self):
        return self.registrations.filter(status="CONFIRMED").count()

    @property
    def seats_left(self):
        return max(0, self.capacity - self.registered_count)

    def __str__(self):
        return self.title


class Registration(models.Model):
    STATUS = [("CONFIRMED", "Confirmed"), ("CANCELLED", "Cancelled")]
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="registrations")
    registered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default="CONFIRMED")

    class Meta:
        unique_together = ("event", "user")
        ordering = ["-registered"]

    def __str__(self):
        return f"{self.user.username} → {self.event.title} ({self.status})"
