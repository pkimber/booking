# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

import reversion

from base.model_utils import TimeStampedModel
from base.singleton import SingletonModel


def default_permission():
    return Permission.objects.get(slug=Permission.PUBLIC).pk


class BookingSettings(SingletonModel):

    display_permissions = models.BooleanField(
        default=False,
        help_text="Display permissions on the list of bookings."
    )
    notes_user_staff = models.BooleanField(
        default=False,
        help_text=(
            "Allow a member of staff to edit notes for logged "
            "in users (and members of staff)"
        )
    )

    class Meta:
        verbose_name = 'Booking settings'

    def __str__(self):
        return "Booking settings (permissions: {}, notes: {})".format(
            self.display_permissions,
            self.notes_user_staff,
        )

reversion.register(BookingSettings)


class CategoryManager(models.Manager):

    def create_category(self, description):
        category = self.model(
            description=description,
        )
        category.save()
        return category


class Category(TimeStampedModel):

    description = models.CharField(max_length=200)
    promote = models.BooleanField(default=False)
    routine = models.BooleanField(default=True)
    objects = CategoryManager()

    class Meta:
        ordering = ('description',)
        verbose_name = 'Event type'
        verbose_name_plural = 'Event types'

    def __str__(self):
        return '{}'.format(self.description)

reversion.register(Category)


class LocationManager(models.Manager):

    def create_location(self, description):
        location = self.model(
            description=description,
        )
        location.save()
        return location


class Location(TimeStampedModel):

    title = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    url = models.URLField(blank=True, null=True)
    url_map = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to='booking', blank=True)
    objects = LocationManager()

    class Meta:
        ordering = ('description',)
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return '{}'.format(self.title)

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

    def _current(self):
        """Return all current bookings."""
        return self.model.objects.exclude(deleted=True)

    def _eight_months(self):
        today = timezone.now().date()
        return today + relativedelta(months=8)

    def _filter_by_date(self, qs, start_date, end_date):
        """
        Filter booking objects which are in this date ranage.

        If the start date or end date are in the range, then include them.

        """
        return qs.filter(
            (Q(start_date__gte=start_date) & Q(start_date__lte=end_date))
            |
            (Q(end_date__lte=end_date) & Q(end_date__gte=start_date))
        )

    def _filter_by_month(self, qs, month, year):
        """
        Find booking objects which are in the month.

        If the start date or end date are in the month, then include them.

        """
        return qs.filter(
            (Q(start_date__month=month) & Q(start_date__year=year))
            |
            (Q(end_date__month=month) & Q(end_date__year=year))
        )

    def _two_months(self):
        today = timezone.now().date()
        return today + relativedelta(months=2)

    def _public(self):
        return self._current().filter(
            permission__slug=Permission.PUBLIC,
            #status__publish=True,
        )

    def _user(self):
        return self._current().filter(
            permission__slug__in=(Permission.PUBLIC, Permission.USER),
        )

    def public_calendar(self):
        return self._filter_by_date(
            self._public(), timezone.now().date(), self._two_months()
        )

    def public_calendar_widget(self, start_date, end_date):
        return self._filter_by_date(self._public(), start_date,end_date)

    def public_month(self, month, year):
        """Public bookings for this month."""
        return self._filter_by_month(self._public(), month, year)

    def public_promoted(self):
        return self._public().filter(
            start_date__gt=self._two_months(),
            start_date__lte=self._eight_months(),
            category__promote=True,
        )

    def user_calendar(self):
        return self._filter_by_date(
            self._user(), timezone.now().date(), self._two_months()
        )

    def user_month(self, month, year):
        return self._filter_by_month(self._user(), month, year)

    def staff_calendar(self):
        return self._filter_by_date(
            self._current(), timezone.now().date(), self._two_months()
        )

    def staff_month(self, month, year):
        return self._filter_by_month(self._current(), month, year)


class Booking(TimeStampedModel):

    permission= models.ForeignKey(Permission, default=default_permission)
    category = models.ForeignKey(Category, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(help_text='(dd/mm/yyyy)')
    start_time = models.TimeField(
        blank=True, null=True,
        help_text="Please enter in 24 hour format e.g. 19:00",
    )
    end_date = models.DateField(
        blank=True, null=True,
        help_text='(dd/mm/yyyy)'
    )
    end_time = models.TimeField(
        blank=True, null=True,
        help_text="Please enter in 24 hour format e.g. 21:00",
    )
    location = models.ForeignKey(Location, blank=True, null=True)
    description = models.TextField(blank=True)
    picture = models.ImageField(upload_to='booking', blank=True)
    notes_user = models.TextField(
        blank=True,
        help_text="Notes for your users who are logged into the site.",
    )
    notes_staff = models.TextField(
        blank=True,
        help_text="Notes for members of staff.",
    )
    deleted = models.BooleanField(default=False)
    objects = BookingManager()

    class Meta:
        ordering = ('start_date', 'start_time')
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        end = ''
        if self.end_date:
            end = '-{}'.format(self.end_date.strftime("%a %d %b %Y"))
        return '{}{}: {}'.format(
            self.start_date.strftime("%a %d %b %Y"), end, self.title)

    def _is_in_the_past(self):
        return self.end_date and self.end_date < timezone.now().date()

    def clean(self):
        if self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError(
                    'A booking cannot end before it has started.'
                )
            if self.start_date == self.end_date:
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
