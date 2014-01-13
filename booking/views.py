from django.core.urlresolvers import reverse
from django.views.generic import (
    CreateView,
    ListView,
)

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



class BookingListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):

    model = Booking
