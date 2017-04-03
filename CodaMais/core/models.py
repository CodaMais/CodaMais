# Django.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager

# Local Django.
from . import constants


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    username = models.CharField(max_length=constants.USERNAME_FIELD_LENGTH,
                                default='', unique=True)
    first_name = models.CharField(max_length=constants.FIRST_NAME_FIELD_LENGTH,
                                  default='')
    email = models.EmailField(max_length=constants.EMAIL_FIELD_LENGTH,
                              default='', unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
