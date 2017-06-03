from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from forum.models import Topic
from exercise.models import Exercise
from ranking.views import get_users_with_bigger_score
from exercise.views import get_user_exercises_last_submissions


@login_required()
def dashboard(request):
    user = request.user

    ranking_data = get_ranking_table_data()
    new_topics_data = get_new_forum_topics()
    new_exercises_data = get_new_exercises()
    user_last_exercises = get_user_last_exercise_submissions(user)

    return render(request, 'dashboard.html', {
        'data': ranking_data,
        'topics': new_topics_data,
        'exercises': new_exercises_data,
        'user_exercises': user_last_exercises
    })


def user_exercise_chart(request):
    data = {
            'labels': ['20/JPN - 30/Jan', '20/Feb - 20/Feb', '20/Mar - 20/Mar', '20/Abr - 20/Abr', '20/Mai - 20/Mai'],
            'series': [
                [542, 443, 320, 600, 553],
                [412, 243, 280, 580, 453]
              ]
          }

    return JsonResponse(data)


def get_ranking_table_data():
    ranking_data = get_users_with_bigger_score()
    return ranking_data


def get_new_forum_topics():
    # getting the last 5 topics created
    topics = Topic.objects.all().order_by('-id')[:5]
    return topics


def get_new_exercises():
    # getting the last 5 exercises created
    exercises = Exercise.objects.all().order_by('-id')[:5]
    return exercises


def get_user_last_exercise_submissions(user):

    user_exercises = get_user_exercises_last_submissions(user)
    return user_exercises
