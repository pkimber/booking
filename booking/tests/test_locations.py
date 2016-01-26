# -*- encoding: utf-8 -*-

from django.test import TestCase
from django.utils import timezone

from booking.models import (
    BookingSettings,
    Location,
    Room,
)


class TestEvent(TestCase):

    def test_location_has_rooms(self):
        booking_settings = BookingSettings.load()
        booking_settings.display_rooms = True
        booking_settings.save()
        Location.objects.create_location(title='Community Centre')
        community_centre = Location.objects.get(title='Community Centre')
        assert community_centre.has_rooms == False
        Room.objects.create_room(location=community_centre, title='Kitchen')
        community_centre = Location.objects.get(title='Community Centre')
        assert community_centre.has_rooms
