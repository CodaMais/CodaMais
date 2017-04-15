# Django.
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# local Django.
from exercise.models import *
from user.models import UserProfile
from exercise import constants
from exercise.forms import SubmitExerciseForm

# python
import http.client
import urllib
import decimal
import json


def list_all_exercises(request):
    data = {}
    data['list_exercises'] = Exercise.objects.all()
    return render(request, 'exercises.html', data)

def list_exercises_not_deprecated(request):
    data = {}
    data['list_exercises'] = Exercise.objects.filter(deprecated=constants.IS_NOT_DEPRECATED)
    return render(request, 'exercises.html', data)

def show_exercise(request, id):
    exercise = Exercise.objects.get(id=id, deprecated=0)

    # Get current logged user.
    user = request.user

    # Get the current exercise of the user.
    user_exercise = get_current_user_exercise(user, exercise)

    # Show the user code in the field if the code exists.
    form = SubmitExerciseForm(request.POST or None, initial={constants.CODE_NAME:user_exercise.code})

    # String list for the JSON.
    input_exercise = get_all_input_exercise(exercise)

    # String list to compare with response.
    output_exercise = get_all_output_exercise(exercise)

    if form.is_valid():

        # Source code sent by the user.
        source_code = form.cleaned_data.get(constants.CODE_NAME)

        # Receives the JSON response from API.
        api_result = submit_exercise(exercise, source_code, input_exercise)

        # Sum all runtime of test cases.
        runtime = extract_time(api_result)

        user_exercise.update_or_creates(source_code, exercise, user, runtime, False)

    else:
        # Nothing to do.
        pass

    return render(request, 'description_exercise.html', {
        'exercise':exercise,
        'user_exercise': user_exercise,
        'form': form,
        'input_exercise': input_exercise[0],
        'output_exercise': output_exercise[0]
    })

def get_current_user_exercise(user, exercise):
    try:
        user_exercise = UserExercise.objects.get(user=user, exercise=exercise)
    except UserExercise.DoesNotExist:
        user_exercise = UserExercise()

    return user_exercise;

def submit_exercise(exercise, source_code, input_exercise):
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
    result = conn.getresponse().read().decode('utf-8')

    return result

def extract_time(result):
    list_time = json.loads(result)['result']['time']
    sum_time = constants.INITIAL_SUM

    for time in list_time:
        sum_time += time

    return sum_time

def get_all_input_exercise(exercise):
    test_cases = TestCase.objects.filter(exercise=exercise)
    list_input_exercise = []

    for test_case in test_cases:
        current_input_exercise = str(test_case.input_exercise)
        list_input_exercise.append(current_input_exercise)

    return list_input_exercise

def get_all_output_exercise(exercise):
    test_cases = TestCase.objects.filter(exercise=exercise)
    list_output_exercise = []

    for test_case in test_cases:
        current_output_exercise = str(test_case.output_exercise)
        list_output_exercise.append(current_output_exercise)

    return list_output_exercise
