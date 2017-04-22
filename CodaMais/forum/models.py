# Django.
from django.db import models

# local Django.
from forum import constants


class Topic(models.Model):
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)
    subtilte = models.CharField(max_length=constants.MAX_LENGTH_SUBTITLE)
    author = models.CharField(max_length=constants.MAX_LENGTH_AUTHOR)
    description = models.CharField(max_length=constants.MAX_LENGTH_DESCRIPTION)
    dateTopic = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title
