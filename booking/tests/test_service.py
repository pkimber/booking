from datetime import datetime

from django.test import TestCase

from booking.service import (
    first_next_month,
    first_prev_month,
    first_this_month,
)


class TestBooking(TestCase):

    def test_first_this_month(self):
        d = datetime(2013, 2, 28)
        self.assertEquals(
            datetime(2013, 2, 1).date(),
            first_this_month(d)
        )

    def test_first_next_month(self):
        d = datetime(2013, 2, 28)
        self.assertEquals(
            datetime(2013, 3, 1).date(),
            first_next_month(d),
        )

    def test_first_prev_month(self):
        d = datetime(2013, 1, 31)
        self.assertEquals(
            datetime(2012, 12, 1).date(),
            first_prev_month(d),
        )
