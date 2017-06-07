import logging

from datetime import timedelta

from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template import RequestContext

from django.http import JsonResponse

from forum.models import Topic
from exercise.models import Exercise, UserExerciseSubmission
from ranking.views import get_users_with_bigger_score
from exercise.views import get_user_exercises_last_submissions
from . import constants

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(constants.DEFAULT_LOGGER)


@login_required()
def dashboard(request):
    user = request.user

    ranking_data = get_users_with_bigger_score()

    # getting the last 5 topics created
    new_topics_data = Topic.new_topics()

    # getting the last 5 exercises created
    new_exercises_data = Exercise.new_exercises()
    user_last_exercises = get_user_exercises_last_submissions(user)

    return render(request, 'dashboard.html', {
        'data': ranking_data,
        'topics': new_topics_data,
        'exercises': new_exercises_data,
        'user_exercises': user_last_exercises
    })


def user_exercise_chart(request):
    user = request.user
    days_ago = constants.CHART_USER_EXERCISES_SUBMISSIONS_DAYS
    # calculates the date given the number of days ago
    days_ago_date = timezone.now().date() - timedelta(days=days_ago)

    # get the user exercises submissions
    user_exercises_submissions = UserExerciseSubmission.submissions_by_day(
        user,
        days_ago_date
    )

    # Lists that corresposd to fields in chart.
    label_date_field = []
    series_correct_answer = []
    series_number_submissions = []

    for user_exercise_submission in user_exercises_submissions:
        logger.info(user_exercise_submission)
        submission_date = user_exercise_submission['date_submission']

        # Feed the lists of exercises submissions (days, corrects, submissions)
        label_date_field.append(str(submission_date.day) + '/' + str(submission_date.month))
        series_correct_answer.append(int(user_exercise_submission['corrects']))
        series_number_submissions.append(user_exercise_submission['submissions'])

    # Creates the JSON structure of the chart
    data = {
        'labels': label_date_field,
        'series': [
            series_correct_answer,
            series_number_submissions
        ]
    }

    return JsonResponse(data)


# This method is called when the aplication raises a 404 error and replace the debug
# 404 error default page for a customized one (404.html).
def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response
