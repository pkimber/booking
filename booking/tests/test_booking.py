from datetime import (
    datetime,
    timedelta,
)

from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from booking.models import Booking
from booking.tests.model_maker import make_booking


class TestBooking(TestCase):

    def test_booking(self):
        """A simple booking."""
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        make_booking(
            next_week,
            next_week + timedelta(days=3),
            'Three days in the sun'
        )

    def test_is_current(self):
        """A simple booking."""
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        b = make_booking(
            next_week,
            next_week + timedelta(days=3),
            'Three days in the sun'
        )
        self.assertTrue(b.is_current())

    def test_is_current_in_the_past(self):
        """A simple booking."""
        today = datetime.today().date()
        last_week = today + timedelta(days=-7)
        b = Booking(**dict(
            from_date=last_week,
            to_date=last_week + timedelta(days=3),
            title='Three days in the sun'
        ))
        b.save()
        self.assertFalse(b.is_current())

    def test_booking_in_the_past(self):
        """Cannot create a booking in the past."""
        today = datetime.today().date()
        last_week = today + timedelta(days=-7)
        self.assertRaises(
            ValidationError,
            make_booking,
            last_week,
            last_week + timedelta(days=3),
            'Missed our holiday'
        )

    def test_end_before_start(self):
        """Booking - start before the end!"""
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        self.assertRaises(
            ValidationError,
            make_booking,
            next_week,
            next_week + timedelta(days=-2),
            'Two days in the sun',
        )

    def test_double_booking(self):
        """Don't allow a double booking.

        Not going to write the code to check this (for now).
        """
        pass

    def test_start_equals_end(self):
        """Booking - start date and end date are the same!"""
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        self.assertRaises(
            ValidationError,
            make_booking,
            next_week,
            next_week,
            'Not even one day in the sun',
        )
