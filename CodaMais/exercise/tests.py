# standard library
from datetime import timedelta

# Django
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone

# local Django
from exercise import (
    constants, views,
)
from exercise.models import (
    Exercise, UserExercise, TestCaseExercise,
    UserExerciseSubmission
)

from user.models import User

# 302 is the value returned from a HttpRequest status code when the URL was redirected.
REQUEST_REDIRECT = 302


class TestExerciseRegistration(TestCase):

    exercise = Exercise()

    def setUp(self):
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.exercise.tip = 'Tip exercise.'

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

    def test_exercise_get_tip(self):
        self.exercise.save()
        exercise_database = Exercise.objects.get(id=self.exercise.id)
        self.assertEqual(exercise_database.tip, self.exercise.tip)


class TestUserExerciseRegistration(TestCase):

    exercise = Exercise()
    test_case_exercise = TestCaseExercise()
    user_exercise = UserExercise()
    user = User()

    def setUp(self):

        self.factory = RequestFactory()

        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.test_case_exercise.input_exercise = "a\n"
        self.test_case_exercise.output_exercise = ["B"]
        self.user.email = "user@user.com"
        self.user.password = "userpassword"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.user_exercise.scored = False
        self.user_exercise.code = """
                                    #include <stdio.h>
                                    int main () {
                                        char c;
                                        scanf("%c", &c);
                                        printf("B");
                                        return 0;
                                    }
                                    """
        self.exercise.save()
        self.test_case_exercise.exercise = self.exercise
        self.test_case_exercise.save()
        self.user.save()
        self.user_exercise.user = self.user
        self.user_exercise.exercise = self.exercise

        self.user_exercise_valid_form = {
            'code': self.user_exercise.code
        }

        self.user_exercise_invalid_form = {
            'code': ''
        }

    def test_user_missed_exercise_in_show_exercise(self):
        code = """                 #include <stdio.h>
                                    int main () {
                                        char c;
                                        scanf("%c", &c);
                                        printf("ERROR");
                                        return 0;
                                    }
                                    """
        self.user_exercise.update_or_creates(
                                            code,
                                            self.user_exercise.exercise,
                                            self.user_exercise.user,
                                            self.user_exercise.time,
                                            self.user_exercise.status,
                                            self.user_exercise.scored)
        request = self.factory.get('/exercise/')
        request.user = self.user
        response = views.show_exercise(request, self.exercise.id)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)

    def test_if_relation_user_exercise_saved_database(self):
        self.user_exercise.update_or_creates(
                                            self.user_exercise.code,
                                            self.user_exercise.exercise,
                                            self.user_exercise.user,
                                            self.user_exercise.time,
                                            self.user_exercise.status,
                                            self.user_exercise.scored)
        user_exercise_database = UserExercise.objects.get(
                                user=self.user,
                                exercise=self.exercise)
        self.assertEqual(str(user_exercise_database), str(self.user_exercise))

    def test_if_relation_user_exercise_is_updated(self):
        self.user_exercise.update_or_creates(
                                            self.user_exercise.code,
                                            self.user_exercise.exercise,
                                            self.user_exercise.user,
                                            self.user_exercise.time,
                                            self.user_exercise.status,
                                            self.user_exercise.scored)
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

    def test_if_extract_time_exercise_is_success(self):
        exercise_inputs = ['a\n', 'b\n']
        response = views.submit_exercise(
                                        self.user_exercise.code,
                                        exercise_inputs)
        runtime = views.extract_time(response)
        self.assertNotEqual(runtime, None)

    def test_if_extract_stdout_exercise_is_success(self):
        exercise_inputs = ['a\n', 'b\n']
        response = views.submit_exercise(
                                        self.user_exercise.code,
                                        exercise_inputs)
        stdout = views.extract_stdout(response)
        self.assertNotEqual(stdout, None)

    def test_get_all_input_exercise(self):
        list_all_input = views.get_all_input_exercise(self.exercise)
        length = len(list_all_input)
        self.assertNotEqual(length, 0)

    def test_get_all_ouput_exercise(self):
        list_all_output = views.get_all_output_exercise(self.exercise)
        length = len(list_all_output)
        self.assertNotEqual(length, 0)

    def test_if_user_exercise_is_incorrect(self):
        input_exercise = ['a\n', 'b\n']
        response = views.submit_exercise(
                                        self.user_exercise.code,
                                        input_exercise)
        stdout = views.extract_stdout(response)
        status = views.exercise_status(stdout, self.test_case_exercise.output_exercise)
        self.assertFalse(status)

    def test_if_user_exercise_is_correct(self):
        input_exercise = ['B']
        response = views.submit_exercise(
                                        self.user_exercise.code,
                                        input_exercise)
        stdout = views.extract_stdout(response)
        status = views.exercise_status(stdout, self.test_case_exercise.output_exercise)
        self.assertTrue(status)

    def test_if_verify_compilation_source_code_is_none(self):
        code = None
        exercise_inputs = ['a\n', 'b\n']

        response = views.submit_exercise(
                                        code,
                                        exercise_inputs)
        message = views.verify_compilation_source_code(response)
        self.assertNotEqual(message, None)

    def test_if_user_scored_exercise(self):
        scored = False
        status = True
        response = views.scores_exercise(scored, self.user, self.exercise.score, status)
        self.assertTrue(response)

    def test_if_user_not_scored_exercise(self):
        scored = False
        status = False
        response = views.scores_exercise(scored, self.user, self.exercise.score, status)
        self.assertFalse(response)

    def test_if_user_already_scored_exercise(self):
        scored = True
        status = True
        response = views.scores_exercise(scored, self.user, self.exercise.score, status)
        self.assertTrue(response)

    def test_if_user_exercise_is_processed_valid_form(self):
        request = self.factory.post('/exercise/process/1/', self.user_exercise_valid_form)
        request.user = self.user
        response = views.process_user_exercise(request, self.exercise.id)
        self.assertEqual(response.status_code, REQUEST_REDIRECT)
        self.assertEqual(response.url, '/en/exercise/1/')

    def test_if_user_exercise_is_processed_invalid_form(self):
        request = self.factory.post('/exercise/process/1/', self.user_exercise_invalid_form)
        request.user = self.user
        response = views.process_user_exercise(request, self.exercise.id)
        self.assertEqual(response.status_code, REQUEST_REDIRECT)
        self.assertEqual(response.url, '/en/exercise/1/')

    def test_if_user_exercise_is_processed_invalid_form_code(self):
        user_exercise_invalid_form_code = {
            'code': 'int main()'
        }
        request = self.factory.post('/exercise/process/1/', user_exercise_invalid_form_code)
        request.user = self.user
        response = views.process_user_exercise(request, self.exercise.id)
        self.assertEqual(response.status_code, REQUEST_REDIRECT)
        self.assertEqual(response.url, '/en/exercise/1/')

    def test_get_user_submissions_exercise(self):
        self.user_exercise.update_or_creates(
                                            self.user_exercise.code,
                                            self.user_exercise.exercise,
                                            self.user_exercise.user,
                                            self.user_exercise.time,
                                            self.user_exercise.status,
                                            self.user_exercise.scored)

        list_exercises = Exercise.objects.all()

        submissions = views.get_user_submissions_exercise(self.user, list_exercises)
        self.assertEqual(len(submissions), 1)

    def test_if_status_submission_is_incorrect(self):
        status = False
        self.user_exercise.update_or_creates(
                                            self.user_exercise.code,
                                            self.user_exercise.exercise,
                                            self.user_exercise.user,
                                            self.user_exercise.time,
                                            status,
                                            self.user_exercise.scored)

        list_exercises = Exercise.objects.all()

        submissions = views.get_user_submissions_exercise(self.user, list_exercises)
        for exercise, user_exercise in submissions:
            self.assertEqual(user_exercise.status, status)

    def test_if_status_submission_is_correct(self):
        status = True
        self.user_exercise.update_or_creates(
                                            self.user_exercise.code,
                                            self.user_exercise.exercise,
                                            self.user_exercise.user,
                                            self.user_exercise.time,
                                            status,
                                            self.user_exercise.scored)

        list_exercises = Exercise.objects.all()

        submissions = views.get_user_submissions_exercise(self.user, list_exercises)
        for exercise, user_exercise in submissions:
            self.assertEqual(user_exercise.status, status)

    def test_get_user_submissions_exercise_status_is_true(self):
        self.user_exercise.update_or_creates(
                                            self.user_exercise.code,
                                            self.user_exercise.exercise,
                                            self.user_exercise.user,
                                            self.user_exercise.time,
                                            self.user_exercise.status,
                                            self.user_exercise.scored)

        list_exercises = Exercise.objects.all()

        submissions = views.get_user_submissions_exercise(self.user, list_exercises)
        self.assertEqual(len(submissions), 1)


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


class TestRequestExercise(TestCase):
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
        self.test_case_exercise.input_exercise = "a\n"
        self.test_case_exercise.output_exercise = "B\n"
        self.factory = RequestFactory()
        self.user.set_password('userpassword')
        self.user.save()
        self.exercise.save()

        self.test_case_exercise.exercise = self.exercise
        self.test_case_exercise.save()

    def test_list_exercises_not_deprecated(self):
        request = self.factory.get('/exercise/')
        request.user = self.user
        response = views.list_exercises_not_deprecated(request)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)

    def test_show_exercise_is_valid(self):
        request = self.factory.get('/exercise/')
        request.user = self.user
        response = views.show_exercise(request, self.exercise.id)
        self.assertEqual(response.status_code, constants.REQUEST_SUCCEEDED)


class TestUserExerciseSubmission(TestCase):
    user = User()
    exercise = Exercise()
    user_exercise = UserExercise()
    test_case_exercise = TestCaseExercise()
    user_exercises_submission = UserExerciseSubmission()

    def setUp(self):

        self.factory = RequestFactory()

        self.user.email = "user@user.com"
        self.user.password = "userpassword"
        self.user.first_name = "TestUser"
        self.user.username = "Username"
        self.user.is_active = True
        self.user.save()

        # Exercise.
        self.exercise.title = 'Basic Exercise'
        self.exercise.category = 2
        self.exercise.statement_question = '<p>Text Basic Exercise.</p>'
        self.exercise.score = 10
        self.exercise.deprecated = 0
        self.exercise.save()

        # Test case exercise.
        self.test_case_exercise.input_exercise = "a\n"
        self.test_case_exercise.output_exercise = ["B"]
        self.test_case_exercise.exercise = self.exercise
        self.test_case_exercise.save()

        #
        self.user_exercise.scored = False
        self.user_exercise.code = """
                                    #include <stdio.h>
                                    int main () {
                                        char c;
                                        scanf("%c", &c);
                                        printf("B");
                                        return 0;
                                    }
                                    """

        self.user_exercise.user = self.user
        self.user_exercise.exercise = self.exercise
        self.user_exercise.submissions = 1
        self.user_exercise.save()

    def test_request_user_exercises_submission_by_day(self):
        user = self.user

        days_ago = 7
        days_ago_date = timezone.now().date() - timedelta(days=days_ago)

        user_exercises_submissions = UserExerciseSubmission.submissions_by_day(
            user,
            days_ago_date
        )

        self.assertIsNotNone(user_exercises_submissions)

    def test_updates_exercise_submission(self):
        self.user_exercises_submission = self.user_exercise
        self.user_exercises_submission.save()

        UserExerciseSubmission.updates_submission(self.user_exercises_submission, self.user_exercise)

        self.assertEqual(self.user_exercises_submission.submissions, 2)

    def test_does_not_updates_exercise_submission(self):

        self.user_exercise.status = True
        self.user_exercise.save()

        self.user_exercises_submission.scored = True

        self.user_exercises_submission = self.user_exercise
        self.user_exercises_submission.save()

        UserExerciseSubmission.updates_submission(self.user_exercises_submission, self.user_exercise)

        self.assertEqual(self.user_exercises_submission.submissions, 2)

    def test_user_exercise_submission_submit(self):

        submission = UserExerciseSubmission.submit(self.user_exercise)
        self.assertIsNotNone(submission)

    def test_user_exercise_submission_submit_created(self):

        self.user_exercises_submission = self.user_exercise
        self.user_exercises_submission.save()

        submission = UserExerciseSubmission.submit(self.user_exercise)
        self.assertIsNotNone(submission)
