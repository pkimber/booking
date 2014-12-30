# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import BookingSettings


class BookingSettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(BookingSettings, BookingSettingsAdmin)
