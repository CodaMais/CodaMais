# Django.
from django import forms

# Local Django.
from forum.models import (
    Topic, Answer
)


class TopicForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control'}))

    subtitle = forms.CharField(widget=forms.TextInput(
                                    attrs={'class': 'form-control'}))

    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Topic
        exclude = ['author', 'dateTopic']


class AnswerForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Answer
        exclude = ['user', 'topic', 'date_answer']
