# Django
from django import forms

# local Django
from exercise.models import UserExercise


class SubmitExerciseForm(forms.ModelForm):
    class Meta:
        model = UserExercise
        fields = ('code',)
