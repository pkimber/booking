from django.views.generic import ListView

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from .models import Booking
from base.view_utils import BaseMixin


class BookingListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):

    model = Booking
