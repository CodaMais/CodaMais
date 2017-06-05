# standard library
import logging

# Django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# local Django
from theory.models import Theory
from exercise.models import Exercise
from exercise.views import get_user_submissions_exercise


# Loggers Config
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@login_required
def list_all_theories(request):
    theory_list = Theory.objects.all().order_by('-id')
    return render(request,
                  'theories_page.html',
                  {'theory_list': theory_list})


@login_required
def show_theory(request, id, title):
    theory = Theory.objects.get(id=id)
    user = request.user
    list_theory_exercises = get_exercise_list_in_theory(user, theory)

    return render(request,
                  'theory_details.html', {
                   'theory': theory,
                   'list_theory_exercises': list_theory_exercises,
                  })


def get_exercise_list_in_theory(user, theory):
    logger.info("Getting all exercises corresponding to theory: " + theory.title)
    list_exercises = Exercise.objects.filter(theory=theory, deprecated=False)
    list_theory_exercises = get_user_submissions_exercise(user, list_exercises)

    return list_theory_exercises
