# ============================================================================
#  serializers.py — JSON shapes for events.
# ============================================================================
from rest_framework import serializers
from .models import Venue, Event, Registration


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name", "address", "capacity"]


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.CharField(source="organizer.username", read_only=True)
    venue = VenueSerializer(read_only=True)
    venue_id = serializers.PrimaryKeyRelatedField(
        queryset=Venue.objects.all(), source="venue",
        write_only=True, required=False, allow_null=True)
    registered_count = serializers.IntegerField(read_only=True)
    seats_left = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "description", "datetime", "organizer",
                  "venue", "venue_id", "capacity", "price",
                  "registered_count", "seats_left", "created"]
        read_only_fields = ["id", "organizer", "created"]


class RegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source="event.title", read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Registration
        fields = ["id", "event", "event_title", "user", "status", "registered"]
        read_only_fields = fields
