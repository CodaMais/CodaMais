# Django.
from django.db import models
from django.contrib.auth.models import User

# Local Django.
from . import constants


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=constants.USERNAME_FIELD_LENGTH,
                                default='', unique=True)
    first_name = models.CharField(max_length=constants.FIRST_NAME_FIELD_LENGTH,
                                  default='')
    email = models.EmailField(max_length=constants.EMAIL_FIELD_LENGTH,
                              default='', unique=True)

    # Admin List function.
    def __unicode__(self):
        return self.username
