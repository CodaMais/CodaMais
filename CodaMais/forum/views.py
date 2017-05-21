# standard
import logging

# Django.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

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

    redirect_answer = answer_topic(user, topic, form)

    if redirect_answer is not None:
        return HttpResponseRedirect(redirect_answer)
    else:
        # Nothing to do
        pass

    answers = topic.answers()
    quantity_answer = len(answers)
    choose_best_answer = show_choose_best_answer_button(topic.author, user)
    deletable_topic = show_delete_topic_button(topic.author, user.username)
    deletable_answers = show_delete_answer_button(answers, topic, user.username)
    zipped_data = zip(answers, deletable_answers)
    best_answer = topic.best_answer

    return render(request, 'show_topic.html', {
        'topic': topic,
        'choose_best_answer': choose_best_answer,
        'deletable_topic': deletable_topic,
        'form': form,
        'quantity_answer': quantity_answer,
        'zipped_data': zipped_data,
        'best_answer': best_answer
        })


def show_choose_best_answer_button(topic_author, current_user):
    # Check if logger user is the author of the topic, if is, enable to
    # choose best answer
    if topic_author.id == current_user.id:
        logger.debug("Should enable to choose best answer.")
        return True
    else:
        logger.debug("Should not enable to choose best answer.")
        return False


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

    redirect_answer = None
    if form.is_valid():
        answer_description = form.cleaned_data.get(constants.ANSWER_DESCRIPTION_NAME)
        answer = Answer()
        answer.creates_answer(user, topic, answer_description)

        # Reset form.
        redirect_answer = "/forum/topics/" + str(topic.id)

        logger.debug("Create answer form was valid.")
    else:
        logger.warning("Invalid answer form.")
        # Nothing to do

    return redirect_answer


@login_required(login_url='/')
def delete_answer(request, id):
    logger.info("This is the id number: " + str(id))
    logger.info("Username" + request.user.username)
    try:
        answer = Answer.objects.get(id=id)  # Answer object, from Answer model.
    except ObjectDoesNotExist:
        logger.exception("Answer does not exists.")
        return redirect('list_all_topics')

    user = request.user  # User object, from user model. Is the current online user.

    topic = answer.topic

    assert answer.user is not None, constants.DELETE_ANSWER_ASSERT

    if user.username == answer.user.username:
        logger.debug("Deleting answer.")
        answer.delete()

        return redirect('show_topic', id=topic.id)
    else:
        logger.info("User can't delete answer.")

        return redirect('show_topic', id=topic.id)


@login_required(login_url='/')
def best_answer(request, id):
    try:
        best_answer = Answer.objects.get(id=id)  # Answer object, from Answer model.
    except ObjectDoesNotExist:
        logger.exception("Answer does not exists.")
        return redirect('list_all_topics')

    user = request.user  # User object, from user model. Is the current online user.
    topic = best_answer.topic

    # Checks if the signed user is the owner of the topic, then he can set the best answer.
    if user.username == topic.author.username:
        topic.best_answer = best_answer
        topic.save()
    else:
        pass
        # NOTHING TO DO

    return redirect('show_topic', id=topic.id)


# Only the person who whrote the anwer can delete it.
def show_delete_answer_button(answers, topic, current_user_username):
    deletable_answers = []

    for answer in answers:
        if answer.user.username == current_user_username:
            logger.debug("Answer should be deletable")
            # Current user is viewing his answer(s).
            is_deletable = True
        else:
            logger.debug("Answer shouldn't be deletable.")
            # Current user is viewing other user(s) answer(s).
            is_deletable = False

        deletable_answers.append(is_deletable)
        logger.info("Is deletable? " + str(is_deletable))

    return deletable_answers
