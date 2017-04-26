# standard library
import datetime

# Django.
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
)
from django.db.models import EmailField
from django.core import validators

# Local Django.
from . import constants
from .managers import UserManager


class Email(EmailField):
    validator = validators.EmailValidator(message=constants.EMAIL_FORMAT)

    default_validators = [validator]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = constants.EMAIL_FIELD_LENGTH
        kwargs['default'] = ''
        kwargs['unique'] = True
        super(EmailField, self).__init__(*args, **kwargs)


class Username(models.CharField):
    validator_min_length = validators.MinLengthValidator(constants.
                                                         USERNAME_MIN_LENGTH,
                                                         message=constants.
                                                         USERNAME_SIZE)
    validator_max_length = validators.MaxLengthValidator(constants.
                                                         USERNAME_MAX_LENGHT,
                                                         message=constants.
                                                         USERNAME_SIZE)

    default_validators = [validator_min_length, validator_max_length]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = constants.USERNAME_MAX_LENGHT
        kwargs['default'] = ''
        kwargs['unique'] = True
        super(models.CharField, self).__init__(*args, **kwargs)


class First_name(models.CharField):
    validator_max_length = validators.MaxLengthValidator(constants.
                                                         USERNAME_MAX_LENGHT,
                                                         message=constants.
                                                         FIRST_NAME_SIZE)
    validator_format = validators.RegexValidator(regex=r'^[A-Za-z ]+$',
                                                 message=constants.
                                                 FIRST_NAME_CHARACTERS)
    default_validators = [validator_max_length, validator_format]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = constants.FIRST_NAME_FIELD_LENGTH
        kwargs['default'] = ''
        super(models.CharField, self).__init__(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', ]

    username = Username()
    first_name = First_name()
    email = Email()

    # User Profile Image
    user_image = models.ImageField(default=constants.USER_IMAGE,
                                   editable=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'Perfil de Usuario'


class RecoverPasswordProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'Perfil de Usuario'
