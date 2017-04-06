from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from exercise.models import Exercise
from exercise import constants
from exercise.form import ExerciseForm


def list_all_exercises(request):
    data = {}
    data['list_exercises'] = Exercise.objects.all()
    return render(request, 'exercises.html', data)

def list_exercises_not_deprecated(request):
    data = {}
    data['list_exercises'] = Exercise.objects.filter(deprecated=constants.IS_NOT_DEPRECATED)
    return render(request, 'exercises.html', data)

def show_exercise(request, id):
    exercise = Exercise.objects.get(id=id)
    return render(request, 'description_exercise.html', {'exercise':exercise})

def create_exercise(request):
    form = ExerciseForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('list_exercises_not_deprecated')
    else:
        return render(request, 'new_exercise.html', {'form':form})
