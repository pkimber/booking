# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from base.view_utils import BaseMixin

from .forms import (
    BookingForm,
    BookingNotesForm,
    CategoryForm,
    LocationForm,
)

from .models import (
    Booking,
    BookingSettings,
    Category,
    Location,
)


class BookingCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    model = Booking

    def get_success_url(self):
        return reverse(
            'booking.list.month',
            kwargs=dict(
                year=self.object.start_date.year,
                month=self.object.start_date.month
            )
        )


class BookingDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, DeleteView):

    model = Booking

    def delete(self, request, *args, **kwargs):
        result = super(BookingDeleteView, self).delete(request, *args, **kwargs)
        messages.info(
            self.request,
            "Deleted booking from {} to {}, {}".format(
                self.object.start_date.strftime('%d/%m/%Y'),
                self.object.end_date.strftime('%d/%m/%Y'),
                self.object.title,
            )
        )
        return result

    def get_success_url(self):
        return reverse('booking.list')


class BookingListMixin(LoginRequiredMixin, BaseMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super(BookingListMixin, self).get_context_data(**kwargs)
        context.update(dict(
            booking_settings=BookingSettings.load(),
        ))
        return context


class BookingListView(BookingListMixin):

    model = Booking

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        today = datetime.today().date()
        first_next_month = today + relativedelta(months=+1, day=1)
        first_prev_month = today + relativedelta(months=-1, day=1)
        context.update(dict(
            first_next_month=first_next_month,
            first_prev_month=first_prev_month,
            sub_heading="Home",
        ))
        return context

    def get_queryset(self):
        return Booking.objects.public_calendar()


class BookingListMonthView(BookingListMixin):

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
        first_next_month = d + relativedelta(months=+1, day=1)
        first_prev_month = d + relativedelta(months=-1, day=1)
        context.update(dict(
            first_next_month=first_next_month,
            first_prev_month=first_prev_month,
            sub_heading="Bookings for {}".format(d.strftime("%B %Y"))
        ))
        return context

    def get_queryset(self):
        d = self._get_date()
        return Booking.objects.public_month(d.month, d.year)


class BookingUpdateNotesView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = BookingNotesForm
    model = Booking
    template_name = 'booking/booking_notes_form.html'

    def get_success_url(self):
        return reverse('booking.list')


class BookingUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = BookingForm
    model = Booking

    def get_success_url(self):
        return reverse(
            'booking.list.month',
            kwargs=dict(
                year=self.object.start_date.year,
                month=self.object.start_date.month
            )
        )


class CategoryCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = CategoryForm
    model = Category

    def get_success_url(self):
        return reverse('booking.category.list')


class CategoryListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Category
    #template_name = 'dash/category.html'


class CategoryUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = CategoryForm
    model = Category

    def get_success_url(self):
        return reverse('booking.category.list')


class LocationCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = LocationForm
    model = Location

    def get_success_url(self):
        return reverse('booking.location.list')


class LocationListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Location


class LocationUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = LocationForm
    model = Location

    def get_success_url(self):
        return reverse('booking.location.list')
