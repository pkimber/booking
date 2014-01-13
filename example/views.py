from django.views.generic import TemplateView

from booking.service import (
    get_calendars,
    grouper,
)


class HomeView(TemplateView):

    template_name = 'example/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        calendars = get_calendars()
        grouped = grouper(calendars, 3)
        context.update(dict(
            calendar=list(grouped),
        ))
        return context
