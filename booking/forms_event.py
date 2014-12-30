# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from base.form_utils import RequiredFieldForm

from .models import (
    Booking,
    Category,
    Location,
)


class EventForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for name in ('description', 'location'): #, 'notes_public'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Booking
        fields = (
            'permission',
            #'status',
            'category',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'description',
            'location',
            #'notes_public',
            #'notes_user',
            #'notes_staff',
        )


class EventNotesForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(EventNotesForm, self).__init__(*args, **kwargs)
        for name in ('notes_user', 'notes_staff'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = Booking
        fields = (
            #'notes_public',
            'notes_user',
            'notes_staff',
        )

#class StatusForm(RequiredFieldForm):
#
#    def __init__(self, *args, **kwargs):
#        super(StatusForm, self).__init__(*args, **kwargs)
#        for name in ('description',):
#            self.fields[name].widget.attrs.update(
#                {'class': 'pure-input-2-3'}
#            )
#
#    class Meta:
#        model = Status
#        fields = (
#            'description',
#            'publish',
#        )