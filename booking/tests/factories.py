# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import factory

from django.utils import timezone

from booking.models import (
    Booking,
    Category,
    Location,
)


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category


class LocationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Location


class BookingFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Booking

    category = factory.SubFactory(CategoryFactory)
    location = factory.SubFactory(LocationFactory)
    start_date = timezone.now().date()
