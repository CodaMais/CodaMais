from django.db import models
from django.core.urlresolvers import reverse
from exercise import constants


class Exercise(models.Model):
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)
    category = models.PositiveIntegerField(choices=constants.CATEGORY_CHOICES)
    text = models.TextField()
    score = models.PositiveIntegerField()
    image = models.ImageField(null=True)
    deprecated = models.PositiveIntegerField(choices=constants.DEPRECATED_CHOICES)
    input_exercise = models.CharField(max_length=constants.MAX_LENGTH_INPUT)
    output_exercise = models.CharField(max_length=constants.MAX_LENGTH_OUTPUT)
