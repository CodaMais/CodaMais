# Django.
from django.shortcuts import render

# local Django.
from forum.models import Topic


def list_all_topics(request):
    data = {}
    data['list_topics'] = Topic.objects.all()
    return render(request, 'topics.html', data)
