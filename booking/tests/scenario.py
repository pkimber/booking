from datetime import (
    datetime,
    timedelta,
)

from booking.models import Booking
from booking.tests.model_maker import make_booking


def get_alpe_d_huez():
    return Booking.objects.get(title='Alpe D Huez')


def make_booking_in_past(from_date, to_date, title):
    """Save a booking without cleaning (validating) the data."""
    b = Booking(**dict(
        from_date=from_date,
        to_date=to_date,
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


def default_scenario_booking():
    # set-up some dates
    today = datetime.today().date()
    first_this_month = datetime(today.year, today.month, 1).date()
    last_month = first_this_month - timedelta(days=7)
    first_last_month = datetime(last_month.year, last_month.month, 1).date()
    next_month = first_this_month + timedelta(days=40)
    first_next_month = datetime(next_month.year, next_month.month, 1).date()
    # 1st week last month starting Saturday
    from_date = next_weekday(first_last_month, 5)
    to_date = from_date + timedelta(days=7)
    make_booking_in_past(from_date, to_date, 'Tignes')
    # 2nd week last month
    make_booking_in_past(to_date, to_date + timedelta(days=7), 'Meribel')
    # 1st week this month starting Saturday
    from_date = next_weekday(first_this_month, 5)
    make_booking_in_past(from_date, from_date + timedelta(days=3), 'Whistler')
    # later this month starting Tuesday
    from_date = next_weekday(first_this_month + timedelta(days=10), 1)
    make_booking_in_past(from_date, from_date + timedelta(days=3), 'Dorset')
    # span this and next month
    from_date = datetime(today.year, today.month, 27).date()
    to_date = datetime(next_month.year, next_month.month, 2).date()
    make_booking_in_past(from_date, to_date, 'Devon')
    # next month
    from_date = next_weekday(first_next_month + timedelta(days=3), 2)
    to_date = next_weekday(from_date, 5)
    make_booking(from_date, to_date, 'Alpe D Huez')
    make_booking(to_date, to_date + timedelta(days=4), 'Cornwall')
