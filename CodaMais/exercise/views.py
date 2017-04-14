
# Django.
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

# local Django.
from exercise.models import Exercise
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
    api_response = ''
    if form.is_valid():
        api_response = submit_exercise(exercise, form.cleaned_data.get('code'))
        # form.save()
    else:
        # Nothing to do.
        pass

    return render(request, 'description_exercise.html', {
        'exercise':exercise,
        'form':form,
        'api_response': api_response
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
    response = conn.getresponse()
    return response.read()
