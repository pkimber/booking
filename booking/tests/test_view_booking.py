from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase
from booking.models import Booking
from booking.tests.scenario import default_scenario_booking
from login.tests.scenario import default_scenario_login


class TestViewStory(PermTestCase):

    def setUp(self):
        default_scenario_login()
        default_scenario_booking()

    def test_list_perm(self):
        self.assert_staff_only(reverse('booking.list'))
