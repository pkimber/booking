from datetime import (
    datetime,
    timedelta,
)


def first_next_month(d):
    first = datetime(d.year, d.month, 1).date()
    next_month = first + timedelta(days=40)
    return datetime(next_month.year, next_month.month, 1).date()


def first_prev_month(d):
    first = datetime(d.year, d.month, 1).date()
    last_month = first - timedelta(days=7)
    return datetime(last_month.year, last_month.month, 1).date()


def first_this_month(d):
    return datetime(d.year, d.month, 1).date()
