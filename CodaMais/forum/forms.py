# Django.
from django import forms

# Local Django.
from forum.models import (
    Topic, Answer
)


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


class AnswerForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Answer
        exclude = ['user', 'topic', 'date_answer']
