# Django
from django.db import models

# local Django
from achievement import constants
# from user.models import User


class Achievement(models.Model):
    name = models.CharField(max_length=constants.MAX_LENGTH_NAME)

    description = models.CharField(max_length=constants.MAX_LENGTH_DESCRIPTION)

    # Indicate which group of achievements the current achievement is related to.
    achievement_type = models.PositiveIntegerField(choices=constants.ACHIEVEMENT_TYPE)

    # Indicate the minimum quantity of something to unlock the achievement.
    quantity = models.PositiveIntegerField()

    achievement_icon = models.ImageField(default=constants.ACHIEVEMENTE_IMAGE, editable=True)

    def __str__(self):
        return self.name
