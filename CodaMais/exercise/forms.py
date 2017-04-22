# Django
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

# local Django
from exercise.models import UserExercise
from exercise import constants


class SubmitExerciseForm(forms.ModelForm):
    code = forms.CharField(min_length=constants.MIN_LENGTH_CODE)

    class Meta:
        model = UserExercise
        exclude = ['number_submission', 'user', 'exercise', 'status', 'time']

    def clean(self, *args, **kwargs):
        code = self.cleaned_data.get('code')

        if len(code) < constants.MIN_LENGTH_CODE:
            raise forms.ValidationError(_(constants.CODE_SIZE))
        else:
            # Nothing to do.
            pass

        return super(SubmitExerciseForm, self).clean(*args, **kwargs)
