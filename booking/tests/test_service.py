from datetime import (
    datetime,
    timedelta,
)

from dateutil.relativedelta import relativedelta

from django.test import TestCase

from booking.service import (
    _get_bookings,
    get_calendars,
)
from booking.tests.scenario import default_scenario_booking


class TestService(TestCase):

    def test_get_bookings(self):
        default_scenario_booking()
        from_date = datetime.now() + relativedelta(day=1)
        to_date = from_date + relativedelta(years=+1, days=-1)
        _get_bookings(from_date, to_date)

    def test_get_calendars(self):
        default_scenario_booking()
        get_calendars()
