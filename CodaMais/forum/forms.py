# Django.
from django.forms import ModelForm

# Local Django.
from forum.models import (
    Topic, Answer
)


class TopicForm(ModelForm):

    class Meta:
        model = Topic
        exclude = ['author', 'dateTopic']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ('description',)
