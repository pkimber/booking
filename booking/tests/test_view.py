from datetime import (
    datetime,
    timedelta,
)

from django.core.urlresolvers import reverse
from django.test import TestCase

from booking.models import Booking
from booking.tests.scenario import (
    default_scenario_booking,
    get_alpe_d_huez,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    STAFF,
)


class TestView(TestCase):

    def setUp(self):
        default_scenario_login()
        default_scenario_booking()
        staff = get_user_staff()
        # update simple content
        self.assertTrue(
            self.client.login(username=staff.username, password=STAFF)
        )

    def test_create(self):
        today = datetime.today().date()
        from_date = today + timedelta(days=2)
        to_date = today + timedelta(days=5)
        response = self.client.post(
            reverse('booking.create'),
            dict(
                from_date=from_date,
                to_date=to_date,
                title='Hatherleigh',
            )
        )
        self.assertEqual(response.status_code, 302)
        # check booking
        try:
            Booking.objects.get(title='Hatherleigh')
        except Booking.DoesNotExist:
            self.fail('cannot find new booking')

    def test_list(self):
        response = self.client.get(reverse('booking.list'))
        self.assertEqual(response.status_code, 200)

    def test_list_month(self):
        today = datetime.today().date()
        response = self.client.get(
            reverse(
                'booking.list.month',
                kwargs=dict(year=today.year, month=today.month)
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        b = get_alpe_d_huez()
        response = self.client.post(
            reverse('booking.update', kwargs=dict(pk=b.pk)),
            dict(
                from_date=b.from_date,
                to_date=b.to_date,
                title='Zeal Monachorum',
            )
        )
        self.assertEqual(response.status_code, 302)
        # check booking
        try:
            Booking.objects.get(title='Zeal Monachorum')
        except Booking.DoesNotExist:
            self.fail('cannot find updated booking')
