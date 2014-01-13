from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from booking.models import Booking
from booking.tests.scenario import default_scenario_booking
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    STAFF,
)


class TestView(TestCase):

    def setUp(self):
        default_scenario_login()
        default_scenario_booking()

    def test_list(self):
        staff = get_user_staff()
        self.assertTrue(
            self.client.login(username=staff.username, password=STAFF)
        )
        response = self.client.get(reverse('booking.list'))
        self.assertEqual(response.status_code, 200)

    def test_month(self):
        staff = get_user_staff()
        self.assertTrue(
            self.client.login(username=staff.username, password=STAFF)
        )
        today = datetime.today().date()
        response = self.client.get(
            reverse(
                'booking.list.month',
                kwargs=dict(year=today.year, month=today.month)
            )
        )
        self.assertEqual(response.status_code, 200)
