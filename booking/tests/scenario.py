# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import (
    datetime,
    timedelta,
)

from dateutil.relativedelta import relativedelta

from base.tests.model_maker import clean_and_save
from booking.models import (
    Booking,
    Category,
    Location,
)


def get_alpe_d_huez():
    return Booking.objects.get(title='Alpe D Huez')


def make_booking(start_date, end_date, title, **kwargs):
    defaults = dict(
        start_date=start_date,
        end_date=end_date,
        title=title,
    )
    defaults.update(kwargs)
    return clean_and_save(Booking(**defaults))


def make_booking_in_past(start_date, end_date, title):
    """Save a booking without cleaning (validating) the data."""
    b = Booking(**dict(
        start_date=start_date,
        end_date=end_date,
        title=title,
    ))
    b.save()
    return b


def next_weekday(d, weekday):
    """Find the date for the next weekday.

    Copied from:
    http://stackoverflow.com/questions/6558535/python-find-the-date-for-the-first-monday-after-a-given-a-date

    """
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)


def demo_data():
    # set-up some dates
    today = datetime.today().date()
    # 1st week last month starting Saturday
    first_prev_month = today + relativedelta(months=-1, day=1)
    start_date = next_weekday(first_prev_month, 5)
    end_date = start_date + timedelta(days=7)
    make_booking_in_past(start_date, end_date, 'Tignes')
    # 2nd week last month
    make_booking_in_past(end_date, end_date + timedelta(days=7), 'Meribel')
    # 1st week this month starting Saturday
    first_this_month = today + relativedelta(day=1)
    start_date = next_weekday(first_this_month, 5)
    make_booking_in_past(start_date, start_date + timedelta(days=3), 'Whistler')
    # later this month starting Tuesday
    start_date = next_weekday(first_this_month + timedelta(days=10), 1)
    make_booking_in_past(start_date, start_date + timedelta(days=3), 'Dorset')
    # span this and next month
    start_date = datetime(today.year, today.month, 27).date()
    first_next_month = today + relativedelta(months=+1, day=1)
    end_date = datetime(first_next_month.year, first_next_month.month, 2).date()
    make_booking_in_past(start_date, end_date, 'Devon')
    # next month
    start_date = next_weekday(first_next_month + timedelta(days=3), 2)
    end_date = next_weekday(start_date, 5)
    make_booking(start_date, end_date, 'Alpe D Huez')
    make_booking(end_date, end_date + timedelta(days=4), 'Cornwall')
    # misc
    Category.objects.create_category('Meeting')
    Location.objects.create_location('Community Centre')
