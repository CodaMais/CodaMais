# Django.
from django.shortcuts import render, redirect
import logging

# local Django.
from forum.models import Topic
from forum.forms import TopicForm
from django.contrib.auth.decorators import login_required

# Required to access the information log.
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
    username = request.user.username  # Automaticlly get usrname that is logged.
    logger.info("user: " + username)

    if form.is_valid():
        post = form.save(commit=False)  # Pausing the Django auto-save to enter username.
        post.autor = username
        post.save()  # Posting date is generated automaticlly by the Model.
        return redirect('list_all_topics')
    else:
        return render(request, 'new_topic.html', {'form': form})  # Re-using data if something has been speeled wrong.
