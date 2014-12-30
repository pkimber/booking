# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import (
    patterns,
    url,
)

from .views import (
    BookingCreateView,
    BookingDeleteView,
    BookingListMonthView,
    BookingListView,
    BookingUpdateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^add/$',
        view=BookingCreateView.as_view(),
        name='booking.create'
        ),
    url(regex=r'^$',
        view=BookingListView.as_view(),
        name='booking.list'
        ),
    url(regex=r'^(?P<pk>\d+)/delete/$',
        view=BookingDeleteView.as_view(),
        name='booking.delete'
        ),
    url(regex=r'^(?P<pk>\d+)/update/$',
        view=BookingUpdateView.as_view(),
        name='booking.update'
        ),
    url(regex=r'^(?P<year>\d{4})/(?P<month>\d+)/$',
        view=BookingListMonthView.as_view(),
        name='booking.list.month'
        ),
)
