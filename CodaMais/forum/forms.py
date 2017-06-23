# Django.
from django import forms

# Local Django.
from forum.models import (
    Topic, Answer
)

from forum import constants
from django.utils.translation import ugettext_lazy as _


# Class: TopicForm
# The class represents all the fields of the topic in the site forum.
class TopicForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control'}))

    subtitle = forms.CharField(widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))

    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Topic
        exclude = ['author', 'date_topic', 'best_answer']

    def clean(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        subtitle = self.cleaned_data.get("subtitle")
        description = self.cleaned_data.get("description")

        if title is None:
            raise forms.ValidationError({'title': [_(constants.TITLE_SIZE)]})
        elif len(title) < constants.MIN_LENGTH_TITLE:
            raise forms.ValidationError({'title': [_(constants.TITLE_SIZE)]})
        elif len(title) > constants.MAX_LENGTH_TITLE:
            raise forms.ValidationError({'title': [_(constants.TITLE_SIZE)]})
        else:
            pass

        if subtitle is None:
            raise forms.ValidationError({'subtitle': [_(constants.SUBTITLE_SIZE)]})
        elif len(subtitle) < constants.MIN_LENGTH_SUBTITLE:
            raise forms.ValidationError({'subtitle': [_(constants.SUBTITLE_SIZE)]})
        elif len(subtitle) > constants.MAX_LENGTH_SUBTITLE:
            raise forms.ValidationError({'subtitle': [_(constants.SUBTITLE_SIZE)]})
        else:
            pass

        if description is None:
            raise forms.ValidationError({'description': [_(constants.TOPIC_DESCRIPTION_SIZE)]})
        elif len(description) < constants.MIN_LENGTH_TOPIC_DESCRIPTION:
            raise forms.ValidationError({'description': [_(constants.TOPIC_DESCRIPTION_SIZE)]})
        elif len(description) > constants.MAX_LENGTH_TOPIC_DESCRIPTION:
            raise forms.ValidationError({'description': [_(constants.TOPIC_DESCRIPTION_SIZE)]})
        else:
            pass

        return super(TopicForm, self).clean(*args, **kwargs)


class AnswerForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Answer
        exclude = ['user', 'topic', 'date_answer']
