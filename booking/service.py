import calendar
from datetime import datetime
from itertools import izip_longest

from dateutil.relativedelta import relativedelta
from dateutil.rrule import (
    rrule,
    DAILY,
)

from django.utils.safestring import mark_safe

from booking.models import Booking


def grouper(iterable, n, fillvalue=None):
    """"Collect data into fixed-length chunks or blocks.

    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx

    From
    http://docs.python.org/2/library/itertools.html#recipes

    """
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


class BookingCount(object):
    """Keep track of booking dates, when they start and end."""

    def __init__(self):
        self.morning = False
        self.afternoon = False
        self.count = 0

    def get_count(self):
        return self.count

    def increment(self):
        self.count = self.count + 1

    def is_all_day(self):
        result = False
        if self.morning and self.afternoon:
            result = True
        elif self.count and not (self.morning or self.afternoon):
            result = True
        return result

    def is_afternoon(self):
        result = False
        if self.morning and self.afternoon:
            pass
        else:
            result = self.afternoon
        return result

    def is_morning(self):
        result = False
        if self.morning and self.afternoon:
            pass
        else:
            result = self.morning
        return result

    def set_afternoon(self):
        self.afternoon = True

    def set_morning(self):
        self.morning = True


class HtmlCalendar(object):

    def __init__(self):
        """From the 1st of this month, for 12 months."""
        self.from_date = datetime.now().date() + relativedelta(day=1)
        self.to_date = self.from_date + relativedelta(years=+1, days=-1)

    def _get_bookings(self):
        qs = Booking.objects.calendar(self.from_date, self.to_date)
        result = {}
        for b in qs:
            if not b.from_date in result:
                result[b.from_date] = BookingCount()
            result[b.from_date].set_afternoon()
            if not b.to_date in result:
                result[b.to_date] = BookingCount()
            result[b.to_date].set_morning()
            for d in rrule(DAILY, dtstart=b.from_date, until=b.to_date):
                if not d.date() in result:
                    result[d.date()] = BookingCount()
                result[d.date()].increment()
        return result

    def _generate_html(self, d, bookings):
        c = calendar.Calendar(calendar.SATURDAY)
        data = c.monthdatescalendar(d.year, d.month)
        html = ""
        html = html + "<table>"
        if data:
            html = html + "<thead>"
            html = html + "<tr>"
            html = html + "<th colspan='7'>{}</th>".format(datetime(d.year, d.month, 1).strftime("%B %Y"))
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
                if col.month == d.month:
                    is_morning = False
                    is_afternoon = False
                    is_all_day = False
                    if col in bookings:
                        is_all_day = bookings[col].is_all_day()
                        is_afternoon = bookings[col].is_afternoon()
                        is_morning = bookings[col].is_morning()
                    if is_all_day:
                        html = html + "<td class='booked'>{}</td>".format(col.strftime("%d"))
                    elif is_afternoon:
                        html = html + "<td class='afternoon'>{}</td>".format(col.strftime("%d"))
                    elif is_morning:
                        html = html + "<td class='morning'>{}</td>".format(col.strftime("%d"))
                    else:
                        html = html + "<td>{}</td>".format(col.strftime("%d"))
                else:
                    html = html + "<td></td>"
            html = html + "</tr>"
        html = html + "</tbody>"
        html = html + "</table>"
        return html

    def get_calendars(self):
        result = []
        bookings = self._get_bookings()
        d = self.from_date
        for i in range(0, 12):
            html = self._generate_html(d, bookings)
            # move to the 1st day of the next month
            d = d + relativedelta(months=+1, day=1)
            result.append(mark_safe(html))
        return result
