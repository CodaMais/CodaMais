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
    Exercise, UserExercise, TestCaseExercise
)
from exercise import constants
from exercise.forms import SubmitExerciseForm
from achievement.views import verify_correct_exercise_achievement


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@login_required
def list_all_exercises(request):
    logger.info("List all exercises page.")
    data = {}
    data['list_exercises'] = Exercise.objects.all()
    return render(request, 'exercises.html', data)


@login_required
def list_exercises_not_deprecated(request):
    data = {}
    logger.info("List exercises not deprecated page.")
    data['list_exercises'] = Exercise.objects.filter(
                             deprecated=constants.IS_NOT_DEPRECATED)
    return render(request, 'exercises.html', data)


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

    return render(request, 'description_exercise.html', {
        'exercise': exercise,
        'user_exercise': user_exercise,
        'form': form,
        'input_exercise': input_exercise[0],
        'output_exercise': output_exercise[0]
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

        # Sum all runtime of test cases.
        runtime = extract_time(api_result)

        # Get the outputs of test cases.
        stdout = extract_stdout(api_result)

        # String list to compare with response.
        output_exercise = get_all_output_exercise(exercise)

        # Define if user exercise if correct or not
        status = exercise_status(stdout, output_exercise)

        # Define if user has scored or not in this exercise
        scored = scores_exercise(user_exercise.scored, user, exercise.score, status)

        user_exercise.update_or_creates(
                                        source_code, exercise,
                                        user, runtime, status, scored)

        # Used to unlock correct exercise achievements everytime this method is called.
        verify_correct_exercise_achievement(user)
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
