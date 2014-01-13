from datetime import (
    datetime,
    timedelta,
)

from booking.models import Booking
from booking.tests.model_maker import make_booking


def get_alpe_d_huez():
    return Booking.objects.get(title='Alpe D Huez')


def default_scenario_booking():
    today = datetime.today()
    next_week = today + timedelta(days=7)
    make_booking(
        next_week,
        next_week + timedelta(days = 3),
        'Alpe D Huez',
    )
