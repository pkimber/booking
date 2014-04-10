# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.views.generic import TemplateView

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
            calendar=list(grouped),
        ))
        return context
