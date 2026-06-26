from django.contrib import admin
from .models import Venue, Event, Registration


class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "capacity"]
    search_fields = ["name"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "datetime", "venue", "capacity",
                    "registered_count", "seats_left", "organizer"]
    list_filter = ["venue"]
    search_fields = ["title"]
    inlines = [RegistrationInline]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "status", "registered"]
    list_filter = ["status"]
