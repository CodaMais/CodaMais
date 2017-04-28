# Django.
from django.conf.urls import url
from django.conf.urls import include

# Local Django.
from .views import (
    show_exercise,
    list_exercises_not_deprecated,
    process_user_exercise
)

urlpatterns = (
    # Exercise.
    url(r'^(?P<id>\d+)/$', show_exercise, name='show_exercise'),
    url(r'^$', list_exercises_not_deprecated,
        name='list_exercises_not_deprecated'),
    url(r'^process/(?P<id>\d+)/$', process_user_exercise, name='process_user_exercise'),
    url(r'^redactor/', include('redactor.urls'))
)
