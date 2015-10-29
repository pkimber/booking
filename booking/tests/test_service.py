# -*- encoding: utf-8 -*-
import pytest

from booking.service import (
    BookingCount,
    HtmlCalendar,
)
from booking.tests.scenario import demo_data


@pytest.mark.django_db
def test_get_bookings():
    demo_data()
    c = HtmlCalendar()
    c._get_bookings()


@pytest.mark.django_db
def test_get_calendars():
    demo_data()
    c = HtmlCalendar()
    c.get_calendars()


@pytest.mark.django_db
def test_booking_count():
    c = BookingCount()
    assert c.is_all_day() is False
    assert c.is_afternoon() is False
    assert c.is_morning() is False


@pytest.mark.django_db
def test_booking_count_afternoon():
    c = BookingCount()
    c.set_afternoon()
    assert c.is_afternoon() is True
    assert c.is_all_day() is False


@pytest.mark.django_db
def test_booking_count_morning():
    c = BookingCount()
    c.set_morning()
    assert c.is_morning() is True
    assert c.is_all_day() is False


@pytest.mark.django_db
def test_booking_count_morning_and_afternoon():
    c = BookingCount()
    c.set_afternoon()
    c.set_morning()
    assert c.is_all_day() is True
    assert c.is_afternoon() is False
    assert c.is_morning() is False
