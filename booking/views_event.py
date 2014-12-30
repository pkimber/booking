# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from base.view_utils import BaseMixin

from .forms_event import (
    EventForm,
    EventNotesForm,
)
from .models import Booking



class EventCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = EventForm
    model = Booking

    def get_success_url(self):
        return reverse('booking.list')


#class EventListView(
#        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):
#
#    model = Booking


class EventUpdateNotesView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = EventNotesForm
    model = Booking
    template_name = 'booking/booking_notes_form.html'

    #def get_context_data(self, **kwargs):
    #    context = super(EventUpdateNotesView, self).get_context_data(**kwargs)
    #    context.update(dict(
    #        event=self.object,
    #    ))
    #    return context

    def get_success_url(self):
        return reverse('booking.list')


class EventUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = EventForm
    model = Booking

    def get_success_url(self):
        return reverse('booking.list')


#class PermissionCreateView(
#        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):
#
#    form_class = PermissionForm
#    model = Permission
#
#    def get_success_url(self):
#        return reverse('event.permission.list')
#
#
#class PermissionListView(
#        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):
#
#    model = Permission
#
#
#class PermissionUpdateView(
#        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):
#
#    form_class = PermissionForm
#    model = Permission
#
#    def get_success_url(self):
#        return reverse('event.permission.list')


#class StatusCreateView(
#        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):
#
#    form_class = StatusForm
#    model = Status
#
#    def get_success_url(self):
#        return reverse('event.status.list')
#
#
#class StatusListView(
#        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):
#
#    model = Status
#    #template_name = 'dash/event_status.html'
#
#
#class StatusUpdateView(
#        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):
#
#    form_class = StatusForm
#    model = Status
#
#    def get_success_url(self):
#        return reverse('event.status.list')