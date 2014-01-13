from datetime import (
    datetime,
    timedelta,
)

from dateutil.relativedelta import relativedelta

from django.test import TestCase

from booking.service import HtmlCalendar
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
