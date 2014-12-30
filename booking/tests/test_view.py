# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

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
from login.tests.factories import TEST_PASSWORD
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
)


class TestView(TestCase):

    def setUp(self):
        default_scenario_login()
        default_scenario_booking()
        staff = get_user_staff()
        # update simple content
        self.assertTrue(
            self.client.login(username=staff.username, password=TEST_PASSWORD)
        )

    def test_create(self):
        today = datetime.today().date()
        start_date = today + timedelta(days=2)
        end_date = today + timedelta(days=5)
        response = self.client.post(
            reverse('booking.create'),
            dict(
                start_date=start_date,
                end_date=end_date,
                title='Hatherleigh',
            )
        )
        self.assertEqual(response.status_code, 302)
        # check booking
        try:
            Booking.objects.get(title='Hatherleigh')
        except Booking.DoesNotExist:
            self.fail('cannot find new booking')

    def test_create_no_title(self):
        """Booking a self-catering cottage requires from/to date and title."""
        today = datetime.today().date()
        start_date = today + timedelta(days=2)
        end_date = today + timedelta(days=5)
        response = self.client.post(
            reverse('booking.create'),
            dict(
                start_date=start_date,
                end_date=end_date,
            )
        )
        self.assertEqual(response.status_code, 200)
        form = response.context_data['form']
        self.assertEqual(
            {'title': ['This field is required.']},
            form.errors,
        )

    def test_create_no_end_date(self):
        """Booking a self-catering cottage requires from/to date and title."""
        today = datetime.today().date()
        start_date = today + timedelta(days=2)
        response = self.client.post(
            reverse('booking.create'),
            dict(
                start_date=start_date,
                title='Hatherleigh',
            )
        )
        self.assertEqual(response.status_code, 200)
        form = response.context_data['form']
        self.assertEqual(
            {'end_date': ['This field is required.']},
            form.errors,
        )

    def test_delete(self):
        b = get_alpe_d_huez()
        response = self.client.post(
            reverse('booking.delete', kwargs=dict(pk=b.pk)),
        )
        self.assertEqual(response.status_code, 302)
        # check booking
        try:
            b = get_alpe_d_huez()
            self.fail('booking was not deleted')
        except Booking.DoesNotExist:
            pass

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
                start_date=b.start_date,
                end_date=b.end_date,
                title='Zeal Monachorum',
            )
        )
        self.assertEqual(response.status_code, 302)
        # check booking
        try:
            Booking.objects.get(title='Zeal Monachorum')
        except Booking.DoesNotExist:
            self.fail('cannot find updated booking')
