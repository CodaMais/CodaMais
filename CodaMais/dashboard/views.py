from datetime import timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import JsonResponse

from forum.models import Topic
from exercise.models import Exercise, UserExerciseSubmission
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
    user = request.user
    days_ago = 30
    days_ago_date = timezone.now().date() - timedelta(days=days_ago)
    user_exercises_submissions = UserExerciseSubmission.get_user_exercises_submissions_by_day(user, days_ago_date)

    # Lists that corresposd to fields in chart.
    label_date_field = []
    series_correct_answer = []
    series_number_submissions = []

    for user_exercise_submission in user_exercises_submissions:
        print(user_exercise_submission)
        submission_date = user_exercise_submission['date_submission']

        label_date_field.append(str(submission_date.day) + '/' + str(submission_date.month))
        series_correct_answer.append(int(user_exercise_submission['corrects']))
        series_number_submissions.append(user_exercise_submission['submissions'])

    data = {
        'labels': label_date_field,
        'series': [
            series_correct_answer,
            series_number_submissions
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
