# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import bleach
import calendar

from datetime import datetime
from itertools import zip_longest
from reportlab import platypus
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

from dateutil.relativedelta import relativedelta
from dateutil.rrule import (
    rrule,
    DAILY,
)

from django.utils.dateformat import DateFormat
from django.utils import timezone
from django.utils.safestring import mark_safe

from booking.models import (
    Booking,
    BookingSettings,
)


def grouper(iterable, n, fillvalue=None):
    """"Collect data into fixed-length chunks or blocks.

    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx

    From
    http://docs.python.org/2/library/itertools.html#recipes

    """
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


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
        self.start_date = datetime.now().date() + relativedelta(day=1)
        self.end_date = self.start_date + relativedelta(years=+1, days=-1)

    def _get_bookings(self):
        qs = Booking.objects.public_calendar_widget(
            self.start_date, self.end_date
        )
        result = {}
        for b in qs:
            if not b.start_date in result:
                result[b.start_date] = BookingCount()
            result[b.start_date].set_afternoon()
            if not b.end_date in result:
                result[b.end_date] = BookingCount()
            result[b.end_date].set_morning()
            for d in rrule(DAILY, dtstart=b.start_date, until=b.end_date):
                if not d.date() in result:
                    result[d.date()] = BookingCount()
                result[d.date()].increment()
        return result

    def _generate_html(self, d, bookings):
        c = calendar.Calendar(calendar.SATURDAY)
        data = c.monthdatescalendar(d.year, d.month)
        # every month to display with 6 rows so they can be lined up.
        while len(data) < 6:
            data.append([None, None, None, None, None, None, None])
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
                if col and col.month == d.month:
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
                    # the space keeps all the rows the same height
                    html = html + "<td>&nbsp;</td>"
            html = html + "</tr>"
        html = html + "</tbody>"
        html = html + "</table>"
        return html

    def get_calendars(self):
        result = []
        bookings = self._get_bookings()
        d = self.start_date
        for i in range(0, 12):
            html = self._generate_html(d, bookings)
            # move to the 1st day of the next month
            d = d + relativedelta(months=+1, day=1)
            result.append(mark_safe(html))
        return result


class MyReport(object):

    def __init__(self):
        # Use the sample style sheet.
        style_sheet = getSampleStyleSheet()
        self.body = style_sheet["BodyText"]
        self.head_1 = style_sheet["Heading1"]
        self.head_2 = style_sheet["Heading2"]
        self.GRID_LINE_WIDTH = 0.1

    def _bold(self, text):
        return self._para('<b>{}</b>'.format(text))

    def _head_1(self, text):
        return platypus.Paragraph(text, self.head_1)

    def _head_2(self, text):
        return platypus.Paragraph(text, self.head_2)

    def _para(self, text):
        return platypus.Paragraph(text, self.body)


class PdfCalendar(MyReport):

    def report(self, response, user):
        # Create the document template
        doc = platypus.SimpleDocTemplate(
            response,
            title='Calendar',
            pagesize=A4
        )
        # Container for the 'Flowable' objects
        elements = []
        booking_settings = BookingSettings.load()
        if booking_settings.pdf_heading:
            elements.append(self._head_1(booking_settings.pdf_heading))
        elements.append(self._head_2('Calendar'))
        elements.append(platypus.Spacer(1, 12))
        #elements.append(self._table_lines(invoice))
        calendar = self._calendar(user)
        if calendar:
            elements.append(calendar)
        elements.append(self._para(
            'Printed {} by {}'.format(
                timezone.now().strftime('%d/%m/%Y %H:%M'),
                user.username
            )
        ))
        doc.build(elements)

    def _calendar(self, user):
        lines = []
        year = 0
        month = 0
        for b in Booking.objects.calendar(user):
            if b.start_date.year == year and b.start_date.month == month:
                pass
            else:
                lines.append([
                    self._bold(DateFormat(b.start_date).format('F Y')),
                    ''
                ])
                year = b.start_date.year
                month = b.start_date.month
            lines.append([
                self._para(self._booking_date(b)),
                self._description(b)
            ])
        # initial styles
        style = [
            ('GRID', (0, 0), (-1, -1), self.GRID_LINE_WIDTH, colors.gray),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ]
        # column widths
        column_widths = [100, 340]
        # draw the table if there is some data
        result = None
        if lines:
            result = platypus.Table(
                lines,
                colWidths=column_widths,
                style=style,
            )
        return result

    def _booking_date(self, b):
        result = []
        result.append(DateFormat(b.start_date).format('l jS'))
        if b.end_date:
            end_date = DateFormat(b.end_date).format('l jS')
            end_month = ''
            if b.end_date.month != b.start_date.month:
                end_month = ' {}'.format(DateFormat(b.end_date).format('M'))
            result.append('{}{}'.format(end_date, end_month))
        return '<br />'.join(result)

    def _strip_html(self, html):
        """a wrapper for bleach.clean() that strips nearly tags."""
        tags = ['br', 'p']
        attr = {}
        styles = []
        result = bleach.clean(
            html, tags=tags, attributes=attr, styles=styles, strip=True
        )
        result = result.replace('</p>', '<br />')
        result = result.replace('<p>', '')
        return result

    def _description(self, b):
        result = []
        category = ''
        end_time = ''
        location = ''
        start_time = ''
        title = ''
        if b.start_time or b.end_time:
            start_time = '{} '.format(DateFormat(b.start_time).format('g:ia'))
            if b.end_time:
                end_time = '- {} '.format(DateFormat(b.end_time).format('g:ia'))
        if b.title:
            title = '{} '.format(b.title)
        if b.category:
            category = '{} '.format(b.category)
        if b.location:
            location = 'at {} '.format(b.location.title)
        result.append('{}{}{}{}{}'.format(
            start_time, end_time, title, category, location
        ))
        description = [self._para('<br />'.join(result))]
        if b.description:
            description.append(self._para(self._strip_html(b.description)))
        if b.notes_user:
            description.append(self._para(self._strip_html(b.notes_user)))
        rota_list = b.rota()
        if rota_list.count():
            result = []
            for rota in rota_list:
                result.append('<b>{}</b>: {}'.format(rota.rota.name, rota.name))
            description.append(self._para(' '.join(result)))
        return description
