# standard library
import datetime

# Django.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Local Django.
from . import constants
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', ]

    username = models.CharField(max_length=constants.USERNAME_FIELD_LENGTH,
                                default='', unique=True)
    first_name = models.CharField(max_length=constants.FIRST_NAME_FIELD_LENGTH,
                                  default='')
    email = models.EmailField(max_length=constants.EMAIL_FIELD_LENGTH,
                              default='', unique=True)

    # User Profile Image
    user_image = models.ImageField(default=constants.USER_IMAGE,
                                   editable=False)

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
