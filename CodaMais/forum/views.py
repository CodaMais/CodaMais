# Django.
from django.shortcuts import render

# local Django.
from forum.models import Topic


def list_all_topics(request):
    data = {}
    data['list_topics'] = Topic.objects.all()
    return render(request, 'topics.html', data)


def show_topic(request, id):
    topic = Topic.objects.get(id=id)
    return render(request, 'show_topic.html', {'topic': topic})
