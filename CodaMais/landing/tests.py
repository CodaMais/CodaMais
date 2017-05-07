from django.test import TestCase
from django.test.client import RequestFactory

from user.models import User
from landing.views import home


class LandingViewTest(TestCase):
    user = User()
    email = "user@user.com"
    wrong_email = "useruser.com"
    password = "userpassword"
    first_name = "TestUser"
    username = "Username"
    factory = RequestFactory()

    # This will happen when user is already logged.
    def test_if_landing_page_is_not_showing(self):
        request = self.factory.get('/')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 302)
