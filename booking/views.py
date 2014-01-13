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

from .forms import BookingForm
from .models import Booking
from base.view_utils import BaseMixin


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

    def get_queryset(self):
        d = self._get_date()
        return Booking.objects.month(d.month, d.year)
        #return Booking.objects.filter(
        #    (Q(from_date__month=d.month) & Q(from_date__year=d.year))
        #    |
        #    (Q(to_date__month=d.month) & Q(to_date__year=d.year))
        #)


class BookingUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = BookingForm
    model = Booking

    def get_success_url(self):
        return reverse('booking.list')
