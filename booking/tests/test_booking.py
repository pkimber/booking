# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import (
    datetime,
    time,
    timedelta,
)

from django.core.exceptions import ValidationError
from django.test import TestCase

from base.tests.model_maker import clean_and_save
from booking.models import Booking

from .factories import BookingFactory, CategoryFactory


class TestBooking(TestCase):

    def test_booking(self):
        """A simple booking."""
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        clean_and_save(BookingFactory(
            start_date=next_week,
            end_date=next_week + timedelta(days=3),
            title='Three days in the sun'
        ))

    def test_is_current(self):
        """A simple booking."""
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        b = BookingFactory(
            start_date=next_week,
            end_date=next_week + timedelta(days=3),
            title='Three days in the sun'
        )
        self.assertTrue(b.is_current())

    def test_is_current_in_the_past(self):
        """A simple booking."""
        today = datetime.today().date()
        last_week = today + timedelta(days=-7)
        b = Booking(**dict(
            start_date=last_week,
            end_date=last_week + timedelta(days=3),
            title='Three days in the sun'
        ))
        b.save()
        self.assertFalse(b.is_current())

    def test_booking_in_the_past(self):
        """Cannot create a booking in the past."""
        today = datetime.today().date()
        last_week = today + timedelta(days=-7)
        with self.assertRaises(ValidationError):
            clean_and_save(BookingFactory(
                start_date=last_week,
                end_date=last_week + timedelta(days=3),
                title='Missed our holiday'
            ))

    def test_end_before_start(self):
        """Booking - start before the end!"""
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        with self.assertRaises(ValidationError):
            clean_and_save(BookingFactory(
            start_date=next_week,
            end_date=next_week + timedelta(days=-2),
            title='Two days in the sun',
            ))

    def test_end_time_before_start_time(self):
        """Booking - start before the end!"""
        category = CategoryFactory(per_day_booking=False)

        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        with self.assertRaises(ValidationError):
            clean_and_save(BookingFactory(
                category=category,
                start_date=next_week,
                end_date=next_week,
                start_time=time(hour=9),
                end_time=time(hour=8),
                title='not an hour',
            ))

    def test_timed_booking(self):
        """Booking - timed booking allows a two hour booking"""
        category = CategoryFactory(per_day_booking=False)

        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        clean_and_save(BookingFactory(
            category=category,
            start_date=next_week,
            end_date=next_week,
            start_time=time(hour=11),
            end_time=time(hour=13),
            title='fun at lunchtime',
        ))
        b = Booking.objects.get(title='fun at lunchtime')
        assert b.start_time == time(hour=11)

    def test_double_booking(self):
        """Don't allow a double booking.

        Not going to write the code to check this (for now).
        """
        pass

    def test_start_equals_end(self):
        """Booking - start date and end date are the same!"""
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        with self.assertRaises(ValidationError):
            clean_and_save(BookingFactory(
            start_date=next_week,
            end_date=next_week,
            title='Not even one day in the sun',
            ))
