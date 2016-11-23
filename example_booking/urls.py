# -*- encoding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from booking.forms import (
    BookingForm,
    BookingEventForm,
)
from booking.views import (
    BookingCreateView,
    BookingUpdateView,
)

from .views import (
    HomeView,
    SettingsView,
)

admin.autodiscover()


urlpatterns = [
    url(regex=r'^$',
        view=HomeView.as_view(),
        name='project.home'
        ),
    url(regex=r'^',
        view=include('login.urls')
        ),
    url(regex=r'^admin/',
        view=include(admin.site.urls)
        ),
    url(regex=r'^booking/create/$',
        view=BookingCreateView.as_view(form_class=BookingEventForm),
        name='booking.create'
        ),
    url(regex=r'^booking/create/cottage/$',
        view=BookingCreateView.as_view(form_class=BookingForm),
        name='booking.create.cottage'
        ),
    url(regex=r'^booking/(?P<pk>\d+)/update/$',
        view=BookingUpdateView.as_view(form_class=BookingEventForm),
        name='booking.update'
        ),
    url(regex=r'^booking/(?P<pk>\d+)/update/cottage/$',
        view=BookingUpdateView.as_view(form_class=BookingForm),
        name='booking.update.cottage'
        ),
    url(regex=r'^booking/',
        view=include('booking.urls')
        ),
    url(regex=r'^home/user/$',
        view=RedirectView.as_view(url=reverse_lazy('project.home')),
        name='project.dash'
        ),
    url(regex=r'^settings/$',
        view=SettingsView.as_view(),
        name='project.settings'
        ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#   ^ helper function to return a URL pattern for serving files in debug mode.
# https://docs.djangoproject.com/en/1.5/howto/static-files/#serving-files-uploaded-by-a-user

urlpatterns += staticfiles_urlpatterns()
