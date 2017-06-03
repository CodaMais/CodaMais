# Django.
from django.test import TestCase
from django.test.client import RequestFactory

# local Django
from theory import (
    constants, views,
)

from exercise.models import (
    Exercise, TestCaseExercise
)

from user.models import User

from theory.models import Theory


class TestTheoryRegistration(TestCase):

    theory = Theory()

    def setUp(self):
        self.theory.title = 'Vector'
        self.theory.content = '<p>Theory about Vector.</p>'

    def test_str_is_correct(self):
        self.theory.save()
        theory_data = Theory.objects.get(id=self.theory.id)
        self.assertEqual(str(theory_data), str(self.theory))


class TestRequestRegistration(TestCase):

    user = User()
    theory = Theory()

    def setUp(self):
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.theory.title = 'Vector'
        self.theory.content = '<p>Theory about Vector.</p>'
        self.factory = RequestFactory()
        self.user.save()

    def test_list_all_theories(self):
        request = self.factory.get('/theory/')
        request.user = self.user
        response = views.list_all_theories(request)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)

    def test_show_theory(self):
        self.theory.save()
        request = self.factory.get('/theory/')
        request.user = self.user
        response = views.show_theory(request, self.theory.id, self.theory.title)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)


class TestExerciseTheory(TestCase):
    theory = Theory()
    exercise = Exercise()
    test_case_exercise = TestCaseExercise()
    user = User()

    def setUp(self):
        self.user.email = "user@user.com"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.exercise.tip = "Exercise tip."
        self.test_case_exercise.input_exercise = "a\n"
        self.test_case_exercise.output_exercise = "B\n"
        self.theory.title = 'Vector'
        self.theory.content = '<p>Theory about Vector.</p>'
        self.factory = RequestFactory()
        self.user.set_password('userpassword')
        self.theory.save()
        self.user.save()

    def test_if_list_of_exercises_in_theory_is_filled(self):
        self.exercise.theory = self.theory
        self.exercise.save()
        self.test_case_exercise.exercise = self.exercise
        self.test_case_exercise.save()

        list_exercises = views.get_exercise_list_in_theory(self.user, self.theory)
        number_exercises = len(list_exercises)
        number_expected = 1

        self.assertEqual(number_expected, number_exercises)

    def test_if_list_of_exercises_in_theory_is_empty(self):
        list_exercises = views.get_exercise_list_in_theory(self.user, self.theory)
        number_exercises = len(list_exercises)
        number_expected = 0

        self.assertEqual(number_expected, number_exercises)
