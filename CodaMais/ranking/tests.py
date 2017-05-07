# Django
from django.test import TestCase
from django.test.client import RequestFactory

# local Django
from user.models import (
    User,
)
from .views import (
    show_ranking,
)

# RESPONSE CODES.
REQUEST_SUCCEEDED = 200  # 200 is return with success response.

# 302 is the value returned from a HttpRequest status code when the URL was redirected.
REQUEST_REDIRECT = 302


class RankingViewTest(TestCase):
    user = User()

    def setUp(self):
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.user.set_password('userpassword')
        self.user.save()
        self.factory = RequestFactory()

    def test_show_ranking(self):
        request = self.factory.get('/ranking/ranking/')
        request.user = self.user
        response = show_ranking(request)
        self.assertEqual(response.status_code, REQUEST_SUCCEEDED)
