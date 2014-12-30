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
    PermissionFactory,
)


class TestViewPerm(PermTestCase):

    def setUp(self):
        self.setup_users()

    def test_event_create(self):
        self.assert_staff_only(reverse('event.create'))

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
        event = BookingFactory(
            start_date=date(2013, 3, 30),
            start_time=timezone.now().time(),
        )
        url = reverse(
            'event.update',
            kwargs=dict(pk=event.pk)
        )
        self.assert_staff_only(url)

    def test_event_category_create(self):
        self.assert_staff_only(reverse('event.category.create'))

    def test_event_category_list(self):
        self.assert_staff_only(reverse('event.category.list'))

    def test_event_category_update(self):
        category = CategoryFactory()
        url = reverse(
            'event.category.update',
            kwargs=dict(pk=category.pk)
        )
        self.assert_staff_only(url)

    def test_event_location_create(self):
        self.assert_staff_only(reverse('event.location.create'))

    def test_event_location_list(self):
        self.assert_staff_only(reverse('event.location.list'))

    def test_event_location_update(self):
        location = LocationFactory()
        url = reverse(
            'event.location.update',
            kwargs=dict(pk=location.pk)
        )
        self.assert_staff_only(url)

    #def test_event_permission_create(self):
    #    self.assert_staff_only(reverse('event.permission.create'))

    #def test_event_permission_list(self):
    #    self.assert_staff_only(reverse('event.permission.list'))

    #def test_event_permission_update(self):
    #    permission = PermissionFactory()
    #    url = reverse(
    #        'event.permission.update',
    #        kwargs=dict(pk=permission.pk)
    #    )
    #    self.assert_staff_only(url)

    #def test_event_status_create(self):
    #    self.assert_staff_only(reverse('event.status.create'))

    #def test_event_status_list(self):
    #    self.assert_staff_only(reverse('event.status.list'))

    #def test_event_status_update(self):
    #    status = StatusFactory()
    #    url = reverse(
    #        'event.status.update',
    #        kwargs=dict(pk=status.pk)
    #    )
    #    self.assert_staff_only(url)
