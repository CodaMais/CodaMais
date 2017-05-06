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
    topics = {}
    topics['list_topics'] = Topic.objects.all()

    return render(request, 'topics.html', topics)


# Displays topic and user data and a space for response to the topic.
def show_topic(request, id):
    logger.debug("Rendering topic page.")
    form = AnswerForm(request.POST or None,
                      initial={'description': ''})
    user = request.user

    try:
        topic = Topic.objects.get(id=id)
    except ObjectDoesNotExist:
        logger.exception("Topic is not exists.")
        # TODO(Roger) Create structure to alert the user that the topic doesn't exist.
        return redirect('list_all_topics')

    form = answer_topic(user, topic, form)
    answers = list_all_answer(topic)
    quantity_answer = len(answers)
    deletable_topic = show_delete_topic_button(topic.author, user.username)
    deletable_answers = show_delete_answer_button(answers, topic, user.username)
    zipped_data = zip(answers, deletable_answers)

    return render(request, 'show_topic.html', {
        'topic': topic,
        'deletable_topic': deletable_topic,
        'form': form,
        'quantity_answer': quantity_answer,
        'zipped_data': zipped_data
        })


def show_delete_topic_button(topic_author, current_user_username):
    deletable_topic = False  # Variable to define if user will see a button to delete a topic.

    # Check if logged user is visiting his own topic page.
    if topic_author.username == current_user_username:
        logger.debug("Topic page should be deletable")
        deletable_topic = True
    else:
        logger.debug("Topic page shouldn't be deletable.")
        # Nothing to do.

    logger.debug("Topic page is deletable? " + str(deletable_topic))
    return deletable_topic


@login_required(login_url='/')
def create_topic(request):
    form = TopicForm(
                    request.POST or None,
                    initial={constants.ANSWER_DESCRIPTION_NAME: ''})

    user = request.user  # Automaticlly get username that is logged.
    logger.info("user: " + user.username)

    if form.is_valid():

        logger.info("Create topic form was valid.")

        post = form.save(commit=False)  # Pausing the Django auto-save to enter username.
        post.author = user
        post.save()  # Posting date is generated automaticlly by the Model.

        # Reset form.
        form = TopicForm()
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
        logger.exception("Topic is not exists.")
        # TODO(Roger) Create structure to alert the user that the topic doesn't exist.
        return redirect('list_all_topics')

    user = request.user  # User object, from user model. Is the current online user.

    assert topic.author is not None, constants.DELETE_TOPIC_ASSERT

    if user.username == topic.author.username:
        logger.debug("Deleting topic.")
        topic.delete()

        return redirect('list_all_topics')
    else:
        logger.info("User can't delete topic.")

        # TODO(Roger) Create structure to alert the user that the topic isn't his.
        return redirect('list_all_topics')


# The user answers the topic accessed.
def answer_topic(user, topic, form):
    assert user is not None, "User not logged in."
    assert topic is not None, "Topic is not exists."

    if form.is_valid():
        answer_description = form.cleaned_data.get(constants.ANSWER_DESCRIPTION_NAME)
        answer = Answer()
        answer.creates_answer(user, topic, answer_description)

        # Reset form.
        form = AnswerForm()

        logger.debug("Create answer form was valid.")
    else:
        logger.warning("Invalid answer form.")

    return form


# List all answers of the topic that the user is accessing.
def list_all_answer(topic):
    assert topic is not None, "Topic is not exists."

    answers = []
    answers = Answer.objects.filter(topic=topic)
    logger.debug("Get all answers.")
    return answers


@login_required(login_url='/')
def delete_answer(request, id):
    logger.info("This is the id number: " + id)
    logger.info("Username" + request.user.username)
    try:
        answer = Answer.objects.get(id=id)  # Answer object, from Answer model.
    except ObjectDoesNotExist:
        logger.exception("Answer does not exists.")

    user = request.user  # User object, from user model. Is the current online user.

    topic = answer.topic

    assert answer.user is not None, constants.DELETE_TOPIC_ASSERT

    if user.username == answer.user.username:
        logger.debug("Deleting answer.")
        answer.delete()

        return redirect('show_topic', id=topic.id)
    else:
        logger.info("User can't delete answer.")

        return redirect('show_topic', id=topic.id)


def show_delete_answer_button(answers, topic, current_user_username):
    deletable_answers = []

    for answer in answers:
        # Check if logged user is visiting his own topic page.
        if answer.user.username == current_user_username:
            logger.debug("Answer should be deletable")
            is_deletable = True
        else:
            logger.debug("Answer shouldn't be deletable.")
            is_deletable = False

        deletable_answers.append(is_deletable)
        logger.info("Is deletable? " + str(is_deletable))

    return deletable_answers
