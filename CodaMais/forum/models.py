# Django.
from django.db import models

# local Django.
from forum import constants
from user.models import User


class Topic(models.Model):
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)
    subtitle = models.CharField(max_length=constants.MAX_LENGTH_SUBTITLE)
    author = models.CharField(max_length=constants.MAX_LENGTH_AUTHOR)
    description = models.CharField(max_length=constants.MAX_LENGTH_DESCRIPTION)
    dateTopic = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    description = models.CharField(max_length=constants.MAX_LENGTH_DESCRIPTION)
    user = models.ForeignKey(
          User,
          on_delete=models.CASCADE,)
    topic = models.ForeignKey(
          Topic,
          on_delete=models.CASCADE,)
    date_answer = models.DateTimeField(auto_now_add=True, blank=True)

    def update_or_creates(self, user, topic, description):
        self.user = user
        self.topic = topic
        self.description = description
        self.save()


    def __str__(self):
        return self.description
