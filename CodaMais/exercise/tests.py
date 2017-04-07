from django.test import TestCase
from django.test.client import RequestFactory
from exercise.models import  Exercise
from exercise.views import *


class TestRequestExercise(TestCase):

    exercise = Exercise()

    def setUp(self):
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.exercise.input_exercise = 'Input Basic Exercise.'
        self.exercise.output_exercise = 'Output Basic Exercise.'
        self.factory = RequestFactory()

    def test_if_the_list_all_exercises_is_showing(self):
        request = self.factory.get('/exercise')
        response = list_all_exercises(request)
        self.assertEqual(response.status_code, 200)

    def test_if_the_list_exercises_is_not_deprecated(self):
        request = self.factory.get('/exercise')
        response = list_exercises_not_deprecated(request)
        self.assertEqual(response.status_code, 200)

    def test_if_the_exercise_is_showing(self):
        self.exercise.save()
        request = self.factory.get('/exercise/')
        response = show_exercise(request, self.exercise.id)
        self.assertEqual(response.status_code, 200)
