# standard library
import logging

# Django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Local Django
from user.models import User
from exercise.models import UserExercise

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@login_required
def show_ranking(request):
    logger.info("INSIDE show_ranking!")
    ranking_data = get_user_scores_and_completed_exercises()
    return render(request, 'ranking.html', {'data': ranking_data})


def get_user_scores_and_completed_exercises():
    completed_exercises = []

    user_list = User.objects.filter().order_by('-score')

    # Count all completed exercises for each user.
    for user in user_list:
        completed_exercises.append(UserExercise.objects.filter(user=user, status=True).count())

    data = zip(user_list, completed_exercises)
    return data


# This method is responsable to catch the five users with big score to show in dashboard
def get_users_with_bigger_score():
    logger.info("Picking up users with higher scores!")
    completed_exercises = []
    user_list = User.objects.filter().order_by('-score')
    contador = 0

    # Count all completed exercises for each user.
    for user in user_list:
        completed_exercises.append(UserExercise.objects.filter(user=user, status=True).count())
        contador = contador + 1
        if(contador == 5):
            break

    data = zip(user_list, completed_exercises)

    return data
