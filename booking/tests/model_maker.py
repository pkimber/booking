# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify

from base.tests.model_maker import clean_and_save

from booking.models import Booking


#def make_booking(start_date, end_date, title, **kwargs):
#    defaults = dict(
#        start_date=start_date,
#        end_date=end_date,
#        title=title,
#    )
#    defaults.update(kwargs)
#    return clean_and_save(Booking(**defaults))
