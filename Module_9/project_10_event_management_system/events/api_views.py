# ============================================================================
#  api_views.py — event listing, capacity-checked registration, attendee list.
# ----------------------------------------------------------------------------
#  register() runs inside transaction.atomic() with select_for_update() so two
#  people grabbing the last seat at the same instant can't both get in.
# ============================================================================
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db import transaction

from .filters import EventFilter
from .models import Venue, Event, Registration
from .permissions import IsOrganizerOwnerOrReadOnly
from .serializers import VenueSerializer, EventSerializer, RegistrationSerializer


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [AllowAny]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("organizer", "venue")
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOwnerOrReadOnly]
    filterset_class = EventFilter
    search_fields = ["title", "description", "venue__name"]
    ordering_fields = ["datetime", "price"]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        """POST /api/events/<id>/register/ — book a seat (capacity-enforced)."""
        with transaction.atomic():
            event = Event.objects.select_for_update().get(pk=self.get_object().pk)
            already = Registration.objects.filter(
                event=event, user=request.user, status="CONFIRMED").exists()
            if already:
                return Response({"detail": "You are already registered."}, status=400)
            confirmed = Registration.objects.filter(
                event=event, status="CONFIRMED").count()
            if confirmed >= event.capacity:
                return Response({"detail": "This event is full."}, status=400)
            reg, _ = Registration.objects.update_or_create(
                event=event, user=request.user, defaults={"status": "CONFIRMED"})
        return Response(RegistrationSerializer(reg).data, status=201)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """POST /api/events/<id>/cancel/ — cancel your own registration."""
        event = self.get_object()
        reg = Registration.objects.filter(event=event, user=request.user).first()
        if reg is None:
            return Response({"detail": "You are not registered."}, status=400)
        reg.status = "CANCELLED"
        reg.save()
        return Response(RegistrationSerializer(reg).data)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def attendees(self, request, pk=None):
        """GET /api/events/<id>/attendees/ — organizer (owner) or admin only."""
        event = self.get_object()
        if event.organizer_id != request.user.id and not request.user.is_staff:
            return Response({"detail": "Only the organizer can view attendees."},
                            status=403)
        regs = event.registrations.filter(status="CONFIRMED").select_related("user")
        return Response(RegistrationSerializer(regs, many=True).data)


class RegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    """A user's own registrations ("My events")."""
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.select_related("event").filter(
            user=self.request.user)
