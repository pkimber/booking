# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.core.management.base import BaseCommand

from booking.tests.scenario import default_scenario_booking


class Command(BaseCommand):

    help = "Create demo data for 'booking'"

    def handle(self, *args, **options):
        default_scenario_booking()
        print("Created 'booking' demo data...")
