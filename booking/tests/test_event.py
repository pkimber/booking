# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.utils import timezone

from booking.models import (
    Booking,
    Permission,
)

from .factories import (
    BookingFactory,
    CategoryFactory,
)


class TestEvent(TestCase):

    def test_public_calendar(self):
        public = Permission.objects.get(slug=Permission.PUBLIC)
        user = Permission.objects.get(slug=Permission.USER)
        staff = Permission.objects.get(slug=Permission.STAFF)
        BookingFactory(title='a', permission=public)
        BookingFactory(title='b', permission=user)
        BookingFactory(title='c', permission=staff)
        BookingFactory(title='d', permission=public)
        events = Booking.objects.public_calendar()
        self.assertEquals(
            ['a', 'd'],
            [e.title for e in events]
        )

    def test_public_calendar_date(self):
        """Select published events within the next two months."""
        today = timezone.now().date()
        b4 = today + relativedelta(days=-1)
        one = today + relativedelta(days=7)
        two = today + relativedelta(days=14)
        year = today + relativedelta(years=1)
        public = Permission.objects.get(slug=Permission.PUBLIC)
        #publish = StatusFactory(publish=True)
        start = timezone.now().time()
        BookingFactory(
            title='a', start_date=one, start_time=start, #status=publish,
            permission=public,
        )
        BookingFactory(
            title='b', start_date=two, start_time=start, #status=publish,
            permission=public,
        )
        # do NOT include this one because it is older than two months
        BookingFactory(
            title='c', start_date=year, start_time=start, #status=publish,
            permission=public,
        )
        # do NOT include this one because it for yesterday
        BookingFactory(
            title='d', start_date=b4, start_time=start, #status=publish,
            permission=public,
        )
        events = Booking.objects.public_calendar()
        self.assertEquals(
            ['a', 'b'],
            [e.title for e in events]
        )

    def test_public_delete(self):
        today = timezone.now().date()
        one = today + relativedelta(days=7)
        public = Permission.objects.get(slug=Permission.PUBLIC)
        #publish = StatusFactory(publish=True)
        start = timezone.now().time()
        BookingFactory(
            title='a', start_date=one, start_time=start, #status=publish,
            permission=public,
        )
        # do NOT include this one because it is deleted
        BookingFactory(
            title='b', start_date=one, start_time=start, #status=publish,
            permission=public, deleted=True,
        )
        events = Booking.objects._public()
        self.assertEquals(
            ['a',],
            [e.title for e in events]
        )

    def test_public_promoted(self):
        """Promoted events are between two and eight months."""
        today = timezone.now().date()
        one = today + relativedelta(days=7)
        six = today + relativedelta(months=6)
        year = today + relativedelta(years=1)
        public = Permission.objects.get(slug=Permission.PUBLIC)
        #publish = StatusFactory(publish=True)
        #pending = StatusFactory(publish=False)
        promote = CategoryFactory(promote=True)
        routine = CategoryFactory(promote=False, routine=True)
        start = timezone.now().time()
        # do NOT include this one because it is less than 2 months
        BookingFactory(
            title='a', start_date=one, start_time=start, #status=publish,
            permission=public,
        )
        BookingFactory(
            title='b', start_date=six, start_time=start, #status=publish,
            permission=public, category=promote,
        )
        # do NOT include this one because it is a routine event (not promoted)
        BookingFactory(
            title='c', start_date=six, start_time=start, #status=publish,
            permission=public, category=routine,
        )
        # do NOT include this one because it is older than 8 months
        BookingFactory(
            title='d', start_date=year, start_time=start, #status=publish,
            permission=public,
        )
        # do NOT include this one because it is deleted
        BookingFactory(
            title='e', start_date=six, start_time=start, #status=publish,
            permission=public, deleted=True,
        )
        # do NOT include this one because it is not published
        BookingFactory(
            title='e', start_date=six, start_time=start, #status=pending,
            permission=public,
        )
        events = Booking.objects.public_promoted()
        self.assertEquals(
            ['b',],
            [e.title for e in events]
        )

    #def test_public_status(self):
    #    today = timezone.now().date()
    #    one = today + relativedelta(days=7)
    #    public = PermissionFactory(slug=Permission.PUBLIC)
    #    #publish = StatusFactory(publish=True)
    #    #pending = StatusFactory(publish=False)
    #    start = timezone.now().time()
    #    BookingFactory(
    #        title='a', start_date=one, start_time=start, #status=pending,
    #        permission=public,
    #    )
    #    BookingFactory(
    #        title='b', start_date=one, start_time=start, #status=publish,
    #        permission=public,
    #    )
    #    events = Booking.objects._public()
    #    self.assertEquals(
    #        ['b',],
    #        [e.title for e in events]
    #    )
