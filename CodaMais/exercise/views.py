from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from exercise.models import Exercise
from exercise import constants


def list_all_exercises(request):
    data = {}
    data['list_exercises'] = Exercise.objects.all()
    return render(request, 'exercises.html', data)

def list_exercises_not_deprecated(request):
    data = {}
    data['list_exercises'] = Exercise.objects.filter(deprecated=constants.IS_NOT_DEPRECATED)
    return render(request, 'exercises.html', data)
