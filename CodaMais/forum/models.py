# Django.
from django.db import models

# Import datetime class.
from datetime import datetime

# local Django.
from exercise import constants


class Topic(models.Model):
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)
    subtilte = models.CharField(max_length=constants.MAX_LENGTH_SUBTITLE)
    autor = models.CharField(max_length=constants.MAX_LENGTH_AUTHOR)
    description = models.CharField(max_length=constants.MAX_LENGTH_DESCRIPTION)
    date = models.DateField(("Data"), default=datetime.date.today)

    def __str__(self):
        return self.title
