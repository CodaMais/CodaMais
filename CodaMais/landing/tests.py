from django.test import TestCase
from django.test.client import RequestFactory

from landing.views import home


class LandingViewTest(TestCase):
    factory = RequestFactory()

    def test_if_landing_page_is_showing(self):
        request = self.factory.get('/')
        response = home(request)
        self.assertEqual(response.status_code, 200)
