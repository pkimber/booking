from django import forms

from base.form_utils import RequiredFieldForm

from .models import Booking


class BookingEmptyForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ()


class BookingForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'pure-input-2-3'}
        )
        self.fields['description'].widget.attrs.update(
            {'class': 'pure-input-2-3'}
        )

    class Meta:
        model = Booking
        fields = ('from_date', 'to_date', 'title', 'description')
