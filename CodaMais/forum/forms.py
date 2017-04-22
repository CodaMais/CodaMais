# Django.
from django.forms import ModelForm

# Local Django.
from forum.models import Topic


class TopicForm(ModelForm):

    class Meta:
        model = Topic
        exclude = ['author', 'dateTopic']
