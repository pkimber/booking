from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from base.tests.test_utils import PermTestCase
from booking.tests.scenario import (
    default_scenario_booking,
    get_alpe_d_huez,
)
from login.tests.scenario import default_scenario_login


class TestViewPerm(PermTestCase):

    def setUp(self):
        default_scenario_login()
        default_scenario_booking()

    def test_create(self):
        url = reverse('booking.create')
        self.assert_staff_only(url)

    def test_delete(self):
        b = get_alpe_d_huez()
        url = reverse('booking.delete', kwargs={'pk': b.pk})
        self.assert_staff_only(url)

    def test_list(self):
        url = reverse('booking.list')
        self.assert_staff_only(url)

    def test_list_month(self):
        today = datetime.today().date()
        url = reverse(
            'booking.list.month',
            kwargs=dict(year=today.year, month=today.month)
        )
        self.assert_staff_only(url)

    def test_update(self):
        b = get_alpe_d_huez()
        url = reverse('booking.update', kwargs={'pk': b.pk})
        self.assert_staff_only(url)
