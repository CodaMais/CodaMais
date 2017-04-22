# Django
from django.contrib import auth
from django.test import TestCase
from django.test.client import RequestFactory

# local Django
from exercise import constants
from exercise.models import (
    Exercise, UserExercise, TestCaseExercise
)
from user.models import User
from exercise import views


class TestExerciseRegistration(TestCase):

    exercise = Exercise()

    def setUp(self):
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0

    def test_str_is_correct(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(str(exercise_database), str(self.exercise))

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
        self.assertEqual(
                        exercise_database.statement_question,
                        self.exercise.statement_question)

    def test_exercise_get_score(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database.score, self.exercise.score)

    def test_exercise_get_deprecated(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(
            exercise_database.deprecated,
            self.exercise.deprecated)


class TestUserExerciseRegistration(TestCase):

    exercise = Exercise()
    test_case_exercise = TestCaseExercise()
    user_exercise = UserExercise()
    user = User()

    def setUp(self):
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.test_case_exercise.input_exercise = "a\n"
        self.test_case_exercise.output_exercise = "B\n"
        self.user.email = "user@user.com"
        self.user.password = "userpassword"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.user_exercise.code = """
                                    #include <stdio.h>
                                    int main () {
                                        char c;
                                        scanf("%c", &c);
                                        printf("B");
                                        return 0;
                                    }
                                    """

    def test_if_relation_user_exercise_saved_database(self):
        self.exercise.save()
        self.test_case_exercise.exercise = self.exercise
        self.test_case_exercise.save()
        self.user.save()
        self.user_exercise.user = self.user
        self.user_exercise.exercise = self.exercise
        self.user_exercise.update_or_creates(
                                            self.user_exercise.code,
                                            self.user_exercise.exercise,
                                            self.user_exercise.user,
                                            self.user_exercise.time,
                                            self.user_exercise.status)
        user_exercise_database = UserExercise.objects.get(
                                user=self.user,
                                exercise=self.exercise)
        self.assertEqual(str(user_exercise_database), str(self.user_exercise))

    def test_if_relation_user_exercise_is_updated(self):
        self.exercise.save()
        self.test_case_exercise.exercise = self.exercise
        self.test_case_exercise.save()
        self.user.save()
        self.user_exercise.user = self.user
        self.user_exercise.exercise = self.exercise
        self.user_exercise.save()
        self.user_exercise.update_or_creates(
                                            self.user_exercise.code,
                                            self.user_exercise.exercise,
                                            self.user_exercise.user,
                                            self.user_exercise.time,
                                            self.user_exercise.status)
        user_exercise_database = UserExercise.objects.get(
                                 user=self.user,
                                 exercise=self.exercise)
        self.assertEqual(str(user_exercise_database), str(self.user_exercise))

    def test_if_exercise_is_submitted(self):
        exercise_inputs = ['a\n', 'b\n']
        response = views.submit_exercise(
                                        self.user_exercise.code,
                                        exercise_inputs)
        self.assertIn("result", response)



class TestCaseExerciseRegistration(TestCase):
    exercise = Exercise()
    test_case_exercise = TestCaseExercise()

    def setUp(self):
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.test_case_exercise.input_exercise = "1 2\n"
        self.test_case_exercise.output_exercise = "2 1\n"

    def test_if_user_exercise_is_saved_database(self):
        self.exercise.save()
        self.test_case_exercise.exercise = self.exercise
        self.test_case_exercise.save()
        test_case_exercise_database = TestCaseExercise.objects.get(
                                    id=self.test_case_exercise.id)
        self.assertEqual(
                        str(test_case_exercise_database),
                        str(self.test_case_exercise))


# class TestRequestExercise(TestCase):
#     exercise = Exercise()
#     test_case_exercise = TestCaseExercise()
#     user = User()
#
#     def setUp(self):
#         self.user.email = "user@user.com"
#         self.user.password = "userpassword"
#         self.user.first_name = "TestUser"
#         self.user.username = "Username"
#         self.user.is_active = True
#         self.exercise.title = 'Basic Exercise'
#         self.exercise.category = 2
#         self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
#         self.exercise.score = 10
#         self.exercise.deprecated = 0
#         self.test_case_exercise.input_exercise = "a\n"
#         self.test_case_exercise.output_exercise = "B\n"
#         self.factory = RequestFactory()
#         self.user.save()
#         self.exercise.save()
#
#         self.test_case_exercise.exercise = self.exercise
#
#         self.test_case_exercise.save()
#         auth = self.authenticate(
#                                 email=self.user.email,
#                                 password=self.user.password)
#         auth.is_authenticated()
#
#
#     def test_list_all_exercises(self):
#         request = self.factory.get('/exercise')
#         response = views.list_all_exercises(request)
#         self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)
#
#     def test_list_exercises_not_deprecated(self):
#         request = self.factory.get('/exercise')
#         response = views.list_exercises_not_deprecated(request)
#         self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)

    # def test_show_exercise(self):
    #     self.exercise.save()
    #     request = self.factory.get('/exercise/')
    #     response = views.show_exercise(request, self.exercise.id)
    #     self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)
