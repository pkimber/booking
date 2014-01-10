from django.conf.urls import (
    patterns, url
)

from .views import (
    BookingListView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=BookingListView.as_view(),
        name='booking.list'
        ),
)
