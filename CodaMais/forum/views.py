# Django.
from django.shortcuts import render, redirect

# local Django.
from forum.models import Topic
from forum.forms import TopicForm


def list_all_topics(request):
    data = {}
    data['list_topics'] = Topic.objects.all()
    return render(request, 'topics.html', data)


def show_topic(request, id):
    topic = Topic.objects.get(id=id)
    return render(request, 'show_topic.html', {'topic': topic})


def create_topic(request):
    form = TopicForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('list_all_topics')
    else:
        return render(request, 'new_topic.html', {'form': form})
