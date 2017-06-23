'''
Copyright (C) 2017, CodaMais.
License: GNU General Public License v3.0, see LICENSE.txt
App: User
File: models.py
Contains all methods of the view layer related to the forum.
It is django's default to keep all methods in single file.
'''

# standard library
import datetime
import logging

# Django.
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
)
from django.db.models import EmailField
from django.core import validators
from django.apps import apps


# Local Django.
from . import constants
from .managers import UserManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(constants.PROJECT_NAME)


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


class Score(models.IntegerField):
    validator_min_value = validators.MinValueValidator(constants.SCORE_MIN_LENGTH)

    default_validators = [validator_min_value]

    def __init__(self, *args, **kwargs):
        kwargs['default'] = constants.SCORE_MIN_LENGTH
        super(models.IntegerField, self).__init__(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', ]

    username = Username()
    first_name = First_name()
    email = Email()
    score = Score()

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

    # Function to get user's current position in ranking.
    def get_position(self):
        # List of all cadastrated users.
        user_list = User.objects.filter().order_by('-score')

        position = 0

        for user in user_list:
            position = position + 1
            if user.username == self.username:
                break
            else:
                # Nothing to do.
                pass

        logger.info("User position in ranking: " + str(position))
        return position

    # Function to count all user correct exercises.
    def get_correct_exercises(self):
        Exercise = apps.get_model(app_label='exercise', model_name='Exercise')
        all_excersices = 0
        # Getting all exercise not deprecated.
        all_excersices = Exercise.objects.filter(deprecated='0').count()

        UserExercise = apps.get_model(app_label='exercise', model_name='UserExercise')
        user_correct_exercises = 0
        # Getting all the exercises answered correctly from the user.
        user_correct_exercises = UserExercise.objects.filter(status=True, user=self).count()

        logger.info("All exercisesr: " + str(all_excersices))
        logger.info("All correct exercises by user: " + self.username + ": " + str(all_excersices))

        if user_correct_exercises > 0:
            percentage_correct_exercises = (100 * user_correct_exercises) / all_excersices
        else:
            percentage_correct_exercises = 0

        percentage_correct_exercises = round(percentage_correct_exercises, 2)

        return percentage_correct_exercises


# This class is used to set a relation between the user that required the register and the activation key.
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
