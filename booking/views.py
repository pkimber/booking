# -*- encoding: utf-8 -*-
from datetime import datetime

from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import (
    Http404,
    HttpResponse,
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
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
    BookingNotesStaffForm,
    BookingNotesUserForm,
    CategoryForm,
    LocationForm,
    RoomForm,
    RotaEmptyForm,
    RotaForm,
    RotaTypeForm,
)
from .models import (
    Booking,
    BookingSettings,
    Category,
    Location,
    Room,
    Rota,
    RotaType,
)
from .service import (
    grouper,
    HtmlCalendar,
    PdfCalendar,
)


def _url_booking(booking):
    """If we are editing from the detail form."""
    if BookingSettings.load().edit_from_detail:
        return reverse('booking.detail', args=[booking.pk])
    else:
        return _url_booking_list_month(booking)


def _url_booking_list_month(booking):
    return reverse(
        'booking.list.month',
        kwargs=dict(
            year=booking.start_date.year,
            month=booking.start_date.month
        )
    )


class BookingCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    model = Booking

    def get_success_url(self):
        return _url_booking(self.object)


class BookingDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, DeleteView):

    model = Booking

    def delete(self, request, *args, **kwargs):
        result = super(BookingDeleteView, self).delete(request, *args, **kwargs)
        end_date = ''
        if self.object.end_date:
            end_date = ' to {}, '.format(
                self.object.end_date.strftime('%d/%m/%Y')
            )
        messages.info(
            self.request,
            "Deleted booking from {}{} {}".format(
                self.object.start_date.strftime('%d/%m/%Y'),
                end_date,
                self.object.title,
            )
        )
        return result

    def get_success_url(self):
        return reverse('booking.list')


class BookingDetailView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, DetailView):

    model = Booking

    def get_context_data(self, **kwargs):
        context = super(BookingDetailView, self).get_context_data(**kwargs)
        context.update(dict(
            booking_settings=BookingSettings.load(),
        ))
        return context


class BookingListMixin(LoginRequiredMixin, BaseMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            booking_settings=BookingSettings.load(),
        ))
        return context


class BookingListMonthMixin(BookingListMixin):

    def _get_date(self):
        month = int(self.kwargs.get('month', 0))
        year = int(self.kwargs.get('year', 0))
        try:
            return datetime(year, month, 1).date()
        except ValueError:
            raise Http404("Invalid date.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        return Booking.objects.month(self.request.user, d.month, d.year)


class BookingListTodayMixin(BookingListMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today().date()
        first_next_month = today + relativedelta(months=+1, day=1)
        first_prev_month = today + relativedelta(months=-1, day=1)
        context.update(dict(
            first_next_month=first_next_month,
            first_prev_month=first_prev_month,
            display_today=True,
            sub_heading="Home",
        ))
        return context

    def get_queryset(self):
        return Booking.objects.calendar(self.request.user)


class BookingListView(BookingListTodayMixin):

    def get_context_data(self, **kwargs):
        context = super(BookingListView, self).get_context_data(**kwargs)
        context.update(dict(
            booking_edit=True,
        ))
        return context

    model = Booking


class BookingListMonthView(BookingListMonthMixin):

    model = Booking

    def get_context_data(self, **kwargs):
        context = super(BookingListMonthView, self).get_context_data(**kwargs)
        context.update(dict(
            booking_edit=True,
        ))
        return context


class BookingUpdateNotesStaffView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = BookingNotesStaffForm
    model = Booking
    template_name = 'booking/booking_notes_form.html'

    def get_success_url(self):
        return _url_booking(self.object)


class BookingUpdateNotesUserView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = BookingNotesUserForm
    model = Booking
    template_name = 'booking/booking_notes_form.html'

    def get_success_url(self):
        return _url_booking(self.object)


class BookingUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    model = Booking

    def get_success_url(self):
        return _url_booking(self.object)


class CalendarMixin(object):

    def get_month_count(self):
        try:
            result = self.month_count
        except AttributeError:
            result = None
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendars = HtmlCalendar().get_calendars(count=self.get_month_count())
        grouped = grouper(calendars, 3)
        context.update(dict(
            calendar=list(grouped),
        ))
        return context


class CategoryCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = CategoryForm
    model = Category

    def get_success_url(self):
        return reverse('booking.category.list')


class CategoryListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Category


class CategoryUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = CategoryForm
    model = Category

    def get_success_url(self):
        return reverse('booking.category.list')


def _get_response(file_name):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
    return response


@login_required
def download_calendar(request):
    response = _get_response('calendar.pdf')
    PdfCalendar().report(response, request.user)
    return response


class LocationCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = LocationForm
    model = Location

    def get_success_url(self):
        return reverse('booking.location.list')


class LocationDetailView(BaseMixin, DetailView):

    model = Location


class LocationListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Location


class LocationUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = LocationForm
    model = Location

    def get_success_url(self):
        return reverse('booking.location.list')


class RoomCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = RoomForm
    model = Room

    def _get_location(self):
        pk = self.kwargs.get('pk', None)
        return Location.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(location=self._get_location()))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.location = self._get_location()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('booking.location', args=[self.object.location.pk])


class RoomDetailView(BaseMixin, DetailView):

    model = Room


class RoomUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = RoomForm
    model = Room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(location=self.object.location))
        return context

    def get_success_url(self):
        return reverse('booking.location', args = [self.object.location.pk])


class RotaCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = RotaForm
    model = Rota

    def _get_booking(self):
        pk = self.kwargs.get('pk', None)
        return Booking.objects.get(pk=pk)

    def get_context_data(self, **kwargs):
        context = super(RotaCreateView, self).get_context_data(**kwargs)
        context.update(dict(booking=self._get_booking()))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.booking = self._get_booking()
        return super(RotaCreateView, self).form_valid(form)

    def get_success_url(self):
        return _url_booking(self.object.booking)


class RotaDeleteView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = RotaEmptyForm
    model = Rota
    template_name = 'booking/rota_remove_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.deleted = True
        return super(RotaDeleteView, self).form_valid(form)

    def get_success_url(self):
        return _url_booking(self.object.booking)


class RotaUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = RotaForm
    model = Rota

    def get_context_data(self, **kwargs):
        context = super(RotaUpdateView, self).get_context_data(**kwargs)
        context.update(dict(booking=self.object.booking))
        return context

    def get_success_url(self):
        return _url_booking(self.object.booking)


class RotaTypeCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = RotaTypeForm
    model = RotaType

    def get_success_url(self):
        return reverse('booking.rota.type.list')


class RotaTypeListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = RotaType


class RotaTypeUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = RotaTypeForm
    model = RotaType

    def get_success_url(self):
        return reverse('booking.rota.type.list')
