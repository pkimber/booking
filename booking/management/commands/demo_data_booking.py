# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from booking.tests.scenario import demo_data


class Command(BaseCommand):

    help = "Create demo data for 'booking'"

    def handle(self, *args, **options):
        demo_data()
        print("Created 'booking' demo data...")
