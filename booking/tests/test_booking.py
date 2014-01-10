from datetime import (
    datetime,
    timedelta,
)

from django.core.exceptions import ValidationError
from django.test import TestCase

from booking.tests.model_maker import make_booking


class TestBooking(TestCase):

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
