# -*- encoding: utf-8 -*-
import pytest

from datetime import date
from dateutil.relativedelta import relativedelta

from booking.service import (
    BookingCount,
    HtmlCalendar,
)
from booking.tests.factories import BookingFactory


def _demo_data():
    # today
    BookingFactory(
        start_date=date.today(),
        end_date=date.today()+relativedelta(days=2),
    )
    # in the past
    start_date = date.today() + relativedelta(days=-10)
    BookingFactory(
        start_date=start_date,
        end_date=start_date+relativedelta(days=3),
    )
    # in the future
    start_date = date.today() + relativedelta(days=10)
    BookingFactory(
        start_date=start_date,
        end_date=start_date+relativedelta(days=5),
    )


@pytest.mark.django_db
def test_get_bookings():
    _demo_data()
    c = HtmlCalendar()
    c._get_bookings()


@pytest.mark.django_db
def test_get_calendars():
    _demo_data()
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
