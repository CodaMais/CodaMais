'''
    Copyright (C) 2017, CodaMais.
    License: GNU General Public License v3.0, see LICENSE.txt
    App: theory
    File: views.py
    Contains all methods related to the theory informations that should appear for the user.
'''

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


# Obtaining all theories in a list to show in the theories page.
@login_required
def list_all_theories(request):
    logger.debug("Trying to show all theories.")

    theory_list = Theory.objects.all().order_by('-id')

    assert theory_list is not None, "List of theories is Null."

    return render(request,
                  'theories_page.html',
                  {'theory_list': theory_list})


# Obtaining theory informations to show in the theory page.
@login_required
def show_theory(request, id, title):
    assert id is not None, "Theory id is Invalid."
    assert title is not None, "Theory tittle is Null."
    logger.debug("Trying to show theory: " + title)

    # Getting all informations needed to show a Theory page completely.
    theory = Theory.objects.get(id=id)
    user = request.user
    list_theory_exercises = get_exercise_list_in_theory(user, theory)

    assert list_theory_exercises is not None, "List of theory exercises is Null."
    assert theory is not None, "Theory is Null."
    logger.info("Showing theory: " + title + " for user: " + user.username)

    return render(request,
                  'theory_details.html', {
                   'theory': theory,
                   'list_theory_exercises': list_theory_exercises,
                  })


# Obtaining exercises corresponding to determinate theory.
def get_exercise_list_in_theory(user, theory):
    assert user is not None, "User not logged in."
    assert theory is not None, "This theory doesn't exist."
    logger.info("Trying to get all exercises corresponding to theory: " + theory.title)

    # Getting: all exercises not deprecated related with this theory and user informations about
    # his exercies submissions.
    list_exercises = Exercise.objects.filter(theory=theory, deprecated=False)
    list_theory_exercises = get_user_submissions_exercise(user, list_exercises)

    assert list_theory_exercises is not None, "List of theory exercises is Null."
    logger.info("Getting all exercises corresponding to theory: " + theory.title)
    return list_theory_exercises
