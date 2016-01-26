# -*- encoding: utf-8 -*-
from django import forms

from base.form_utils import (
    RequiredFieldForm,
    set_widget_required,
)

from .models import (
    Booking,
    Category,
    Location,
    Room,
    Rota,
    RotaType,
)


class BookingEmptyForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ()


class BookingDayForm(RequiredFieldForm):
    """
    Form for booking one day at a time.

    Require: 'start_date' and 'title'.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )
        set_widget_required(self.fields['title'])

    class Meta:
        model = Booking
        fields = ('start_date', 'title', 'description')


class BookingEventForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(BookingEventForm, self).__init__(*args, **kwargs)
        for name in ('title', 'description', 'location'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )
        set_widget_required(self.fields['category'])
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
            'title',
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


class BookingNotesStaffForm(RequiredFieldForm):
    """
    Notes for members of staff.

    This form will only be used if 'booking.BookingSettings.notes_user_staff'
    is set to 'True'.

    """

    def __init__(self, *args, **kwargs):
        super(BookingNotesStaffForm, self).__init__(*args, **kwargs)
        self.fields['notes_staff'].widget.attrs.update(
            {'class': 'pure-input-2-3'}
        )

    class Meta:
        model = Booking
        fields = (
            'notes_staff',
        )


class BookingNotesUserForm(RequiredFieldForm):
    """
    Notes for logged in users.

    This form will only be used if 'booking.BookingSettings.notes_user_staff'
    is set to 'True'.

    """

    def __init__(self, *args, **kwargs):
        super(BookingNotesUserForm, self).__init__(*args, **kwargs)
        self.fields['notes_user'].widget.attrs.update(
            {'class': 'pure-input-2-3'}
        )

    class Meta:
        model = Booking
        fields = (
            'notes_user',
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
            'per_day_booking',
        )


class LocationForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        for name in ('title', 'address', 'url', 'url_map', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Location
        fields = (
            'title',
            'address',
            'url',
            'url_map',
            'description',
            'picture',
        )

class RoomForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Room
        fields = (
            'title',
            'description',
            'picture',
        )


class RotaEmptyForm(forms.ModelForm):

    class Meta:
        model = Rota
        fields = ()


class RotaForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(RotaForm, self).__init__(*args, **kwargs)
        for name in ('rota', 'name',):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Rota
        fields = (
            'rota',
            'name',
        )


class RotaTypeForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(RotaTypeForm, self).__init__(*args, **kwargs)
        for name in ('name',):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = RotaType
        fields = (
            'name',
            'order',
        )
