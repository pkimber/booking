from django.test import TestCase

from booking.management.commands import demo_data_booking
from booking.management.commands import init_app_booking
from login.management.commands import demo_data_login


class TestCommand(TestCase):

    def test_demo_data(self):
        """ Test the management command """
        pre_command = demo_data_login.Command()
        pre_command.handle()
        command = demo_data_booking.Command()
        command.handle()

    def test_init_app(self):
        """ Test the management command """
        command = init_app_booking.Command()
        command.handle()
