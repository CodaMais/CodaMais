
# Django.
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

# local Django.
from exercise.models import *
from user.models import UserProfile
from exercise import constants
from exercise.forms import SubmitExerciseForm

# python
import http.client
import urllib

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
    form = SubmitExerciseForm(request.POST or None)
    # TODO: mostrar o codigo do usuário no formulário. Se existir.

    # get current logged user
    user = request.user
    # get the current exercise of the user
    user_exercise = UserExercise.objects.get(user = user, exercise = exercise)

    if form.is_valid():
        # source code sent by the user
        source_code = form.cleaned_data.get('code')

        # receives the JSON response from API
        api_result = submit_exercise(exercise, source_code)

        # TODO: change variable time
        user_exercise.update_or_creates(source_code, exercise, user, "0.0")

    else:
        # Nothing to do.
        pass

    return render(request, 'description_exercise.html', {
        'exercise':exercise,
        # 'user_exercise': user_exercise,
        'form':form
    })

def submit_exercise(excercise, source_code):
    # split the string of test cases into an array
    test_cases = excercise.input_exercise.split(" ")
    conn = http.client.HTTPConnection("api.hackerrank.com")
    conn.request("POST", "/checker/submission.json", urllib.parse.urlencode({
        "source": source_code,
        "lang": 1,
        "testcases": json.dumps(test_cases),
        "api_key": constants.HACKERRANK_API_KEY,
        "wait": "true",
        "format": "json"
    }), {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    })
    result = conn.getresponse().read()
    return result
