# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.utils import timezone

from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase

from .factories import (
    BookingFactory,
    CategoryFactory,
    LocationFactory,
    RotaTypeFactory,
)


class TestViewPerm(PermTestCase):

    def setUp(self):
        self.setup_users()

    def test_event_create(self):
        self.assert_staff_only(reverse('booking.create'))

    def test_event_list(self):
        self.assert_logged_in(reverse('booking.list'))

    def test_event_list_month(self):
        today = timezone.now().date()
        url = reverse(
            'booking.list.month',
            kwargs=dict(year=today.year, month=today.month),
        )
        self.assert_logged_in(url)

    def test_event_update(self):
        event = BookingFactory(start_date=date(2013, 3, 30))
        url = reverse(
            'booking.update',
            kwargs=dict(pk=event.pk)
        )
        self.assert_staff_only(url)

    def test_event_category_create(self):
        self.assert_staff_only(reverse('booking.category.create'))

    def test_event_category_list(self):
        self.assert_staff_only(reverse('booking.category.list'))

    def test_event_category_update(self):
        category = CategoryFactory()
        url = reverse(
            'booking.category.update',
            kwargs=dict(pk=category.pk)
        )
        self.assert_staff_only(url)

    def test_event_location_create(self):
        self.assert_staff_only(reverse('booking.location.create'))

    def test_event_location_detail(self):
        location = LocationFactory()
        url = reverse(
            'booking.location',
            kwargs=dict(pk=location.pk)
        )
        self.assert_any(url)

    def test_event_location_list(self):
        self.assert_staff_only(reverse('booking.location.list'))

    def test_event_location_update(self):
        location = LocationFactory()
        url = reverse(
            'booking.location.update',
            kwargs=dict(pk=location.pk)
        )
        self.assert_staff_only(url)

    def test_rota_type_create(self):
        self.assert_staff_only(reverse('booking.rota.type.create'))

    def test_rota_type_list(self):
        self.assert_staff_only(reverse('booking.rota.type.list'))

    def test_rota_type_update(self):
        rota_type = RotaTypeFactory()
        url = reverse(
            'booking.rota.type.update',
            kwargs=dict(pk=rota_type.pk)
        )
        self.assert_staff_only(url)
