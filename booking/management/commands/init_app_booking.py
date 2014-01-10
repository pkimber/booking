from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Initialise 'booking' application"

    def handle(self, *args, **options):
        print "Initialised 'booking' app..."
