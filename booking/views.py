from datetime import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.views.generic import (
    CreateView,
    DeleteView,
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
)


class BookingCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = BookingForm
    model = Booking

    def get_success_url(self):
        return reverse('booking.list')


class BookingDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, DeleteView):

    model = Booking

    def delete(self, request, *args, **kwargs):
        result = super(BookingDeleteView, self).delete(request, *args, **kwargs)
        messages.info(
            self.request,
            "Deleted booking from {} to {}, {}".format(
                self.object.from_date.strftime('%d/%m/%Y'),
                self.object.to_date.strftime('%d/%m/%Y'),
                self.object.title,
            )
        )
        return result

    def get_success_url(self):
        return reverse('booking.list')


class BookingListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Booking

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        today = datetime.today().date()
        context.update(dict(
            first_next_month=first_next_month(today),
            first_prev_month=first_prev_month(today),
            sub_heading="Home",
        ))
        return context

    def get_queryset(self):
        """Maximum 31 bookings."""
        return Booking.objects.bookings()[:31]


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
        context.update(dict(
            first_next_month=first_next_month(d),
            first_prev_month=first_prev_month(d),
            sub_heading="Bookings for {}".format(d.strftime("%B %Y"))
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
