# standard
import logging

# Django.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# local Django.
from .models import (
    Topic, Answer
)
from .forms import (
    TopicForm, AnswerForm
)
from . import constants

# Required to access the information log.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def list_all_topics(request):
    data = {}
    data['list_topics'] = Topic.objects.all()
    return render(request, 'topics.html', data)


def show_topic(request, id):
    form = AnswerForm(request.POST or None)
    user = request.user
    try:
        topic = Topic.objects.get(id=id)
    except ObjectDoesNotExist:
        # TODO(Roger) Create structure to alert the user that the topic doesn't exist.
        return redirect('list_all_topics')

    answer_topic(user, topic, form)
    deletable_topic = show_delete_button(topic.author, request.user.username)

    return render(request, 'show_topic.html', {
        'topic': topic,
        'deletable_topic': deletable_topic,
        'form': form
        })


def show_delete_button(topic_author, current_user_username):
    deletable_topic = False  # Variable to define if user will see a button to edit his profile page.

    # Check if logged user is visiting his own topic page.
    if topic_author == current_user_username:
        logger.debug("Topic page should be deletable")
        deletable_topic = True
    else:
        logger.debug("Topic page shouldn't be deletable.")
        # Nothing to do.

    logger.debug("Topic page is deletable? " + str(deletable_topic))
    return deletable_topic


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
        # Create topic form was invalid.
        pass

        return render(request, 'new_topic.html', {'form': form})  # Re-using data if something has been speeled wrong.


@login_required(login_url='/')
def delete_topic(request, id):
    try:
        topic = Topic.objects.get(id=id)  # Topic object, from Topic model.
    except ObjectDoesNotExist:
        # TODO(Roger) Create structure to alert the user that the topic doesn't exist.
        return redirect('list_all_topics')

    user = request.user  # User object, from user model. Is the current online user.

    assert topic.author is not None, constants.DELETE_TOPIC_ASSERT

    if user.username == topic.author:
        logger.debug("Deleting topic.")
        topic.delete()

        return redirect('list_all_topics')
    else:
        logger.info("User can't delete topic.")

        # TODO(Roger) Create structure to alert the user that the topic isn't his.
        return redirect('list_all_topics')


def answer_topic(user, topic, form):

    if form.is_valid():
        answer_description = form.cleaned_data.get(constants.ANSWER_DESCRIPTION_NAME)
        answer = Answer()
        answer.update_or_creates(user, topic, answer_description)
    else:
        # Nothing to do.
        pass
