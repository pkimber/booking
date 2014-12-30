# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import (
    patterns,
    url,
)

from .views_event import (
    EventCreateView,
    #EventListView,
    EventUpdateNotesView,
    EventUpdateView,
    #PermissionCreateView,
    #PermissionListView,
    #PermissionUpdateView,
    #StatusCreateView,
    #StatusListView,
    #StatusUpdateView,
)


urlpatterns = patterns(
    '',
    #url(regex=r'^event/$',
    #    view=EventListView.as_view(),
    #    name='event.list'
    #    ),
    url(regex=r'^event/create/$',
        view=EventCreateView.as_view(),
        name='event.create'
        ),
    url(regex=r'^event/(?P<pk>\d+)/update/$',
        view=EventUpdateView.as_view(),
        name='event.update'
        ),
    #url(regex=r'^permission/$',
    #    view=PermissionListView.as_view(),
    #    name='event.permission.list'
    #    ),
    #url(regex=r'^permission/create/$',
    #    view=PermissionCreateView.as_view(),
    #    name='event.permission.create'
    #    ),
    #url(regex=r'^permission/(?P<pk>\d+)/update/$',
    #    view=PermissionUpdateView.as_view(),
    #    name='event.permission.update'
    #    ),
    #url(regex=r'^status/$',
    #    view=StatusListView.as_view(),
    #    name='event.status.list'
    #    ),
    #url(regex=r'^status/create/$',
    #    view=StatusCreateView.as_view(),
    #    name='event.status.create'
    #    ),
    #url(regex=r'^status/(?P<pk>\d+)/update/$',
    #    view=StatusUpdateView.as_view(),
    #    name='event.status.update'
    #    ),
)
