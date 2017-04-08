# Django.
from django.test import TestCase
from django.test.client import RequestFactory

# local Django.
from exercise import constants
from exercise.models import  Exercise
from exercise.views import *


class TestExerciseRegistration(TestCase):

    exercise = Exercise()

    def setUp(self):
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.exercise.input_exercise = 'Input Basic Exercise.'
        self.exercise.output_exercise = 'Output Basic Exercise.'

    def test_str_is_correct(self):
        self.exercise.save()
        exercise_database = exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(str(exercise_database),str(self.exercise))

    def test_if_exercise_is_saved_database(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database, self.exercise)

    def test_exercise_get_title(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database.title, self.exercise.title)

    def test_exercise_get_category(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database.category, self.exercise.category)

    def test_exercise_get_statement_question(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database.statement_question, self.exercise.statement_question)

    def test_exercise_get_score(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database.score, self.exercise.score)

    def test_exercise_get_deprecated(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database.deprecated, self.exercise.deprecated)

    def test_exercise_get_input_exercise(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database.input_exercise, self.exercise.input_exercise)

    def test_exercise_get_output_exercise(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database.output_exercise, self.exercise.output_exercise)


class TestRequestExercise(TestCase):

    exercise = Exercise()
    REQUEST_SUCCEEDED = 200 # 200 is return with success response.

    def setUp(self):
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.exercise.input_exercise = 'Input Basic Exercise.'
        self.exercise.output_exercise = 'Output Basic Exercise.'
        self.factory = RequestFactory()


    def test_list_all_exercises(self):
        request = self.factory.get('/exercise')
        response = list_all_exercises(request)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)

    def test_list_exercises_not_deprecated(self):
        request = self.factory.get('/exercise')
        response = list_exercises_not_deprecated(request)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)

    def test_show_exercise(self):
        self.exercise.save()
        request = self.factory.get('/exercise/')
        response = show_exercise(request, self.exercise.id)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)
