from datetime import (
    datetime,
    timedelta,
)

from dateutil.relativedelta import relativedelta

from django.test import TestCase

from booking.service import (
    _get_bookings,
    first_next_month,
    first_prev_month,
    first_this_month,
    get_calendars,
)
from booking.tests.scenario import default_scenario_booking


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

    def test_get_bookings(self):
        default_scenario_booking()
        d = first_this_month(datetime.now())
        e = d + relativedelta(years=+1, days=-1)
        _get_bookings(d, e)

    def test_get_calendars(self):
        default_scenario_booking()
        get_calendars()
