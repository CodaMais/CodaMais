# standard library.
import logging

# Django.
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

# Local Django.
from .models import User
from .import constants

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(constants.PROJECT_NAME)


class UserRegisterForm(forms.ModelForm):
    # Form Fields.
    username = forms.CharField(label=constants.USERNAME,
                               max_length=constants.USERNAME_MAX_LENGHT)

    email = forms.EmailField(label=constants.EMAIL)

    password = forms.CharField(widget=forms.PasswordInput,
                               label=_(constants.PASSWORD))

    password_confirmation = forms.CharField(widget=forms.PasswordInput,
                                            label=_(constants.PASSWORD_CONFIRMATION))

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

        if username_from_database.exists():
            raise forms.ValidationError(_(constants.USERNAME_REGISTERED))
        elif email_from_database.exists():
            raise ValidationError(_(constants.EMAIL_REGISTERED))
        elif len(password) < constants.PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(_(constants.PASSWORD_SIZE))
        elif len(password) > constants.PASSWORD_MAX_LENGTH:
            raise forms.ValidationError(_(constants.PASSWORD_SIZE))
        elif password != password_confirmation:
            raise forms.ValidationError(_(constants.PASSWORD_NOT_EQUAL))

        return super(UserRegisterForm, self).clean(*args, **kwargs)


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label=_(constants.PASSWORD))

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get("password")

        if len(password) < constants.PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(_(constants.PASSWORD_SIZE))
        elif len(password) > constants.PASSWORD_MAX_LENGTH:
            raise forms.ValidationError(_(constants.PASSWORD_SIZE))
        else:
            pass

        return super(UserLoginForm, self).clean(*args, **kwargs)


class RecoverPasswordForm(forms.Form):
    email = forms.EmailField(label=constants.EMAIL)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_from_database = User.objects.filter(email=email)

        if email_from_database.exists():
            pass
        else:
            raise forms.ValidationError(_(constants.EMAIL_NOT_REGISTERED))

        return super(RecoverPasswordForm, self).clean(*args, **kwargs)


class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _(constants.PASSWORD)}),
                               label='')

    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':

                                                                       _(constants.PASSWORD_CONFIRMATION)}), label='')

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if len(password) < constants.PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(_(constants.PASSWORD_SIZE))
        elif len(password) > constants.PASSWORD_MAX_LENGTH:
            raise forms.ValidationError(_(constants.PASSWORD_SIZE))
        elif password != password_confirmation:
            raise forms.ValidationError(_(constants.PASSWORD_NOT_EQUAL))
        else:
            pass
        return super(ConfirmPasswordForm, self).clean(*args, **kwargs)


class UserEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
                            attrs={'class': 'form-control'}),
                            label=_(constants.NEW_PASSWORD),
                            required=False)

    password_confirmation = forms.CharField(widget=forms.PasswordInput(
                                            attrs={'class': 'form-control'}),
                                            label=_(constants.PASSWORD_CONFIRMATION),
                                            required=False)

    first_name = forms.CharField(widget=forms.TextInput(
                                attrs={'class': 'form-control'}),
                                label=constants.FIRST_NAME,
                                max_length=constants.FIRST_NAME_FIELD_LENGTH,
                                required=False)

    user_image = forms.ImageField(
                                label=constants.USER_IMAGE_FIELD,
                                required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'user_image',
        ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        logger.debug("User password: " + password)
        logger.debug("User password confirmation: " + password_confirmation)

        if len(password) != constants.NULL_FIELD:
            logger.debug("Trying to alter user password.")
            if len(password) < constants.PASSWORD_MIN_LENGTH:
                raise forms.ValidationError(_(constants.PASSWORD_SIZE))
            elif len(password) > constants.PASSWORD_MAX_LENGTH:
                raise forms.ValidationError(_(constants.PASSWORD_SIZE))
            elif password != password_confirmation:
                logger.debug("Password don't match with password confirmation.")
                raise forms.ValidationError(_(constants.PASSWORD_NOT_EQUAL))
            else:
                logger.debug("User password: " + password)
                logger.debug("User password confirmation: " + password_confirmation)
        else:
            pass

        return super(UserEditForm, self).clean(*args, **kwargs)
