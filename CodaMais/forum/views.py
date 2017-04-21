# Django.
from django.shortcuts import render, redirect
import logging

# local Django.
from forum.models import Topic
from forum.forms import TopicForm
from django.contrib.auth.decorators import login_required
from user.models import User


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_all_topics(request):
    data = {}
    data['list_topics'] = Topic.objects.all()
    return render(request, 'topics.html', data)


def show_topic(request, id):
    topic = Topic.objects.get(id=id)
    return render(request, 'show_topic.html', {'topic': topic})


@login_required(login_url='/')
def create_topic(request):

    form = TopicForm(request.POST or None)
    # user = User.objects.get(username=username)
    username = request.user.username
    logger.info("user: " + username)
    if form.is_valid():
        post = form.save(commit=False)
        post.autor = username
        post.save()
        return redirect('list_all_topics')
    else:
        return render(request, 'new_topic.html', {'form': form})
