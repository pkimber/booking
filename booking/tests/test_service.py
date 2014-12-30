# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from booking.service import (
    BookingCount,
    HtmlCalendar,
)
from booking.tests.scenario import default_scenario_booking


class TestService(TestCase):

    def test_get_bookings(self):
        default_scenario_booking()
        c = HtmlCalendar()
        c._get_bookings()

    def test_get_calendars(self):
        default_scenario_booking()
        c = HtmlCalendar()
        c.get_calendars()

    def test_booking_count(self):
        c = BookingCount()
        self.assertFalse(c.is_all_day())
        self.assertFalse(c.is_afternoon())
        self.assertFalse(c.is_morning())

    def test_booking_count_afternoon(self):
        c = BookingCount()
        c.set_afternoon()
        self.assertTrue(c.is_afternoon())
        self.assertFalse(c.is_all_day())

    def test_booking_count_morning(self):
        c = BookingCount()
        c.set_morning()
        self.assertTrue(c.is_morning())
        self.assertFalse(c.is_all_day())

    def test_booking_count_morning_and_afternoon(self):
        c = BookingCount()
        c.set_afternoon()
        c.set_morning()
        self.assertTrue(c.is_all_day())
        self.assertFalse(c.is_afternoon())
        self.assertFalse(c.is_morning())
