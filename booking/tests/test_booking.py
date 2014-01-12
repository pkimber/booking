from datetime import (
    datetime,
    timedelta,
)

from django.core.exceptions import ValidationError
from django.test import TestCase

from booking.tests.model_maker import make_booking


class TestBooking(TestCase):

    def test_booking(self):
        """A simple booking."""
        today = datetime.today()
        next_week = today + timedelta(days=7)
        make_booking(
            next_week,
            next_week + timedelta(days=3),
            'Three days in the sun'
        )

    def test_end_before_start(self):
        """Booking - start before the end!"""
        today = datetime.today()
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

        Not going to check this for now.
        """
        pass

    def test_start_equals_end(self):
        """Booking - start date and end date are the same!"""
        today = datetime.today()
        next_week = today + timedelta(days=7)
        self.assertRaises(
            ValidationError,
            make_booking,
            next_week,
            next_week,
            'Not even one day in the sun',
        )
