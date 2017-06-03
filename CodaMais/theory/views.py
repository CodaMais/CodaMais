# standard library
import logging

# Django
from django.shortcuts import render

# local Django
from theory.models import Theory
from exercise.models import Exercise

# Loggers Config
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def list_all_theories(request):
    theory_list = Theory.objects.all().order_by('-id')
    return render(request,
                  'theories_page.html',
                  {'theory_list': theory_list})


def show_theory(request, id, title):
    theory = Theory.objects.get(id=id)
    return render(request, 'theory_details.html', {'theory': theory})


def get_exercise_list_in_theory(theory):
    logger.info("Getting all exercises corresponding to theory: " + theory.title)
    list_exercises = Exercise.objects.filter(theory=theory)
    return list_exercises
