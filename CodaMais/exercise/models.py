# Django.
from django.db import models

# Third-Party.
from redactor.fields import RedactorField

# local Django.
from exercise import constants


class Exercise(models.Model):
    title = models.CharField(max_length=constants.MAX_LENGTH_TITLE)
    category = models.PositiveIntegerField(choices=constants.CATEGORY_CHOICES)
    statement_question = RedactorField(verbose_name=u'Text',
                                       allow_file_upload=False,    # Represents the text and, if any, images referring.
                                       allow_image_upload=True,    # to the statement of the exercise.
                                       redactor_options={'lang': 'en', 'focus': True},
                                       upload_to='tmp/')
    score = models.PositiveIntegerField()
    deprecated = models.PositiveIntegerField(choices=constants.DEPRECATED_CHOICES)
    input_exercise = models.CharField(max_length=constants.MAX_LENGTH_INPUT)
    output_exercise = models.CharField(max_length=constants.MAX_LENGTH_OUTPUT)

    def __str__(self):
        return self.title
