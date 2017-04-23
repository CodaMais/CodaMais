# Django.
from django.conf.urls import url
from django.conf.urls import include

# Local Django.
from .views import(
    show_exercise,
    list_exercises_not_deprecated
)

urlpatterns = (
    # Exercise.
    url(r'^exercise/(?P<id>\d+)/$', show_exercise, name='show_exercise'),
    url(r'^exercise/$', list_exercises_not_deprecated,
        name='list_exercises_not_deprecated'),
    url(r'^redactor/', include('redactor.urls')),
)
