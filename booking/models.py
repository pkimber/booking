from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models

import reversion

from base.model_utils import TimeStampedModel


class Booking(TimeStampedModel):
    from_date = models.DateField(help_text="(dd/mm/yyyy)")
    to_date = models.DateField(help_text="(dd/mm/yyyy)")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['from_date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __unicode__(self):
        return unicode('{}-{}: {}'.format(
            self.from_date.strftime("%a %d %b %Y"),
            self.to_date.strftime("%a %d %b %Y"),
            self.title,
        ))

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

    def can_update(self):
        return not self._is_in_the_past()

reversion.register(Booking)
