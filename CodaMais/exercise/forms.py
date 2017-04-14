# Django.
from django import forms
from exercise.models import UserExercise

class SubmitExerciseForm(forms.ModelForm):
     class Meta:
        model = UserExercise
        exclude = ['number_submission', 'user', 'exercise', 'status']
