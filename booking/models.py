# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils import timezone

import reversion

from base.model_utils import TimeStampedModel


class Category(TimeStampedModel):

    description = models.CharField(max_length=200)
    promote = models.BooleanField(default=False)
    routine = models.BooleanField(default=True)

    class Meta:
        ordering = ('description',)
        verbose_name = 'Event type'
        verbose_name_plural = 'Event types'

    def __str__(self):
        return '{}'.format(self.description)

reversion.register(Category)


class Location(TimeStampedModel):

    description = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    url_map = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('description',)
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return '{}'.format(self.description)

reversion.register(Location)


class PermissionManager(models.Manager):

    def create_permission(self, slug, description):
        permission = self.model(
            slug=slug,
            description=description,
        )
        permission.save()
        return permission

    def init_permission(self, slug, description):
        try:
            permission = self.model.objects.get(slug=slug)
            permission.description = description
            permission.save()
        except self.model.DoesNotExist:
            permission = self.create_permission(slug, description)
        return permission


class Permission(TimeStampedModel):

    PUBLIC = 'public'
    STAFF = 'staff'
    USER = 'user'

    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=200)
    objects = PermissionManager()

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

    def __str__(self):
        return '{}'.format(self.description)

reversion.register(Permission)


class BookingManager(models.Manager):

    def _eight_months(self):
        today = timezone.now().date()
        return today + relativedelta(months=8)

    def _two_months(self):
        today = timezone.now().date()
        return today + relativedelta(months=2)

    def _public(self):
        return self.model.objects.filter(
            permission__slug=Permission.PUBLIC,
            #status__publish=True,
        ).exclude(
            deleted=True
        )

    def bookings(self):
        """Return a list of booking objects starting with this month.

        If the to date is in this month, then include the booking.

        """
        first = timezone.now().date() + relativedelta(day=1)
        return self.model.objects.filter(to_date__gte=first)

    def calendar(self, from_date, to_date):
        """Return a list of booking objects starting with this month.

        If the to date is in this month, then include the booking.

        """
        return self.model.objects.filter(
            to_date__gte=from_date,
            from_date__lte=to_date,
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

    def public_calendar(self):
        return self._public().filter(
            from_date__gte=timezone.now().date(),
            from_date__lte=self._two_months(),
        )

    def public_promoted(self):
        return self._public().filter(
            from_date__gt=self._two_months(),
            from_date__lte=self._eight_months(),
            category__promote=True,
        )


class Booking(TimeStampedModel):

    permission= models.ForeignKey(Permission, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)
    from_date = models.DateField(help_text='(dd/mm/yyyy)')
    from_time = models.TimeField(
        blank=True, null=True,
        help_text="Please enter in 24 hour format e.g. 19:00",
    )
    to_date = models.DateField(
        blank=True, null=True,
        help_text='(dd/mm/yyyy)'
    )
    to_time = models.TimeField(
        blank=True, null=True,
        help_text="Please enter in 24 hour format e.g. 21:00",
    )
    location = models.ForeignKey(Location, blank=True, null=True)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to='booking', blank=True)
    notes_user = models.TextField(blank=True)
    notes_staff = models.TextField(blank=True)
    deleted = models.BooleanField(default=False)
    objects = BookingManager()

    class Meta:
        ordering = ('from_date', 'from_time')
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        end = ''
        if self.to_date:
            end = '-{}'.format(self.to_date.strftime("%a %d %b %Y"))
        return '{}{}: {}'.format(
            self.from_date.strftime("%a %d %b %Y"), end, self.title)

    def _is_in_the_past(self):
        return self.to_date < timezone.now().date()

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
