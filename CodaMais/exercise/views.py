
# Django.
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

# local Django.
from exercise.models import Exercise
from exercise import constants
from exercise.forms import SubmitExerciseForm


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

    if form.is_valid():

        form.save()
    else:
        # Nothing to do.
        pass

    return render(request, 'description_exercise.html', {'exercise':exercise, 'form':form})
