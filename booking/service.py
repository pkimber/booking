import calendar
from datetime import (
    datetime,
    timedelta,
)
from itertools import izip_longest

from django.utils.safestring import mark_safe


def _add_one_month(dt0):
    """Add one month.

    Copied from:
    http://code.activestate.com/recipes/577274-subtract-or-add-a-month-to-a-datetimedate-or-datet/
    For finding the next month's first you advance to the next month. By adding
    32 days from the first of a month you will always reach the next month.

    """
    dt1 = dt0.replace(day=1)
    dt2 = dt1 + timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3


def _get_month(year, month):
    c = calendar.Calendar(calendar.SATURDAY)
    data = c.monthdatescalendar(year, month)
    html = ""
    #html = html + "<table class='pure-table pure-table-bordered'>"
    html = html + "<table>"
    if data:
        html = html + "<thead>"
        html = html + "<tr>"
        html = html + "<th colspan='7'>{}</th>".format(datetime(year, month, 1).strftime("%B %Y"))
        html = html + "</tr>"
        for row in data:
            html = html + "<tr>"
            for col in row:
                html = html + "<th>{}</th>".format(col.strftime("%a"))
            html = html + "</tr>"
            break
        html = html + "</thead>"
    html = html + "<tbody>"
    for row in data:
        html = html + "<tr>"
        for col in row:
            if col.month == month:
                if col.weekday() == 3:
                    html = html + "<td class='booked'>{}</td>".format(col.strftime("%d"))
                elif col.weekday() == 1:
                    html = html + "<td class='afternoon'>{}</td>".format(col.strftime("%d"))
                elif col.weekday() == 5:
                    html = html + "<td class='morning'>{}</td>".format(col.strftime("%d"))
                else:
                    html = html + "<td>{}</td>".format(col.strftime("%d"))
            else:
                html = html + "<td></td>"
        html = html + "</tr>"
    html = html + "</tbody>"
    html = html + "</table>"
    return html


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


def get_calendars():
    result = []
    today = datetime.now()
    d = datetime(today.year, today.month, 1)
    for i in range(0, 12):
        html = _get_month(d.year, d.month)
        d = _add_one_month(d)
        result.append(mark_safe(html))
    return result


def grouper(iterable, n, fillvalue=None):
    """"Collect data into fixed-length chunks or blocks.

    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx

    From
    http://docs.python.org/2/library/itertools.html#recipes

    """
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)
