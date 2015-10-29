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
    result = c.get_calendars()
    assert list is type(result)
    assert 12 == len(result)


@pytest.mark.django_db
def test_get_calendars_html():
    today = date.today()
    BookingFactory(
        start_date=date(today.year, today.month, 3),
        end_date=date(today.year, today.month, 5),
    )
    c = HtmlCalendar()
    result = c.get_calendars(count=1)
    assert list is type(result)
    assert 1 == len(result)
    html = result[0]
    assert "<td>02</td>" in html
    assert "<td class='afternoon'>03</td>" in html
    assert "<td class='booked'>04</td>" in html
    assert "<td class='morning'>05</td>" in html
    assert "<td>06</td>" in html


@pytest.mark.django_db
def test_get_calendars_no_end_date_html():
    today = date.today()
    BookingFactory(start_date=date(today.year, today.month, 3))
    c = HtmlCalendar()
    result = c.get_calendars(count=1)
    assert list is type(result)
    assert 1 == len(result)
    html = result[0]
    assert "<td>02</td>" in html
    assert "<td class='booked'>03</td>" in html
    assert "<td>04</td>" in html


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
