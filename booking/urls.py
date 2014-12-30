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
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    LocationCreateView,
    LocationListView,
    LocationUpdateView,
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
    url(regex=r'^category/$',
        view=CategoryListView.as_view(),
        name='booking.category.list'
        ),
    url(regex=r'^category/create/$',
        view=CategoryCreateView.as_view(),
        name='booking.category.create'
        ),
    url(regex=r'^category/(?P<pk>\d+)/update/$',
        view=CategoryUpdateView.as_view(),
        name='booking.category.update'
        ),
    url(regex=r'^location/$',
        view=LocationListView.as_view(),
        name='booking.location.list'
        ),
    url(regex=r'^location/create/$',
        view=LocationCreateView.as_view(),
        name='booking.location.create'
        ),
    url(regex=r'^location/(?P<pk>\d+)/update/$',
        view=LocationUpdateView.as_view(),
        name='booking.location.update'
        ),
)
