# Django.
from django.conf.urls import url

# Local Django
from .views import(
    list_all_topics,
    show_topic,
    create_topic
)

urlpatterns = (
    # Forum
    url(r'^topics/$', list_all_topics, name='list_all_topics'),
    url(r'^topics/(?P<id>\d+)/$', show_topic, name='show_topic'),
    url(r'^newtopic/$', create_topic, name='create_topic'),
)
