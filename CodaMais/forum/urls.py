# Django.
from django.conf.urls import url

# Local Django
from .views import (
    list_all_topics,
    show_topic,
    create_topic,
    delete_topic,
    delete_answer,
    best_answer,
    lock_topic,
)

urlpatterns = (
    # Forum
    url(r'^topics/$', list_all_topics, name='list_all_topics'),
    url(r'^topics/(?P<id>\d+)/$', show_topic, name='show_topic'),
    url(r'^newtopic/$', create_topic, name='create_topic'),
    url(r'^deletetopic/(?P<id>\d+)/$', delete_topic, name='delete_topic'),
    url(r'^deleteanswer/(?P<id>\d+)/$', delete_answer, name='delete_answer'),
    url(r'^best_answer/(?P<id>\d+)/$', best_answer, name='best_answer'),
    url(r'^locktopic/(?P<id>\d+)/$', lock_topic, name='lock_topic'),
)
