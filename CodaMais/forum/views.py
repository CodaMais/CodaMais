# standard
import logging

# Django.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# local Django.
from .models import Topic
from .forms import TopicForm
from . import constants

# Required to access the information log.
logging.basicConfig(level=logging.DEBUG)
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
    username = request.user.username  # Automaticlly get username that is logged.
    logger.info("user: " + username)

    if form.is_valid():

        logger.info("Create topic form was valid.")

        post = form.save(commit=False)  # Pausing the Django auto-save to enter username.
        post.author = username
        post.save()  # Posting date is generated automaticlly by the Model.
        return redirect('list_all_topics')
    else:
        logger.info("Create topic form was invalid.")

        return render(request, 'new_topic.html', {'form': form})  # Re-using data if something has been speeled wrong.


@login_required(login_url='/')
def delete_topic(request, id):

    topic = Topic.objects.get(id=id)  # Topic object, from Topic model.
    user = request.user  # User object, from user model. Is the current online user.

    if topic is not None:

        assert topic.author is not None, constants.DELETE_TOPIC_ASSERT

        if user.username == topic.author:
            logger.debug("Deleting topic.")
            topic.delete()

            return redirect('list_all_topics')
        else:
            logger.info("User can't delete topic.")

            # TODO(Roger) Create structure to alert the user that the topic isn't his.
            return redirect('list_all_topics')
    else:
        logger.info("Topic doesn't exist.")

        # TODO(Roger) Create structure to alert the user that the topic doesn't exist.
        return redirect('list_all_topics')
