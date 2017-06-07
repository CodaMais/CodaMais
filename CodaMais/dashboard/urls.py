# Django.
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

# Local Django.
from dashboard.views import dashboard, user_exercise_chart

urlpatterns = (
    url(r'^dashboard/', login_required(dashboard), name='dashboard'),
    url(r'^userExerciseChart', user_exercise_chart, name='user_exercise_chart'),
)
