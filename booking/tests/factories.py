# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory
from django.utils import timezone

from booking.models import (
    Booking,
    Category,
    Location,
    Permission,
)


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category


class LocationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Location


class PermissionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Permission


class BookingFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Booking

    category = factory.SubFactory(CategoryFactory)
    location = factory.SubFactory(LocationFactory)
    permission = factory.SubFactory(PermissionFactory)
    from_date = timezone.now().date()
