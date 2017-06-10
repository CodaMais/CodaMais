
# standard library
import http.client
import urllib
import json
import logging

# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# local Django
from exercise.models import (
    Exercise, UserExercise, TestCaseExercise, UserExerciseSubmission
)
from exercise import constants
from exercise.forms import SubmitExerciseForm
from achievement.views import (
    verify_correct_exercise_achievement, verify_score_achievement, verify_submited_exercises_achievement
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(constants.PROJECT_NAME)


@login_required
def list_exercises_not_deprecated(request):
    logger.info("List exercises not deprecated page.")
    exercises = Exercise.objects.filter(
                             deprecated=constants.IS_NOT_DEPRECATED)
    user = request.user

    list_exercises = get_user_submissions_exercise(user, exercises)
    return render(request, 'exercises.html', {
        'list_exercises': list_exercises
    })


@login_required
def show_exercise(request, id):
    exercise = Exercise.objects.get(id=id, deprecated=0)
    logger.info("Show exercises not deprecated page.")

    # Get current logged user.
    user = request.user
    assert user is not None, "User not logged in."

    # Get the current exercise of the user.
    user_exercise = get_current_user_exercise(user, exercise)

    # Show the user code in the field if the code exists.
    form = SubmitExerciseForm(None,
                              initial={constants.CODE_NAME: user_exercise.code})

    # String list for the JSON.
    input_exercise = get_all_input_exercise(exercise)

    # String list to compare with response.
    output_exercise = get_all_output_exercise(exercise)

    # Verify if user should access a tip.
    user_missed_exercise = False
    if user_exercise.number_submission > 0 and user_exercise.status is False:
        user_missed_exercise = True
    else:
        # Nothing to do.
        pass

    return render(request, 'description_exercise.html', {
        'exercise': exercise,
        'user_exercise': user_exercise,
        'form': form,
        'input_exercise': input_exercise[0],
        'output_exercise': output_exercise[0],
        'user_missed_exercise': user_missed_exercise
    })


@login_required
def process_user_exercise(request, id):
    user = request.user
    form = SubmitExerciseForm(request.POST)
    exercise = Exercise.objects.get(id=id, deprecated=0)

    if form.is_valid():
        logger.info("Code form was valid.")
        # Source code sent by the user.
        source_code = form.cleaned_data.get(constants.CODE_NAME)

        # String list for the JSON.
        input_exercise = get_all_input_exercise(exercise)

        # Get the current exercise of the user.
        user_exercise = get_current_user_exercise(user, exercise)

        # Receives the JSON response from API.
        api_result = submit_exercise(source_code, input_exercise)

        # Defines whether the submitted code can be compiled
        code_has_been_compiled = verify_compilation_source_code(api_result)

        # Case compiled, extract API return data.
        if code_has_been_compiled is True:
            # Sum all runtime of test cases.
            runtime = extract_time(api_result)

            # Get the outputs of test cases.
            stdout = extract_stdout(api_result)
        else:
            # Initializes with default variable values required
            stdout = []
            runtime = 0.0

        # String list to compare with response.
        output_exercise = get_all_output_exercise(exercise)

        # Define if user exercise if correct or not
        status = exercise_status(stdout, output_exercise)

        # Define if user has scored or not in this exercise
        scored = scores_exercise(user_exercise.scored, user, exercise.score, status)

        user_exercise.update_or_creates(
                                        source_code, exercise,
                                        user, runtime, status, scored)

        UserExerciseSubmission.submit(user_exercise)

        # Used to unlock correct exercise achievements everytime this method is called.
        verify_correct_exercise_achievement(user, request)

        # Used to unlock submited exercises achievement everytime this method is called.
        verify_submited_exercises_achievement(user, request)

        # Used to unlock score achievements when the user receives points from exercises.
        verify_score_achievement(user, request)
    else:
        logger.info("The code form was invalid.")
        # Nothing to do.
        pass

    return redirect('show_exercise', id=id)


def scores_exercise(scored, user, score, status):
    if not scored:
        logger.info("The user has not scored.")
        # if the user has not scored before
        if status:
            logger.info("Set score to the user.")
            # if the exercise is correct
            user.score += score
            user.save()
            return True
        else:
            logger.info("The exercise is incorrect.")
            # but it is incorrect
            return False
    else:
        logger.info("The user has already scored.")
        # the user has already scored in that exercise
        return True


def get_current_user_exercise(user, exercise):
    try:
        user_exercise = UserExercise.objects.get(user=user, exercise=exercise)
    except UserExercise.DoesNotExist:
        user_exercise = UserExercise()
    return user_exercise


def submit_exercise(source_code, input_exercise):
    conn = http.client.HTTPConnection("api.hackerrank.com")
    conn.request("POST", "/checker/submission.json", urllib.parse.urlencode({
        "source": source_code,
        "lang": 1,
        "testcases": json.dumps(input_exercise),
        "api_key": constants.HACKERRANK_API_KEY,
        "wait": "true",
        "format": "json"
    }), {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    })
    logger.info("The exercise submission and the API response were made.")
    result = conn.getresponse().read().decode('utf-8')

    return result


def extract_time(api_result):
    list_time = json.loads(api_result)['result']['time']
    sum_time = constants.INITIAL_SUM
    for time in list_time:
        sum_time += time

    logger.info("The runtime extraction was taken from the API response.")
    return sum_time


def extract_stdout(api_result):
    stdout = json.loads(api_result)['result']['stdout']

    logger.info("The stdout extraction was taken from the API response.")
    return stdout


def exercise_status(actual_output, original_output):
    if actual_output == original_output:

        logger.info("The exercise is correct.")
        return True
    else:
        return False


def get_all_input_exercise(exercise):
    test_cases = TestCaseExercise.objects.filter(exercise=exercise)
    list_input_exercise = []

    for test_case in test_cases:
        current_input_exercise = str(test_case.input_exercise)
        list_input_exercise.append(current_input_exercise)

    logger.info("The inputs for the exercise from database have been organized.")
    return list_input_exercise


def get_all_output_exercise(exercise):
    test_cases = TestCaseExercise.objects.filter(exercise=exercise)
    list_output_exercise = []

    for test_case in test_cases:
        current_output_exercise = str(test_case.output_exercise)
        list_output_exercise.append(current_output_exercise)

    logger.info("The outputs for the exercise from database have been organized.")
    return list_output_exercise


# This method get the number of submissions made by user in the exercise.
def get_user_submissions_exercise(user, exercises):
    assert user is not None, "User not logged."

    logger.info("Inside get_user_submissions_exercise")

    list_user_exercise = []

    # Getting informations about submissions in exercises made by user.
    for exercise in exercises:
        user_exercise = None
        try:
            user_exercise = UserExercise.objects.get(user=user, exercise=exercise)
        except UserExercise.DoesNotExist:
            user_exercise = UserExercise()

        logger.debug("Exercise: "+exercise.title+" Status: "+str(user_exercise.status))
        list_user_exercise.append(user_exercise)

    assert len(exercises) == len(list_user_exercise), "The list of submissions has a different number of exercises."
    zipped_data = zip(exercises, list_user_exercise)
    list_user_submissions = list(zipped_data)

    return list_user_submissions


# This method get the last five exercises submited by user.
def get_user_exercises_last_submissions(user):
    assert user is not None, "User not logged."

    user_exercises_list = UserExercise.objects.filter(user=user).order_by('-date_submission')[:5]

    return user_exercises_list


# Defines whether the submitted code can be compiled
def verify_compilation_source_code(api_result):
    message = json.loads(api_result)['result']['message']

    # True was compiled, False was not compiled
    if message is not None:
        return True
    else:
        return False
