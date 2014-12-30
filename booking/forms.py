# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from base.form_utils import (
    RequiredFieldForm,
    set_widget_required,
)

from .models import (
    Booking,
    Category,
    Location,
)


class BookingEmptyForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ()


class BookingEventForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(BookingEventForm, self).__init__(*args, **kwargs)
        for name in ('description', 'location'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )
        set_widget_required(self.fields['location'])
        set_widget_required(self.fields['permission'])

    class Meta:
        model = Booking
        fields = (
            'permission',
            'category',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'description',
            'location',
            'picture',
        )


class BookingForm(RequiredFieldForm):
    """
    Form for simple booking e.g. self-catering cottage.

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


class BookingNotesForm(RequiredFieldForm):
    """
    Notes for logged in users and members of staff.

    This form will only be used if 'booking.BookingSettings.notes_user_staff'
    is set to 'True'.

    """

    def __init__(self, *args, **kwargs):
        super(BookingNotesForm, self).__init__(*args, **kwargs)
        for name in ('notes_user', 'notes_staff'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Booking
        fields = (
            'notes_user',
            'notes_staff',
        )


class CategoryForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for name in ('description',):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Category
        fields = (
            'description',
            'promote',
            'routine',
        )


class LocationForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        for name in ('description', 'url', 'url_map', 'notes'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Location
        fields = (
            'description',
            'url',
            'url_map',
            'notes',
        )
