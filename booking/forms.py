# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from base.form_utils import (
    RequiredFieldForm,
    set_widget_required,
)

from .models import Booking


class BookingEmptyForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ()


class BookingForm(RequiredFieldForm):
    """
    Form for booking a self-catering cottage.

    Require: 'start_date', 'end_date' and 'title'.

    """

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )
        set_widget_required(self.fields['title'])
        set_widget_required(self.fields['end_date'])

    class Meta:
        model = Booking
        fields = ('start_date', 'end_date', 'title', 'description')
