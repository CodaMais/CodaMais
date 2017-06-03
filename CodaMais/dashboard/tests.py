# Django
from django.test import TestCase
from django.test.client import RequestFactory

# local Django
from user.models import (
    User,
)
from dashboard.views import dashboard

# RESPONSE CODES.
REQUEST_SUCCEEDED = 200  # 200 is return with success response.


class DashboardViewTest(TestCase):
    user = User()

    def setUp(self):
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.user.set_password('userpassword')
        self.user.save()
        self.factory = RequestFactory()

    def test_show_dashboard(self):
        request = self.factory.get('/dashboard/dashboard')
        request.user = self.user
        response = dashboard(request)
        self.assertEqual(response.status_code, REQUEST_SUCCEEDED)
