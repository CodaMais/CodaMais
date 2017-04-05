# standard library
import re

# Django.
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

# Local Django.
from .models import User
from .import constants


class UserRegisterForm(forms.ModelForm):
    # Form Fields.
    password = forms.CharField(widget=forms.PasswordInput,
                               label=_('Password'))

    password_confirmation = forms.CharField(widget=forms.PasswordInput,
                                            label=_('Password Confirmation'))

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'email',
        ]

    # Front-end validation function for register page.
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        email_from_database = User.objects.filter(email=email)
        username_from_database = User.objects.filter(username=username)

        if username_from_database.exists():
            raise forms.ValidationError(_(constants.USERNAME_REGISTERED))
        elif len(username) < constants.USERNAME_MIN_LENGTH:
            raise forms.ValidationError(_(constants.USERNAME_MIN_SIZE))
        elif not re.match(r'^[A-Za-z ]+$', first_name):
            raise forms.ValidationError(_(constants.USERNAME_FORMAT))
        elif email_from_database.exists():
            raise ValidationError(_(constants.EMAIL_REGISTERED))
        elif len(password) < constants.PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(_(constants.PASSWORD_MIN_SIZE))
        elif password != password_confirmation:
            raise forms.ValidationError(_(constants.PASSWORD_NOT_EQUAL))

        return super(UserRegisterForm, self).clean(*args, **kwargs)
