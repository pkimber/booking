# -*- encoding: utf-8 -*-
import factory

from django.utils import timezone

from booking.models import (
    Booking,
    Category,
    Location,
    Rota,
    RotaType,
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


class RotaTypeFactory(factory.django.DjangoModelFactory):

    @factory.sequence
    def order(n):
        return n

    class Meta:
        model = RotaType


class RotaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Rota

    booking = factory.SubFactory(BookingFactory)
    rota = factory.SubFactory(RotaTypeFactory)

    @factory.sequence
    def name(n):
        return 'name_{:02d}'.format(n)
