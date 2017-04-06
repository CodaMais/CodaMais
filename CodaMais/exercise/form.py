from django.forms import ModelForm
from exercise.models import Exercise


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        exclude = ['']
