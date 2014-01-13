from django.conf.urls import (
    patterns, url
)

from .views import (
    BookingCreateView,
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
    url(regex=r'^(?P<pk>\d+)/update/$',
        view=BookingUpdateView.as_view(),
        name='booking.update'
        ),
)
