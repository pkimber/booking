from datetime import datetime

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
)
from django.views.generic.dates import MonthArchiveView

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from base.view_utils import BaseMixin

from .forms import BookingForm
from .models import Booking
from .service import (
    first_next_month,
    first_prev_month,
    first_this_month,
)


class BookingCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = BookingForm
    model = Booking

    def get_success_url(self):
        return reverse('booking.list')



class BookingListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Booking


class BookingListMonthView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Booking

    def _get_date(self):
        month = int(self.kwargs.get('month', 0))
        year = int(self.kwargs.get('year', 0))
        try:
            return datetime(year, month, 1).date()
        except ValueError:
            raise Http404("Invalid date.")

    def get_context_data(self, **kwargs):
        context = super(BookingListMonthView, self).get_context_data(**kwargs)
        d = self._get_date()
        today = datetime.today().date()
        is_current_month = d.month == today.month and d.year == today.year
        context.update(dict(
            first_this_month=first_this_month(d),
            first_next_month=first_next_month(d),
            first_prev_month=first_prev_month(d),
            is_current_month=is_current_month,
            today=first_this_month(today),
        ))
        return context

    def get_queryset(self):
        d = self._get_date()
        return Booking.objects.month(d.month, d.year)


class BookingUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = BookingForm
    model = Booking

    def get_success_url(self):
        return reverse('booking.list')
