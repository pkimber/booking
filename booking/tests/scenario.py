from datetime import (
    datetime,
    timedelta,
)

from booking.models import Booking
from booking.tests.model_maker import make_booking


def default_scenario_booking():
    today = datetime.today()
    next_week = today + timedelta(days=7)
    make_booking(
        next_week,
        next_week + timedelta(days = 3),
        'Three days in the sun',
    )
