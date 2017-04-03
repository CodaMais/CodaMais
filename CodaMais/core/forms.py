# Django.
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

# Local Django.
from .models import User


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
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        email_from_database = User.objects.filter(email=email)
        username_from_database = User.objects.filter(username=username)

        if email_from_database.exists():
            raise ValidationError(_("This Email has been already registered"))
        elif password != password_confirmation:
            raise forms.ValidationError(_("Passwords don't match."))
        elif username_from_database.exists():
            raise forms.ValidationError(_("Nickname already registered"))
        return super(UserRegisterForm, self).clean(*args, **kwargs)
