# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from booking.models import (
    Booking,
    BookingSettings,
)
from booking.service import (
    grouper,
    HtmlCalendar,
)


class HomeView(TemplateView):

    template_name = 'example/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        calendars = HtmlCalendar().get_calendars()
        grouped = grouper(calendars, 3)
        context.update(dict(
            booking_settings=BookingSettings.load(),
            calendar=list(grouped),
            public_calendar=Booking.objects.public_calendar(),
        ))
        return context
