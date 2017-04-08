# Django.
from django.test import TestCase
from django.test.client import RequestFactory

# Local Django.
from theory.views import list_all_theories, show_theory
from theory.models import Theory
from . import constants


class TestTheoryRegistration(TestCase):

    theory = Theory()

    def setUp(self):
        self.theory.title = 'Vector'
        self.theory.content = '<p>Theory about Vector.</p>'

    def test_str_is_correct(self):
        self.theory.save()
        theory_data = theory_data = Theory.objects.get(id=self.theory.id)
        self.assertEqual(str(theory_data), str(self.theory))


class TestRequestRegistration(TestCase):

    theory = Theory()

    def setUp(self):
        self.theory.title = 'Vector'
        self.theory.content = '<p>Theory about Vector.</p>'
        self.factory = RequestFactory()

    def test_list_all_theories(self):
        request = self.factory.get('/theory/')
        response = list_all_theories(request)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)

    def test_show_theory(self):
        self.theory.save()
        request = self.factory.get('/theory/')
        response = show_theory(request, self.theory.id, self.theory.title)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)
