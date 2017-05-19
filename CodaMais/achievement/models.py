# Django
from django.db import models

# local Django
from achievement import constants
from user.models import User


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


# Class: Achievement
# The class represents the relationship between the achievement and the user.
# The table can only be stored when the user gets the achievement.
class UserAchievement(models.Model):
    class Meta:
        unique_together = (('user', 'achievement'),)

    user = models.ForeignKey(
          User,
          on_delete=models.CASCADE,)

    achievement = models.ForeignKey(
            Achievement,
            on_delete=models.CASCADE,)

    def update_or_creates(self, achievement, user):
        self.achievement = achievement
        self.user = user
        self.save()

    def __str__(self):
        return self.user.email + "-" + str(self.achievement.name)
