# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q

import reversion

from base.model_utils import TimeStampedModel


class BookingManager(models.Manager):

    def bookings(self):
        """Return a list of booking objects starting with this month.

        If the to date is in this month, then include the booking.

        """
        first = datetime.today().date() + relativedelta(day=1)
        return self.model.objects.filter(to_date__gte=first)

    def calendar(self, start_date, end_date):
        """Return a list of booking objects starting with this month.

        If the to date is in this month, then include the booking.

        """
        return self.model.objects.filter(
            to_date__gte=start_date,
            from_date__lte=end_date,
        )

    def month(self, month, year):
        """Return booking objects for a month.

        If the from date or to date are in the month, then include them.

        """
        return self.model.objects.filter(
            (Q(from_date__month=month) & Q(from_date__year=year))
            |
            (Q(to_date__month=month) & Q(to_date__year=year))
        )


class Booking(TimeStampedModel):
    from_date = models.DateField(help_text="(dd/mm/yyyy)")
    to_date = models.DateField(help_text="(dd/mm/yyyy)")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    objects = BookingManager()

    class Meta:
        ordering = ['from_date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return '{}-{}: {}'.format(
            self.from_date.strftime("%a %d %b %Y"),
            self.to_date.strftime("%a %d %b %Y"),
            self.title,
        )

    def _is_in_the_past(self):
        return self.to_date < datetime.today().date()

    def clean(self):
        if self.from_date > self.to_date:
            raise ValidationError(
                'A booking cannot end before it has started.'
            )
        if self.from_date == self.to_date:
            raise ValidationError(
                'A booking cannot start and end on the same day.'
            )
        if self._is_in_the_past():
            raise ValidationError(
                'You cannot make a booking in the past.'
            )

    def is_current(self):
        return not self._is_in_the_past()

reversion.register(Booking)
